"""Package the completed-evidence revision without regenerating analytical assets."""
import argparse
import json
import shutil
import zipfile

from facct.paper.build_overleaf import DEST, ROOT, sha, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--layout-report', type=str)
    parser.add_argument('--release-name', default='PERSONA_FAccT_Overleaf_2026-10-24_review')
    args = parser.parse_args()
    if not args.release_name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.release_name):
        parser.error('release-name must be a simple file stem')
    manifest_path = DEST / 'package_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    expected = set(manifest['files'])
    actual = {str(p.relative_to(DEST)) for p in DEST.rglob('*')
              if p.is_file() and p.name != 'package_manifest.json'}
    assert actual == expected, 'Unexpected package files; inspect before release'
    for relative, digest in manifest['files'].items():
        if relative not in {'main.tex', 'README.md', 'references.bib', 'AUTHOR_CHECKLIST.md'}:
            assert sha(DEST / relative) == digest, f'Frozen asset changed: {relative}'

    checks = validate()
    checks['compilation'] = '2026-10-24: saved main.tex successfully compiled with the desktop editor compiler'
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
        'date': '2026-10-24',
        'scope': 'Review-driven clarity revision; a non-independent in-chat semantic pass is documented outside the manuscript; manuscript numerical evidence unchanged',
        'completed_new_experiments': False,
    }
    manifest['files'] = {relative: sha(DEST / relative) for relative in sorted(actual)}
    manifest['release_archive'] = 'facct/releases/' + args.release_name + '.zip'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')

    release = ROOT / manifest['release_archive']
    with zipfile.ZipFile(release, 'w', zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(actual | {'package_manifest.json'}):
            info = zipfile.ZipInfo(relative, date_time=(2026, 10, 24, 0, 0, 0))
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
