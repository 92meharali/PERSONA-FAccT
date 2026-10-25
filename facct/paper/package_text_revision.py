"""Package the completed-evidence revision without regenerating analytical assets."""
import argparse
import json
import shutil
import zipfile
from datetime import date
from pathlib import Path

from facct.paper.build_overleaf import DEST, ROOT, sha, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout-report', type=str)
    parser.add_argument('--release-name', default='PERSONA_FAccT_Overleaf_2026-10-24_review')
    parser.add_argument('--revision-date', default='2026-10-24', type=date.fromisoformat)
    parser.add_argument('--revision-scope', default='Review-driven clarity revision; numerical evidence unchanged')
    parser.add_argument('--additional-assets-manifest', type=str)
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
    actual = {str(p.relative_to(DEST)) for p in DEST.rglob('*')
              if p.is_file() and p.name != 'package_manifest.json'}
    assert actual == expected, 'Unexpected package files; inspect before release'
    for relative, digest in manifest['files'].items():
        if relative not in {'main.tex', 'README.md', 'references.bib', 'AUTHOR_CHECKLIST.md'}:
            assert sha(DEST / relative) == digest, f'Frozen asset changed: {relative}'

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
    }
    if additions:
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
