"""Prepare a label-blind relevance sample, not capability-conditioned ground truth."""
import argparse
import hashlib
import json
import platform
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "analysis/processed/persona_all.csv"
SEED = 20261023


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(source, output, count=60, seed=SEED):
    source, output = Path(source).resolve(), Path(output).resolve()
    if count < 1:
        raise ValueError("Sample size must be positive")
    if output.exists():
        raise ValueError("Use a new output directory; existing samples are immutable")
    before = digest(source)
    frame = pd.read_csv(source, dtype=str, keep_default_na=False)
    # Whitelisting excludes old ratings, model identity, conditions and all scores.
    frame = frame[["domain", "annotation_item_id", "prompt_id", "prompt", "response"]]
    frame = frame[frame.domain == "mental_health"].copy()
    if frame.empty or (frame == "").any().any():
        raise ValueError("Missing required mental-health source fields")
    if frame.annotation_item_id.duplicated().any():
        raise ValueError("Source response IDs must be unique")
    frame["sample_key"] = [hashlib.sha256(f"{seed}|{v}".encode()).hexdigest()
                           for v in frame.annotation_item_id]
    # One response per prompt avoids treating paraphrases/endpoints as new prompts.
    frame = frame.sort_values("sample_key").drop_duplicates("prompt_id")
    if count > len(frame):
        raise ValueError("Requested more unique prompts than available")
    frame = frame.head(count).copy()
    frame["base_id"] = [f"CAP-{i:03d}" for i in range(1, count + 1)]
    private = frame[["base_id", "domain", "annotation_item_id", "prompt_id"]].copy()
    candidates = frame[["base_id", "prompt", "response"]].copy()
    candidates["candidate_status"] = "unassessed_relevance_sample"
    output.mkdir(parents=True)
    candidates.to_csv(output / "candidates.csv", index=False)
    private.to_csv(output / "source_map.csv", index=False)
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    assert digest(source) == before, "Source changed during preparation"
    manifest = {
        "status": "PREPARATION_ONLY_NOT_ANNOTATION_OR_NEW_EXPERIMENT",
        "source_sha256": before, "git_revision": revision,
        "seed": seed, "sample_count": count, "unique_prompts": count,
        "selection": "hash-order mental-health responses, one per prompt; no labels/scores",
        "interpretation": "Existing-text relevance sample, not new generated responses or a final benchmark",
        "python": platform.python_version(), "pandas": pd.__version__,
        "code_sha256": digest(__file__),
        "outputs": {p.name: digest(p) for p in output.glob("*.csv")},
        "blocked_on": ["case/dossier design and evidence", "protocol freeze",
                       "ethics scope and recruitment", "new independent judgments", "screen scores"],
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, default=60)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output, args.count, args.seed), indent=2))


if __name__ == "__main__":
    main()
