"""Import the verified release, excluding private inputs and local build files."""
import argparse
import json
import shutil
from pathlib import Path
from zipfile import ZipFile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    root = Path(__file__).resolve().parents[1]
    target = root / "facct/concern_detector_eval"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("analysis", "tests", "notes"):
        shutil.copytree(source / name, target / name, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name in ("README.md", "requirements.txt", "RESPONSE_TO_REVIEWERS.md"):
        shutil.copy2(source / name, target / name)
    for path in (source / "analysis_outputs").rglob("*"):
        if not path.is_file() or path.suffix not in {".csv", ".npy", ".json", ".png"}:
            continue
        destination = target / path.relative_to(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if path.name == "manifest.json" and path.parent.name == "professor_revision":
            manifest = json.loads(path.read_text())
            manifest["input_hashes"] = {
                ("private-input/immutable_frame.csv" if "immutable_frame.csv" in k
                 else "repository/" + k.split("/PERSONA-FAccT/", 1)[1]
                 if "/PERSONA-FAccT/" in k else k): v
                for k, v in manifest["input_hashes"].items()
            }
            manifest["publication_note"] = "Local input paths replaced by logical names; source hashes and results unchanged. Private frame is not distributed."
            destination.write_text(json.dumps(manifest, indent=2) + "\n")
        else:
            shutil.copy2(path, destination)
    archive = source / "releases/PERSONA_FAccT_Professor_Revision_2026-11-03.zip"
    with ZipFile(archive) as z:
        assert z.testzip() is None
        for member in z.infolist():
            assert not Path(member.filename).is_absolute() and ".." not in Path(member.filename).parts
        # Keep the analysis package runnable and mirror its exact compiled release
        # at the established manuscript location. Historical files are not deleted.
        z.extractall(target / "paper")
        z.extractall(root / "facct/paper/overleaf")
    release = root / "facct/releases" / archive.name
    release.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(archive, release)
    print("Imported release and analysis; source ratings and private study records untouched.")


if __name__ == "__main__":
    main()
