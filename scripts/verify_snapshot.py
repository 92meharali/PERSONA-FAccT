"""Check the immutable file baseline copied into this research snapshot."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / "SNAPSHOT_MANIFEST.json").read_text())
    failures = []
    for name, expected in manifest["files"].items():
        path = ROOT / name
        if not path.is_file():
            failures.append(f"Missing: {name}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            failures.append(f"Changed: {name}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Verified {len(manifest['files'])} copied research files.")


if __name__ == "__main__":
    main()
