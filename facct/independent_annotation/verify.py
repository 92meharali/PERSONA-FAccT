"""Independent standard-library check of resolution, original queues and tables."""
import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(output, compare=None):
    manifest = json.loads((output / "manifest.json").read_text())
    source = Path(manifest["source"])
    checks = []
    for rel, digest in manifest["source_hashes"].items():
        assert sha(source / rel) == digest, f"Source changed: {rel}"
    for rel, digest in manifest["protected_repo_hashes"].items():
        assert sha(ROOT / rel) == digest, f"Protected input changed: {rel}"
    for rel, digest in manifest["code_hashes"].items():
        assert sha(ROOT / rel) == digest, f"Implementation changed: {rel}"
    for rel, digest in manifest["output_hashes"].items():
        assert sha(output / rel) == digest, f"Output changed: {rel}"
    checks.append("All recorded source, implementation and output hashes match")
    paths = ["resolved/raw_ratings_ANNOTATOR_V1.csv", "assessor_B/returns/rating_sheet_ANNOTATOR_B_completed.csv",
             "assessor_C/returns/rating_sheet_ANNOTATOR_C_completed.csv"]
    ratings = [{r["study_id"]: r["rating"] for r in read(source / path)} for path in paths]
    convert = {"0": 0, "1": 0, "2": 1, "3": 1, "U": -1, "": -1}
    reconstructed = {}
    for sid in ratings[0]:
        votes = [convert[r[sid]] for r in ratings if sid in r]
        reconstructed[sid] = 1 if votes.count(1) >= 2 else 0 if votes.count(0) >= 2 else -1
    for row in read(output / "resolved_labels.csv"):
        assert int(row["resolved"]) == reconstructed[row["study_id"]]
    checks.append("Majority resolution independently reconstructed from assessor returns")
    frame = read(source / "frame/immutable_frame.csv")
    sid_by_original = {r["annotation_item_id"]: r["study_id"] for r in frame}
    corpus = [r for r in read(ROOT / "analysis/processed/persona_all.csv") if r["domain"] == "mental_health"]
    markers = set("i me my mine myself we us our ours ourselves you your yours yourself yourselves hello hi hey thanks thank welcome sorry please".split())
    for r in corpus:
        tokens = re.findall(r"\b\w+\b", r["response"].lower())
        r["scores"] = {"HumT": float(r["H"]), "length_words": len(tokens),
                       "markers_normalized": sum(t in markers for t in tokens)/len(tokens) if tokens else 0}
        stable_id = "mental_health:" + r["annotation_item_id"]
        r["tie"] = int.from_bytes(hashlib.sha256(f"{manifest['original_policy_seed']}|{stable_id}".encode()).digest()[:8], "big")
    targets = {}
    for sid in reconstructed:
        a, b = convert[ratings[0][sid]], convert[ratings[1][sid]]
        targets[sid] = {"A": a, "B": b, "resolved_ABC": reconstructed[sid],
                        "AB_union": max(a,b) if a >= 0 and b >= 0 else -1,
                        "AB_intersection": min(a,b) if a >= 0 and b >= 0 else -1,
                        "A_severity3": int(ratings[0][sid] == "3") if a >= 0 else -1,
                        "B_severity3": int(ratings[1][sid] == "3") if b >= 0 else -1}
    selections = read(output / "policy_selections.csv")
    points_checked = 0
    for row in read(output / "policy_metrics.csv"):
        if row["family"] != "original":
            continue
        target, policy, budget = row["target"], row["policy"], float(row["budget"])
        k = math.floor(len(corpus)*budget+1e-12)
        positive = {sid for sid,t in targets.items() if t[target] == 1}
        unknown = {sid for sid,t in targets.items() if t[target] < 0}
        if policy == "random_expected":
            caught = k*len(positive)/len(corpus) if not unknown else float("nan")
        else:
            ordered = sorted(corpus, key=lambda r: (-r["scores"][policy],r["tie"]))
            selected = {sid_by_original[r["annotation_item_id"]] for r in ordered[:k]}
            saved = {r["study_id"] for r in selections if r["policy"] == policy and float(r["budget"]) == budget}
            assert selected == saved, f"Selection mismatch {policy} {budget}"
            caught = len(selected & positive)
        assert int(row["selected"]) == k
        assert int(row["positives"]) == len(positive)
        for key,value in (("caught",caught), ("recall",caught/len(positive) if positive and not unknown else float("nan")),
                          ("precision",caught/k if k and not unknown else float("nan"))):
            actual = float(row[key]) if row[key] else float("nan")
            assert (math.isnan(value) and math.isnan(actual)) or math.isclose(actual,value,rel_tol=1e-10,abs_tol=1e-10), (key,row)
        points_checked += 1
    checks.append(f"{points_checked} original-policy target/budget cells independently verified")
    compared = []
    if compare:
        for p in sorted(output.glob("*.csv")) + [output / "agreement.json"]:
            assert sha(p) == sha(compare / p.name), f"Rerun differs: {p.name}"
            compared.append(p.name)
        checks.append(f"{len(compared)} numerical files byte-identical in independent rerun")
    return dict(status="pass", checks=checks, source_file_count=len(manifest["source_hashes"]),
                numerical_files_compared=compared)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "facct/independent_annotation/outputs")
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.output, args.compare), indent=2))
