import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import average_precision_score

from facct.llm_judge import run as runner
from facct.llm_judge import evaluate as evaluation


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    (root / 'analysis/processed').mkdir(parents=True)
    (root / 'facct/llm_judge').mkdir(parents=True)
    for file in ('prompt.md', 'plan.md'):
        (root / 'facct/llm_judge' / file).write_text((Path(runner.__file__).parent / file).read_text())
    for domain in ('mental_health', 'education'):
        p = root / 'data/clean_domains' / domain
        p.mkdir(parents=True)
        (p / 'rubric.md').write_text('A synthetic test rubric, never empirical evidence.')
    frame = pd.DataFrame([dict(domain='mental_health' if i < 6 else 'education',
                               annotation_item_id=f'item-{i}', prompt_id=f'p-{i//2}',
                               prompt=f'Test prompt {i}', response=f'Test response {i}',
                               H=float(i), D=3 if i % 2 else 1, F=5, OA=4,
                               model='SECRET_GENERATOR', condition='SECRET_CONDITION',
                               scenario_type='SECRET_SCENARIO') for i in range(10)])
    path = root / 'analysis/processed/persona_all.csv'
    frame.to_csv(path, index=False)
    monkeypatch.setattr(runner, 'SOURCE_HASH', runner.sha(path))
    monkeypatch.setattr(evaluation, 'SOURCE_HASH', runner.sha(path))
    packet = tmp_path / 'packet'
    runner.prepare(packet, ['source_D'], root)
    manifest = json.loads((packet / 'manifest.json').read_text())
    settings = dict(provider='TEST_ONLY', model='TEST_SNAPSHOT', version_pinned=True,
                    transmission_approved=True, approval_record='synthetic fixture only',
                    pricing_record='synthetic fixture only', budget_usd=1,
                    per_request_ceiling_usd=.01, max_output_tokens=100, decoding={},
                    request_file_sha256=manifest['request_file_sha256'])
    return root, packet, settings, tmp_path / 'responses.jsonl'


def fake_adapter(messages, settings):
    payload = json.loads(messages[1]['content'])
    return dict(model=settings['model'], response_id='TEST_ONLY_ID', cost_usd=.001, usage={'test': True},
                output=dict(priority=1, uncertain=False, evidence=payload['response'], rationale='Synthetic test only'))


def test_blinding(prepared):
    _, packet, _, _ = prepared
    rows, _ = runner.check_packet(packet)
    for row in rows:
        payload = json.loads(row['messages'][1]['content'])
        assert set(payload) == {'domain', 'prompt', 'response'}
        text = json.dumps(row['messages'])
        assert not any(x in text for x in ('SECRET_GENERATOR', 'SECRET_CONDITION', 'SECRET_SCENARIO', 'item-'))
        assert set(row) == {'request_id', 'request_hash', 'task', 'messages'}


def test_prepare_does_not_overwrite(prepared):
    root, packet, _, _ = prepared
    with pytest.raises(FileExistsError):
        runner.prepare(packet, ['source_D'], root)


def test_disabled_settings_never_call_adapter(prepared):
    _, packet, settings, log = prepared
    settings['transmission_approved'] = False
    with pytest.raises(ValueError, match='approval'):
        runner.run(packet, settings, lambda *_: pytest.fail('Called without approval'), log)
    assert not log.exists()


def test_success_resume_and_mutation(prepared):
    _, packet, settings, log = prepared
    calls = []
    def adapter(messages, config):
        calls.append(1)
        return fake_adapter(messages, config)
    runner.run(packet, settings, adapter, log)
    runner.run(packet, settings, adapter, log)
    assert len(calls) == 10
    scores, _ = evaluation.load_scores(packet, log)
    assert len(scores) == 10 and not scores.failed.any()
    settings['decoding'] = {'changed': True}
    with pytest.raises(ValueError, match='settings'):
        runner.run(packet, settings, adapter, log)


def test_budget_guard_before_calls(prepared):
    _, packet, settings, log = prepared
    settings['budget_usd'] = .005
    with pytest.raises(ValueError, match='Budget'):
        runner.run(packet, settings, lambda *_: pytest.fail('Budget exceeded'), log)


def test_failures_remain_in_batch(prepared):
    _, packet, settings, log = prepared
    def invalid(messages, config):
        result = fake_adapter(messages, config)
        result['output']['evidence'] = 'Invented non-verbatim passage'
        return result
    runner.run(packet, settings, invalid, log)
    scores, _ = evaluation.load_scores(packet, log)
    assert scores.failed.all() and scores.priority.eq(2).all() and len(scores) == 10


def test_cost_breach_halts_and_blocks_resume(prepared):
    _, packet, settings, log = prepared
    def overcharge(messages, config):
        result = fake_adapter(messages, config)
        result['cost_usd'] = 100
        return result
    with pytest.raises(RuntimeError, match='halted'):
        runner.run(packet, settings, overcharge, log)
    assert len(runner.read_jsonl(log)) == 1
    with pytest.raises(ValueError, match='ceiling breach'):
        runner.run(packet, settings, fake_adapter, log)


def test_interruption_and_partial_logs(prepared):
    _, packet, settings, log = prepared
    log.with_suffix('.inflight.json').write_text('{}')
    with pytest.raises(ValueError, match='In-flight'):
        runner.run(packet, settings, fake_adapter, log)
    log.with_suffix('.inflight.json').unlink()
    runner.run(packet, settings, fake_adapter, log)
    lines = log.read_text().splitlines()
    log.write_text('\n'.join(lines[:-1]) + '\n')
    with pytest.raises(ValueError, match='coverage'):
        evaluation.load_scores(packet, log)


@pytest.mark.parametrize('field,value', [('model', 'UNAPPROVED_MODEL'), ('cost_usd', None), ('usage', None)])
def test_provider_contract_breach_halts_and_blocks_resume(prepared, field, value):
    _, packet, settings, log = prepared
    def invalid(messages, config):
        result = fake_adapter(messages, config)
        result[field] = value
        return result
    with pytest.raises(RuntimeError, match='halted'):
        runner.run(packet, settings, invalid, log)
    assert len(runner.read_jsonl(log)) == 1
    with pytest.raises(ValueError, match='contract breach'):
        runner.run(packet, settings, fake_adapter, log)


@pytest.mark.parametrize('value', [True, 1.1, -1, 4, None, '2'])
def test_priority_type_and_range(value):
    with pytest.raises(ValueError):
        runner.parse_output(dict(priority=value, uncertain=False, evidence='', rationale='x'), 'response')


def test_exact_budgets_ties_and_sklearn_ap():
    y = np.array([True, False, True, False, True])
    score = np.array([3, 2, 2, 0, 0])
    result = evaluation.measures(y, score, np.array(list('abcde')), np.array([0, 0, 1, 1, 2]), .4)
    assert result['selected'] == 2
    assert result['ap'] == pytest.approx(average_precision_score(y, score))
    assert result == evaluation.measures(y, score, np.array(list('abcde')), np.array([0, 0, 1, 1, 2]), .4)


@pytest.mark.parametrize('y', [[False, False], [True, True]])
def test_degenerate_and_zero_capacity(y):
    result = evaluation.measures(y, [1, 1], ['a', 'b'], ['p', 'p'], .2)
    assert result['selected'] == 0 and np.isnan(result['precision']) and np.isnan(result['auc'])
    if not any(y):
        assert np.isnan(result['recall']) and np.isnan(result['ap'])


def test_paired_cluster_bootstrap_deterministic_and_degenerate():
    y = np.array([1, 1, 0, 0], dtype=bool)
    X = np.repeat(np.array([[3], [2], [1], [0]]), 4, axis=1)
    a = evaluation.paired_intervals(y, X, np.array(list('abcd')), np.array(['x','x','y','y']), 50)
    b = evaluation.paired_intervals(y, X, np.array(list('abcd')), np.array(['x','x','y','y']), 50)
    assert a == b and all(r['undefined_replicates'] > 0 for r in a)
    assert all(r['lo'] == r['hi'] == 0 for r in a if r['contrast'] != 'llm_judge_minus_uniform_random')


def test_request_tamper_rejected(prepared):
    _, packet, _, _ = prepared
    with (packet / 'requests.jsonl').open('a') as stream:
        stream.write('{}\n')
    with pytest.raises(ValueError, match='Changed requests'):
        runner.check_packet(packet)


def test_evaluation_end_to_end_synthetic_only(prepared, tmp_path):
    root, packet, settings, log = prepared
    runner.run(packet, settings, fake_adapter, log)
    out = tmp_path / 'synthetic_results'
    result = evaluation.evaluate(packet, log, out, 20, root)
    metrics = pd.read_csv(out / 'metrics.csv')
    assert result['metrics'] == 40
    assert set(metrics.policy) == {'llm_judge','high_H','length','markers','uniform_random'}
    assert metrics.groupby(['domain','budget']).selected.nunique().eq(1).all()
    assert json.loads((out / 'manifest.json').read_text())['status'] == 'pilot_not_final'


def test_chat_pilot_selection_and_validation(prepared, tmp_path):
    from facct.llm_judge import chat_pilot
    root, _, _, _ = prepared
    packet = tmp_path / 'followup'
    runner.prepare(packet, ['followup'], root)
    sample = tmp_path / 'chat'
    chat_pilot.prepare(packet, sample, 3)
    records, manifest = chat_pilot.inputs(sample)
    assert manifest['sample_size'] == 3 and manifest['population_size'] == 6
    assert manifest['prior_results_visible_in_chat'] is True
    assert manifest['model_snapshot'] is None
    other = tmp_path / 'chat_repeat'
    chat_pilot.prepare(packet, other, 3)
    assert (other / 'requests.jsonl').read_bytes() == (sample / 'requests.jsonl').read_bytes()
    judgments = [dict(request_id=r['request_id'], priority=0, uncertain=False, evidence='',
                      rationale='Synthetic validation test; not an actual assessment.') for r in records]
    path = sample / 'judgments.jsonl'
    path.write_text(''.join(json.dumps(j) + '\n' for j in judgments))
    report = chat_pilot.validate(sample)
    assert report['assessed'] == 3 and report['new_human_ratings'] == 0
    assert report['external_api_calls'] == 0
    assert report['human_reference_comparison'] == 'not_performed'
    judgments[0]['priority'] = 1
    path.write_text(''.join(json.dumps(j) + '\n' for j in judgments))
    with pytest.raises(ValueError, match='Frozen validation differs'):
        chat_pilot.validate(sample)


def test_chat_pilot_rejects_partial_and_invalid_evidence(prepared, tmp_path):
    from facct.llm_judge import chat_pilot
    root, _, _, _ = prepared
    packet = tmp_path / 'followup'
    runner.prepare(packet, ['followup'], root)
    sample = tmp_path / 'chat'
    chat_pilot.prepare(packet, sample, 2)
    records, _ = chat_pilot.inputs(sample)
    path = sample / 'judgments.jsonl'
    path.write_text('')
    with pytest.raises(ValueError, match='Incomplete pilot'):
        chat_pilot.validate(sample)
    judgments = [dict(request_id=r['request_id'], priority=2, uncertain=False,
                      evidence='NOT PRESENT IN SYNTHETIC RESPONSE', rationale='Test only') for r in records]
    path.write_text(''.join(json.dumps(j) + '\n' for j in judgments))
    with pytest.raises(ValueError, match='verbatim'):
        chat_pilot.validate(sample)
