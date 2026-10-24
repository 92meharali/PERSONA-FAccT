"""Evaluate complete judge logs against immutable labels, never generate labels."""
import argparse
import importlib.metadata
import json
from pathlib import Path

import numpy as np
import pandas as pd

from facct.analysis.screening import capacity, features, order_scores, rank_metrics, tie_keys
from facct.analysis.uncertainty import draw_indices, summarize
from .run import ROOT, SOURCE_HASH, check_packet, digest, parse_output, read_jsonl, require, sha, validate_settings, write_json

SEED = 20261002
BUDGETS = (.05, .10, .20, .30)
POLICIES = ('llm_judge', 'high_H', 'length', 'markers')


def load_scores(packet, log):
    requests, manifest = check_packet(packet)
    settings = json.loads(Path(log).with_suffix('.settings.json').read_text())
    validate_settings(settings, manifest)
    records = read_jsonl(log)
    indexed = {r['request_id']: r for r in records}
    require(len(indexed) == len(records) and set(indexed) == {r['request_id'] for r in requests},
            'Complete, nonduplicated scoring coverage required; no partial-result report')
    require(not Path(log).with_suffix('.inflight.json').exists(), 'Unreconciled in-flight request')
    rows = []
    for request in requests:
        record = indexed[request['request_id']]
        require(record['request_hash'] == request['request_hash'] and record['settings_hash'] == digest(settings),
                'Log does not match frozen requests/settings')
        require(record['status'] in ('ok', 'failed'), 'Unknown status')
        require(not record.get('budget_ceiling_breach', False), 'Budget violation requires reconciliation')
        require(not record.get('provider_contract_breach', False), 'Provider contract violation requires reconciliation')
        priority = 2
        if record['status'] == 'ok':
            answer = record['adapter_result']
            require(answer['model'] == settings['model'], 'Model mismatch')
            response = json.loads(request['messages'][1]['content'])['response']
            parsed = parse_output(answer['output'], response)
            require(parsed == record['parsed'] and parsed['priority'] == record['priority'], 'Changed parsed score')
            priority = parsed['priority']
        else:
            require(record['priority'] == 2, 'Failure fallback must remain 2')
        rows.append({'request_id': request['request_id'], 'priority': priority,
                     'failed': record['status'] == 'failed'})
    mapping = pd.read_csv(Path(packet) / 'mapping.csv', dtype=str)
    require(not mapping.request_id.duplicated().any() and set(mapping.request_id) == set(indexed), 'Invalid mapping')
    return mapping.merge(pd.DataFrame(rows), on='request_id', validate='one_to_one'), settings


def followup_labels(root):
    out = root / 'facct/independent_annotation/outputs'
    manifest = json.loads((out / 'manifest.json').read_text())
    require(sha(out / 'resolved_labels.csv') == manifest['output_hashes']['resolved_labels.csv'], 'Changed follow-up labels')
    source = Path(manifest['source'])
    frame_path = source / 'frame/immutable_frame.csv'
    require(sha(frame_path) == manifest['source_hashes']['frame/immutable_frame.csv'], 'Changed follow-up mapping')
    mapping = pd.read_csv(frame_path, usecols=['study_id', 'annotation_item_id'], dtype=str)
    labels = pd.read_csv(out / 'resolved_labels.csv', usecols=['study_id', 'resolved'])
    merged = mapping.merge(labels, on='study_id', validate='one_to_one')
    require(len(merged) == 660 and merged.resolved.isin([0, 1]).all(), 'Unexpected incomplete follow-up reference')
    return merged.set_index('annotation_item_id').resolved


def measures(y, score, ids, clusters, budget, seed=SEED):
    y = np.asarray(y, dtype=bool)
    n, p = len(y), int(y.sum())
    require(n > 0 and len(score) == n and len(ids) == n, 'Invalid metric inputs')
    k = capacity(n, budget)
    order = order_scores(score, tie_keys(ids, seed))
    caught = int(y[order[:k]].sum())
    ap, auc, workload = rank_metrics(y, score, order)
    return {'n': n, 'concerns': p, 'concern_clusters': len(set(np.asarray(clusters)[y])),
            'selected': k, 'caught': caught, 'missed': p-caught,
            'prevalence': p/n, 'recall': caught/p if p else np.nan,
            'precision': caught/k if k else np.nan,
            'unselected_prevalence': (p-caught)/(n-k) if n > k else np.nan,
            'ap': ap, 'auc': auc, 'delta_random': caught/p-k/n if p else np.nan,
            **dict(zip(('workload_50', 'workload_80', 'workload_90', 'workload_100'), workload))}


def paired_intervals(y, X, ids, clusters, replicates, seed=20261024):
    require(replicates > 0, 'Positive replicate count required')
    rng = np.random.default_rng(seed)
    differences = np.full((replicates, len(BUDGETS), 4), np.nan)
    domains = np.zeros(len(y), dtype=int)
    for b in range(replicates):
        idx, copies = draw_indices(domains, clusters, rng)
        yy = y[idx]
        if not yy.sum():
            continue
        ties = tie_keys([f'{v}|{copy}' for v, copy in zip(ids[idx], copies)], SEED)
        orders = [order_scores(X[idx, j], ties) for j in range(X.shape[1])]
        for bi, budget in enumerate(BUDGETS):
            k = capacity(len(idx), budget)
            recalls = [yy[o[:k]].sum()/yy.sum() for o in orders]
            differences[b, bi] = [recalls[0]-r for r in recalls[1:]] + [recalls[0]-k/len(idx)]
    rows = []
    for bi, budget in enumerate(BUDGETS):
        for j, baseline in enumerate((*POLICIES[1:], 'uniform_random')):
            lo, hi, finite = summarize(differences[:, bi, j])
            rows.append({'budget': budget, 'contrast': 'llm_judge_minus_' + baseline,
                         'lo': lo, 'hi': hi, 'finite_replicates': finite,
                         'undefined_replicates': replicates-finite,
                         'interval_status': 'conditional_on_defined_draws' if finite < replicates else 'pointwise_exploratory'})
    return rows


def evaluate(packet, log, output, replicates=2000, root=ROOT):
    require(sha(root / 'analysis/processed/persona_all.csv') == SOURCE_HASH, 'Changed corpus')
    scores, settings = load_scores(packet, log)
    corpus = pd.read_csv(root / 'analysis/processed/persona_all.csv')
    require(not corpus.duplicated(['domain', 'annotation_item_id']).any(), 'Duplicate corpus IDs')
    rows, intervals, sensitivity, selected_rows = [], [], [], []
    followup = followup_labels(root) if 'followup' in set(scores.task) else None
    for (task, domain), group in scores.groupby(['task', 'domain'], sort=True):
        expected = corpus[corpus.domain == domain]
        require(set(group.annotation_item_id) == set(expected.annotation_item_id), 'Incomplete declared domain batch')
        batch = group.merge(expected, on=['domain', 'annotation_item_id'], validate='one_to_one').sort_values('source_id')
        if task == 'followup':
            require(domain == 'mental_health', 'Follow-up is mental-health only')
            y = batch.annotation_item_id.map(followup).to_numpy()
            require(not pd.isna(y).any(), 'Unmapped follow-up labels')
            y = y.astype(bool)
        else:
            col = task.split('_')[1]
            y = (batch[col] >= 3 if col == 'D' else batch[col] < 4).to_numpy()
        ids = batch.source_id.to_numpy()
        clusters = (batch.domain + ':' + batch.prompt_id).to_numpy()
        X = np.column_stack([batch.priority.to_numpy(float), features(batch)])
        header = {'task': task, 'domain': domain, 'failed_requests': int(batch.failed.sum())}
        for budget in BUDGETS:
            policy_metrics = {}
            for i, policy in enumerate(POLICIES):
                result = measures(y, X[:, i], ids, clusters, budget)
                policy_metrics[policy] = result
                rows.append({**header, 'policy': policy, 'budget': budget, **result})
                selection = order_scores(X[:, i], tie_keys(ids, SEED))[:result['selected']]
                selected_rows.extend({'task': task, 'domain': domain, 'budget': budget,
                                      'policy': policy, 'source_id': ids[k]} for k in selection)
            n, p, k = len(y), int(y.sum()), capacity(len(y), budget)
            rows.append({**header, 'policy': 'uniform_random', 'budget': budget,
                         'n': n, 'concerns': p, 'concern_clusters': len(set(clusters[y])),
                         'selected': k, 'caught': k*p/n, 'missed': p-k*p/n,
                         'recall': k/n if p else np.nan, 'precision': p/n if k else np.nan,
                         'prevalence': p/n, 'unselected_prevalence': p/n if n > k else np.nan,
                         'ap': np.nan, 'auc': np.nan})
            for fallback in (0, 2, 3):
                altered = X[:, 0].copy()
                altered[batch.failed.to_numpy()] = fallback
                sensitivity.append({**header, 'kind': 'failure_fallback', 'value': fallback, 'budget': budget,
                                    **measures(y, altered, ids, clusters, budget)})
            for seed in range(SEED, SEED+100):
                for i, policy in enumerate(POLICIES):
                    sensitivity.append({**header, 'kind': 'tie_seed', 'policy': policy, 'value': seed,
                                        'budget': budget, **measures(y, X[:, i], ids, clusters, budget, seed)})
        for record in paired_intervals(y, X, ids, clusters, replicates):
            budget = record['budget']
            judge = next(r for r in rows if r['task'] == task and r['domain'] == domain and r['budget'] == budget and r['policy'] == 'llm_judge')
            base = record['contrast'].removeprefix('llm_judge_minus_')
            comparison = next(r for r in rows if r['task'] == task and r['domain'] == domain and r['budget'] == budget and r['policy'] == base)
            intervals.append({**header, **record, 'difference': judge['recall']-comparison['recall']})
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    for name, data in [('metrics', rows), ('paired_intervals', intervals), ('sensitivity', sensitivity), ('selections', selected_rows)]:
        pd.DataFrame(data).to_csv(output / f'{name}.csv', index=False)
    write_json(output / 'manifest.json', {
        'status': 'exploratory_final' if replicates >= 2000 else 'pilot_not_final',
        'requests': len(scores), 'model': settings['model'], 'provider': settings['provider'],
        'replicates': replicates, 'source_sha256': SOURCE_HASH,
        'log_sha256': sha(log), 'settings_sha256': sha(Path(log).with_suffix('.settings.json')),
        'packet_manifest_sha256': sha(Path(packet) / 'manifest.json'),
        'followup_manifest_sha256': sha(root / 'facct/independent_annotation/outputs/manifest.json') if followup is not None else None,
        'software_versions': {name: importlib.metadata.version(name) for name in ('numpy', 'pandas', 'scipy', 'scikit-learn')},
        'plan_sha256': sha(root / 'facct/llm_judge/plan.md'),
        'code_sha256': sha(Path(__file__)), 'runner_sha256': sha(Path(__file__).with_name('run.py')),
        'results': {p.name: sha(p) for p in output.glob('*.csv')},
        'note': 'Model scores are not human labels. No trained-fold comparison or rater-population inference.'})
    return {'output': str(output), 'metrics': len(rows), 'contrasts': len(intervals)}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', required=True, type=Path)
    p.add_argument('--log', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--replicates', type=int, default=2000)
    a = p.parse_args()
    print(json.dumps(evaluate(a.packet, a.log, a.output, a.replicates), indent=2))
