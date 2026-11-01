"""Package the completed-evidence revision without regenerating analytical assets."""
import argparse
import json
import re
import shutil
import tempfile
import zipfile
from datetime import date
from pathlib import Path

from facct.paper.build_overleaf import DEST, ROOT, sha, validate


def same_table_evidence(before, after):
    """Allow caption/comment edits, never a changed numerical table or macro."""
    before, after = before.decode(), after.decode()
    pattern = r"\\begin\{tabular\}.*?\\end\{tabular\}"
    old_tables = re.findall(pattern, before, re.S)
    if old_tables:
        return (old_tables == re.findall(pattern, after, re.S)
                and re.findall(r"\\label\{[^}]+\}", before)
                == re.findall(r"\\label\{[^}]+\}", after))
    clean = lambda text: "\n".join(line for line in text.splitlines()
                                    if line.strip() and not line.lstrip().startswith("%"))
    return clean(before) == clean(after)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout-report', type=str)
    parser.add_argument('--release-name', default='PERSONA_FAccT_Overleaf_2026-10-24_review')
    parser.add_argument('--revision-date', default='2026-10-24', type=date.fromisoformat)
    parser.add_argument('--revision-scope', default='Review-driven clarity revision; numerical evidence unchanged')
    parser.add_argument('--additional-assets-manifest', type=str)
    parser.add_argument('--criterion-transfer-assets-manifest', type=str)
    parser.add_argument('--presentation-updates', action='store_true',
                        help='Verify caption-only table changes and regenerated summary figures')
    args = parser.parse_args()
    if not args.release_name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.release_name):
        parser.error('release-name must be a simple file stem')
    manifest_path = DEST / 'package_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    expected = set(manifest['files'])
    additions = {}
    if args.additional_assets_manifest:
        with open(args.additional_assets_manifest) as stream:
            asset_manifest = json.load(stream)
        asset_parent = Path(args.additional_assets_manifest).parent
        assert asset_manifest['analysis_manifest_sha256'] == sha(asset_parent / 'manifest.json')
        for name, digest in asset_manifest['files'].items():
            assert name in {'prefix_threshold.tex', 'exclusive_profiles.tex'}, 'Unexpected added asset'
            relative = 'tables/' + name
            assert sha(DEST / relative) == digest, 'Generated asset hash mismatch'
            additions[relative] = digest
        expected |= set(additions)
    if args.criterion_transfer_assets_manifest:
        transfer_path = Path(args.criterion_transfer_assets_manifest)
        transfer_assets = json.loads(transfer_path.read_text())
        transfer_manifest_path = transfer_path.parent / 'manifest.json'
        transfer_manifest = json.loads(transfer_manifest_path.read_text())
        assert transfer_manifest['status'] == 'final'
        assert transfer_assets['analysis_manifest_sha256'] == sha(transfer_manifest_path)
        for name, digest in transfer_manifest['outputs'].items():
            assert sha(transfer_path.parent / name) == digest, name
        assert transfer_assets['legacy_incremental_sha256'] == sha(ROOT / 'analysis/outputs/tables/incremental_validity.csv')
        allowed = {'tables/criterion_transfer_counts.tex', 'tables/criterion_transfer_mental_health.tex',
                   'tables/criterion_transfer_education.tex', 'tables/criterion_transfer_health.tex',
                   'tables/criterion_transfer_contrasts.tex', 'tables/measurement_bridge.tex',
                   'tables/criterion_transfer_baselines.tex'}
        assert set(transfer_assets['files']) == allowed
        for name, digest in transfer_assets['files'].items():
            assert sha(DEST / name) == digest, name
            additions[name] = digest
        expected |= set(transfer_assets['files'])
        manifest['criterion_transfer_manifest_sha256'] = sha(transfer_manifest_path)
    actual = {str(p.relative_to(DEST)) for p in DEST.rglob('*')
              if p.is_file() and p.name != 'package_manifest.json'}
    assert actual == expected, 'Unexpected package files; inspect before release'
    presentation_changes = []
    old_release = ROOT / manifest['release_archive']
    for relative, digest in manifest['files'].items():
        if relative not in {'main.tex', 'README.md', 'references.bib', 'AUTHOR_CHECKLIST.md'}:
            if sha(DEST / relative) == digest:
                continue
            assert args.presentation_updates, f'Frozen asset changed: {relative}'
            if relative.startswith('tables/') and relative.endswith('.tex'):
                with zipfile.ZipFile(old_release) as archive:
                    old_bytes = archive.read(relative)
                import hashlib
                assert hashlib.sha256(old_bytes).hexdigest() == digest
                assert same_table_evidence(old_bytes, (DEST / relative).read_bytes()), relative
            else:
                assert relative in {'figures/paired_summary.pdf', 'figures/paired_summary.png'}, relative
            presentation_changes.append(relative)
    if any(name.startswith('figures/') for name in presentation_changes):
        from facct.paper import build_allocation_assets
        original_dest = build_allocation_assets.DEST
        try:
            with tempfile.TemporaryDirectory() as directory:
                build_allocation_assets.DEST = Path(directory)
                (Path(directory) / 'figures').mkdir()
                build_allocation_assets.figures()
                for relative in presentation_changes:
                    if relative.startswith('figures/'):
                        assert (Path(directory) / relative).read_bytes() == (DEST / relative).read_bytes()
        finally:
            build_allocation_assets.DEST = original_dest
    for relative, key in [('facct/outputs/tables/screening.csv', 'screening_table_sha256'),
                          ('facct/conditional/outputs/manifest.json', 'conditional_manifest_sha256')]:
        assert sha(ROOT / relative) == manifest[key], f'Analysis changed: {relative}'

    checks = validate()
    checks['compilation'] = f'{args.revision_date}: saved main.tex checked with the desktop editor compiler'
    checks['page_count'] = 'Unverified without a matching rendered layout report'
    if args.layout_report:
        with open(args.layout_report) as stream:
            layout = json.load(stream)
        assert layout['source_sha256'] == sha(DEST / 'main.tex'), 'Layout source is stale'
        assert layout['bibliography_sha256'] == sha(DEST / 'references.bib'), 'Layout bibliography is stale'
        assert layout['class_sha256'] == sha(DEST / 'acmart.cls'), 'Layout class is stale'
        assert layout['within_main_limit'] and layout['within_endmatter_limit'], 'Rendered draft exceeds limits'
        checks['page_count'] = layout
    manifest['checks'] = checks
    manifest['text_revision'] = {
        'date': args.revision_date.isoformat(),
        'scope': args.revision_scope,
        'new_sensitivity_analysis': bool(additions),
        'verified_presentation_changes': presentation_changes,
    }
    if args.additional_assets_manifest:
        manifest['professor_revision_manifest_sha256'] = asset_manifest['analysis_manifest_sha256']
    manifest['files'] = {relative: sha(DEST / relative) for relative in sorted(actual)}
    manifest['release_archive'] = 'facct/releases/' + args.release_name + '.zip'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')

    release = ROOT / manifest['release_archive']
    with zipfile.ZipFile(release, 'w', zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(actual | {'package_manifest.json'}):
            info = zipfile.ZipInfo(relative, date_time=(args.revision_date.year, args.revision_date.month, args.revision_date.day, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (DEST / relative).read_bytes())
    with zipfile.ZipFile(release) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == actual | {'package_manifest.json'}
        for relative in archive.namelist():
            assert archive.read(relative) == (DEST / relative).read_bytes()
    folder = release.with_suffix('')
    for relative in sorted(actual | {'package_manifest.json'}):
        target = folder / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DEST / relative, target)
    print(json.dumps({'zip': str(release), 'files': len(actual) + 1, **checks}, indent=2))


if __name__ == '__main__':
    main()
