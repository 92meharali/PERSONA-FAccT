"""Local packet and record validation for an exploratory in-chat LLM assessment.

No model invocation, human-label loading, or performance estimation is performed.
Judgments must be authored by the assistant after reading each complete item.
"""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from .run import check_packet, parse_output, read_jsonl, require, sha, write_json

SEED = 'chat-pilot-20261024-v1'


def prepare(packet, output, count=24):
    requests, parent = check_packet(packet)
    require(parent['tasks'] == ['followup'], 'Use the follow-up-only packet')
    require(0 < count <= len(requests), 'Invalid sample size')
    ordered = sorted(requests, key=lambda r: hashlib.sha256(
        f"{SEED}|{r['request_id']}".encode()).hexdigest())
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    inputs = output / 'requests.jsonl'
    inputs.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in ordered[:count]))
    write_json(output / 'manifest.json', {
        'status': 'prepared_in_chat_pilot', 'mode': 'current_chat_assistant',
        'date': '2026-10-24', 'sampling_seed': SEED, 'sample_size': count,
        'population_size': len(requests), 'requests_sha256': sha(inputs),
        'parent_manifest_sha256': sha(Path(packet) / 'manifest.json'),
        'parent_request_file_sha256': parent['request_file_sha256'],
        'source_sha256': parent['source_sha256'],
        'model_snapshot': None, 'decoding_parameters': None,
        'external_api_calls': 0, 'human_evaluation_conducted': False,
        'prior_results_visible_in_chat': True, 'item_labels_in_assessment_view': False,
        'note': 'Exploratory in-chat pilot, not independent/blinded API evidence. '
                'Assistant has prior study context; sample selected without loading labels. '
                'No human reference comparison or full-corpus performance claim.'})


def inputs(directory):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_text())
    require(sha(directory / 'requests.jsonl') == manifest['requests_sha256'], 'Changed input packet')
    records = read_jsonl(directory / 'requests.jsonl')
    require(len(records) == manifest['sample_size'], 'Changed sample size')
    return records, manifest


def show(directory, start, count):
    records, _ = inputs(directory)
    require(start >= 0 and count > 0, 'Invalid range')
    for i, request in enumerate(records[start:start+count], start+1):
        payload = json.loads(request['messages'][1]['content'])
        print(json.dumps({'index': i, 'request_id': request['request_id'], **payload}, ensure_ascii=False))


def validate(directory):
    directory = Path(directory)
    records, manifest = inputs(directory)
    path = directory / 'judgments.jsonl'
    judgments = read_jsonl(path)
    lookup = {r['request_id']: r for r in records}
    require(len(judgments) == len(lookup), 'Incomplete pilot; cannot claim completion')
    require(len({j['request_id'] for j in judgments}) == len(judgments), 'Duplicate judgment')
    require({j['request_id'] for j in judgments} == set(lookup), 'Judgment IDs differ from packet')
    for judgment in judgments:
        request = lookup[judgment['request_id']]
        response = json.loads(request['messages'][1]['content'])['response']
        parse_output({k: v for k, v in judgment.items() if k != 'request_id'}, response)
    report = {
        'status': 'completed_exploratory_chat_pilot_not_full_benchmark',
        'assessed': len(judgments), 'population': manifest['population_size'],
        'priority_counts': dict(sorted(Counter(j['priority'] for j in judgments).items())),
        'uncertain_count': sum(j['uncertain'] for j in judgments),
        'judgments_sha256': sha(path), 'input_manifest_sha256': sha(directory / 'manifest.json'),
        'external_api_calls': 0, 'new_human_ratings': 0,
        'human_reference_comparison': 'not_performed',
        'model_snapshot': None, 'prior_results_visible_in_chat': True,
        'interpretation': 'Counts describe LLM decisions only, not accuracy or target prevalence.'}
    target = directory / 'validation.json'
    if target.exists():
        require(json.loads(target.read_text()) == report, 'Frozen validation differs; preserve original records')
    else:
        write_json(target, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('--packet', required=True, type=Path)
    prep.add_argument('--output', required=True, type=Path)
    prep.add_argument('--count', default=24, type=int)
    view = sub.add_parser('show')
    view.add_argument('--directory', required=True, type=Path)
    view.add_argument('--start', default=0, type=int)
    view.add_argument('--count', default=8, type=int)
    check = sub.add_parser('validate')
    check.add_argument('--directory', required=True, type=Path)
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.packet, args.output, args.count)
    elif args.command == 'show':
        show(args.directory, args.start, args.count)
    else:
        print(json.dumps(validate(args.directory), indent=2))


if __name__ == '__main__':
    main()
