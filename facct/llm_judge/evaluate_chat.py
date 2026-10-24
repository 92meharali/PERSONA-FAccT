"""Evaluate a frozen, manually recorded in-chat scoring pass."""
import argparse
import csv
import importlib.metadata
import json
from pathlib import Path

import numpy as np
import pandas as pd

from facct.analysis.screening import features
from .evaluate import BUDGETS, POLICIES, ROOT, SEED, followup_labels, measures, paired_intervals
from .run import SOURCE_HASH, check_packet, require, sha, write_json


def load_chat_scores(packet, judgments):
    requests, manifest = check_packet(packet)
    with Path(judgments).open(newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    require(len(rows) == len(requests) == 660, 'The full 660-item pass is required')
    require([int(row['index']) for row in rows] == list(range(1, 661)), 'Indexes must be ordered and complete')
    mapping = pd.read_csv(Path(packet) / 'mapping.csv', dtype=str)
    require(len(mapping) == 660 and not mapping.request_id.duplicated().any(), 'Invalid packet mapping')
    require(set(mapping.request_id) == {request['request_id'] for request in requests}, 'Mapping/request mismatch')
    scores = []
    for row, request in zip(rows, requests):
        require(row['priority'] in ('0', '1', '2', '3'), 'Invalid priority')
        require(row['uncertain'] in ('true', 'false'), 'Invalid uncertainty')
        require(bool(row['rationale']), 'A rationale is required for every item')
        response = json.loads(request['messages'][1]['content'])['response']
        require(not row['evidence'] or row['evidence'] in response, 'Evidence is not an exact response substring')
        scores.append({'request_id': request['request_id'], 'priority': int(row['priority']),
                       'uncertain': row['uncertain'] == 'true'})
    return mapping.merge(pd.DataFrame(scores), on='request_id', validate='one_to_one'), manifest


def evaluate_chat(packet, judgments, output, replicates=2000, root=ROOT):
    require(replicates > 0, 'Positive bootstrap count required')
    require(sha(root / 'analysis/processed/persona_all.csv') == SOURCE_HASH, 'Changed source corpus')
    scores, packet_manifest = load_chat_scores(packet, judgments)
    require(set(scores.task) == {'followup'} and set(scores.domain) == {'mental_health'},
            'This pass covers only the mental-health follow-up packet')
    corpus = pd.read_csv(root / 'analysis/processed/persona_all.csv')
    batch = scores.merge(corpus[corpus.domain == 'mental_health'],
                         on=['domain', 'annotation_item_id'], validate='one_to_one').sort_values('source_id')
    require(len(batch) == 660 and not batch.source_id.duplicated().any(), 'Incomplete source batch')
    y = batch.annotation_item_id.map(followup_labels(root)).to_numpy()
    require(not pd.isna(y).any(), 'Unmapped human follow-up labels')
    y = y.astype(bool)
    ids = batch.source_id.to_numpy()
    clusters = (batch.domain + ':' + batch.prompt_id).to_numpy()
    X = np.column_stack([batch.priority.to_numpy(float), features(batch)])
    rows = []
    for budget in BUDGETS:
        for column, policy in enumerate(POLICIES):
            rows.append({'policy': policy, 'budget': budget,
                         **measures(y, X[:, column], ids, clusters, budget)})
        n, p = len(y), int(y.sum())
        k = rows[-1]['selected']
        rows.append({'policy': 'uniform_random', 'budget': budget, 'n': n, 'concerns': p,
                     'selected': k, 'caught': k*p/n, 'missed': p-k*p/n,
                     'recall': k/n if p else np.nan, 'precision': p/n if k else np.nan})
    intervals = paired_intervals(y, X, ids, clusters, replicates)
    for row in intervals:
        budget = row['budget']
        baseline = row['contrast'].removeprefix('llm_judge_minus_')
        judge = next(item for item in rows if item['policy'] == 'llm_judge' and item['budget'] == budget)
        other = next(item for item in rows if item['policy'] == baseline and item['budget'] == budget)
        row['difference'] = judge['recall'] - other['recall']
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    pd.DataFrame(rows).to_csv(output / 'metrics.csv', index=False)
    pd.DataFrame(intervals).to_csv(output / 'paired_intervals.csv', index=False)
    summary = {'status': 'exploratory_in_chat_sensitivity', 'requests': len(scores),
               'positive_priority': int((batch.priority > 0).sum()),
               'score_counts': {str(i): int((batch.priority == i).sum()) for i in range(4)},
               'uncertain_count': int(batch.uncertain.sum()),
               'model_snapshot': 'not pinned by chat interface',
               'prior_study_results_visible_to_chat': True,
               'external_api_calls': 0, 'not_independent_human_evaluation': True,
               'criterion': 'contextual anthropomorphic implication reviewworthiness',
               'replicates': replicates, 'tie_seed': SEED,
               'source_sha256': SOURCE_HASH,
               'packet_manifest_sha256': sha(Path(packet) / 'manifest.json'),
               'judgments_sha256': sha(judgments),
               'followup_manifest_sha256': sha(root / 'facct/independent_annotation/outputs/manifest.json'),
               'evaluator_sha256': sha(Path(__file__)),
               'software_versions': {name: importlib.metadata.version(name)
                                     for name in ('numpy', 'pandas', 'scipy', 'scikit-learn')},
               'outputs_sha256': {name: sha(output / name) for name in ('metrics.csv', 'paired_intervals.csv')},
               'note': 'One chat-session model assessed all 660; earlier paper results were visible. Do not treat as blinded, pinned, independently reproducible comparator.'}
    write_json(output / 'manifest.json', summary)
    return {'output': str(output), 'scores': summary['score_counts'], 'uncertain': summary['uncertain_count']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', required=True, type=Path)
    parser.add_argument('--judgments', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--replicates', type=int, default=2000)
    args = parser.parse_args()
    print(json.dumps(evaluate_chat(args.packet, args.judgments, args.output, args.replicates), indent=2))
