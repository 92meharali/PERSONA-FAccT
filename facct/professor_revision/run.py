"""Reproduce October 26 sensitivity; never mutate source scores or labels."""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import time

import numpy as np
import pandas as pd

from facct.analysis.screening import capacity, features, order_scores, tie_keys
from facct.analysis.uncertainty import draw_indices, summarize
from facct.analysis.validate_inputs import sha, source_hashes

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name("outputs")
DOMAINS = ("mental_health", "education", "health")
POLICIES = ("HumT", "markers_full", "markers_300", "length_full", "length_300", "random_expected")
BUDGETS = (.05, .10, .20, .30)
PAIRS = ((0, 1), (0, 2), (2, 1), (0, 5))
POLICY_SEED = 20261002


def score_matrix(frame):
    full = features(frame)
    short = frame[["response", "H"]].copy()
    short["response"] = short.response.str[:300]
    prefix = features(short)
    return np.column_stack((full[:, 0], full[:, 2], prefix[:, 2], full[:, 1], prefix[:, 1]))


def targets(frame):
    result = {"D_ge3": frame.D.to_numpy() >= 3,
              "D_gt3": frame.D.to_numpy() > 3,
              "D_ge4": frame.D.to_numpy() >= 4,
              "F_lt4": frame.F.to_numpy() < 4,
              "OA_lt4": frame.OA.to_numpy() < 4}
    if "followup" in frame and frame.followup.notna().all():
        result["followup"] = frame.followup.to_numpy().astype(bool)
    return list(result), np.column_stack(list(result.values()))


def catches(scores, y, ties):
    n = len(y)
    if not n:
        raise ValueError("Empty review batch")
    if not np.isfinite(scores).all():
        raise ValueError("Missing score")
    result = np.empty((len(BUDGETS), y.shape[1], len(POLICIES)))
    for j in range(scores.shape[1]):
        order = order_scores(scores[:, j], ties)
        for b, budget in enumerate(BUDGETS):
            result[b, :, j] = y[order[:capacity(n, budget)]].sum(axis=0)
    for b, budget in enumerate(BUDGETS):
        result[b, :, -1] = capacity(n, budget) * y.mean(axis=0)
    return result


def recall(caught, positives):
    return np.divide(caught, positives[None, :, None],
                     out=np.full(caught.shape, np.nan), where=positives[None, :, None] > 0)


def analyze(frame, replicates, seed):
    names, y = targets(frame)
    scores = score_matrix(frame)
    ids, domains, clusters = (frame[c].to_numpy() for c in ("id", "domain", "cluster"))
    point = catches(scores, y, tie_keys(ids, POLICY_SEED))
    p = y.sum(axis=0)
    r = recall(point, p)
    samples = np.empty((replicates, *r.shape))
    rng = np.random.default_rng(seed)
    for b in range(replicates):
        idx, copies = draw_indices(domains, clusters, rng)
        ties = tie_keys([f"{item}|{copy}" for item, copy in zip(ids[idx], copies)], POLICY_SEED)
        samples[b] = recall(catches(scores[idx], y[idx], ties), y[idx].sum(axis=0))
    records, contrasts = [], []
    for b, budget in enumerate(BUDGETS):
        k, n = capacity(len(frame), budget), len(frame)
        for j, criterion in enumerate(names):
            pc, nc = len(set(clusters[y[:, j]])), len(set(clusters[~y[:, j]]))
            shared = dict(domain=domains[0], criterion=criterion, budget=budget, n=n,
                          selected=k, concerns=int(p[j]), concern_clusters=pc,
                          nonconcern_clusters=nc, sparse=min(pc, nc) < 10,
                          replicates=replicates, interval="exploratory pointwise 95%")
            for i, policy in enumerate(POLICIES):
                lo, hi, valid = summarize(samples[:, b, j, i])
                c = point[b, j, i]
                records.append(dict(**shared, policy=policy, caught=c, recall=r[b, j, i],
                                    precision=c/k if k else np.nan, missed=p[j]-c,
                                    unselected_prevalence=(p[j]-c)/(n-k) if n > k else np.nan,
                                    recall_lo=lo, recall_hi=hi, finite_replicates=valid))
            for a, z in PAIRS:
                lo, hi, valid = summarize(samples[:, b, j, a] - samples[:, b, j, z])
                contrasts.append(dict(**shared, policy_a=POLICIES[a], policy_b=POLICIES[z],
                                      recall_difference=r[b, j, a]-r[b, j, z], lo=lo, hi=hi,
                                      finite_replicates=valid))
    return pd.DataFrame(records), pd.DataFrame(contrasts)


def load_frame():
    frame = pd.read_csv(ROOT / "analysis/processed/persona_all.csv")
    frame["id"] = frame.domain + ":" + frame.annotation_item_id
    frame["cluster"] = frame.domain + ":" + frame.prompt_id
    assert frame.id.is_unique and not frame.response.isna().any()
    # Resolve through the authenticated supplied ID map, never through row order.
    manifest = json.loads((ROOT / "facct/independent_annotation/outputs/manifest.json").read_text())
    mapping_path = Path(manifest["source"]) / "frame/immutable_frame.csv"
    assert sha(mapping_path) == manifest["source_hashes"]["frame/immutable_frame.csv"]
    mapping = pd.read_csv(mapping_path, usecols=["study_id", "annotation_item_id"])
    assert mapping.study_id.is_unique and mapping.annotation_item_id.is_unique
    labels_path = ROOT / "facct/independent_annotation/outputs/resolved_labels.csv"
    assert sha(labels_path) == manifest["output_hashes"]["resolved_labels.csv"]
    followup = pd.read_csv(labels_path)
    joined = mapping.merge(followup, on="study_id", validate="one_to_one")
    assert len(joined) == 660 and joined.resolved.sum() == 19
    lookup = dict(zip(joined.annotation_item_id, joined.resolved))
    frame["followup"] = np.nan
    mh = frame.domain == "mental_health"
    frame.loc[mh, "followup"] = frame.loc[mh, "annotation_item_id"].map(lookup)
    assert frame.loc[mh, "followup"].notna().all()
    return frame, mapping_path


def exclusive_cases(frame, out):
    d = frame[frame.domain == "mental_health"].reset_index(drop=True)
    scores = score_matrix(d)
    keys = tie_keys(d.id, POLICY_SEED)
    masks = []
    for i in (0, 1):
        mask = np.zeros(len(d), dtype=bool)
        mask[order_scores(scores[:, i], keys)[:capacity(len(d), .2)]] = True
        masks.append(mask)
    h, m = masks
    selected = (d.D.to_numpy() >= 3) & (h ^ m)
    details = d.loc[selected, ["id", "annotation_item_id", "cluster", "condition", "scenario_type",
                              "model", "D", "F", "OA", "followup"]].copy()
    details["policy_only"] = np.where(h[selected], "HumT", "markers_full")
    details["case_id"] = details.id.map(lambda x: "CASE-" + hashlib.sha256(x.encode()).hexdigest()[:10])
    details["words"] = scores[selected, 3]
    details["marker_fraction"] = scores[selected, 1]
    details["characters"] = d.loc[selected, "response"].str.len().to_numpy()
    assert details.groupby("policy_only").size().to_dict() == {"HumT": 20, "markers_full": 41}
    details.to_csv(out / "exclusive_case_features.csv", index=False)
    rows = []
    for name, g in details.groupby("policy_only"):
        rows.append(dict(policy_only=name, n=len(g), clusters=g.cluster.nunique(),
                         D_eq3=int((g.D == 3).sum()), D_gt3=int((g.D > 3).sum()),
                         D_ge4=int((g.D >= 4).sum()), F_lt4=int((g.F < 4).sum()),
                         OA_lt4=int((g.OA < 4).sum()), followup=int(g.followup.sum()),
                         natural=int((g.condition == "natural").sum()),
                         median_words=g.words.median(), median_marker_fraction=g.marker_fraction.median()))
    pd.DataFrame(rows).to_csv(out / "exclusive_case_summary.csv", index=False)
    private = ROOT / "private/professor_revision_2026-10-26"
    private.mkdir(parents=True, exist_ok=True)
    blinded = details[["case_id", "id"]].merge(d[["id", "prompt", "response"]], on="id", validate="one_to_one")
    blinded = blinded.drop(columns="id").sort_values("case_id")
    blinded.to_csv(private / "cases_blinded.csv", index=False)
    details.to_csv(private / "case_key.csv", index=False)
    return pd.DataFrame(rows)


def report(performance, contrasts, cases, out):
    lines = ["# Professor-requested checks", "", "Exploratory amendment; 2,000 paired prompt-cluster draws. Original source ratings and scores are unchanged.", "",
             "## Counts at 20%", "", "| Domain | Criterion | Cases / prompts | H | Full markers | 300-character markers | Full length | 300-character length | Random expectation |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for (domain, criterion), g in performance[performance.budget == .2].groupby(["domain", "criterion"], sort=False):
        lookup = g.set_index("policy")
        r = g.iloc[0]
        cells = " | ".join(f"{lookup.loc[p, 'caught']:g}" for p in POLICIES)
        lines.append(f"| {domain} | {criterion} | {r.concerns} / {r.concern_clusters} | {cells} |")
    lines += ["", "## Paired recall differences at 20%", "", "| Domain | Criterion | Contrast | Difference, pp [95%] | Finite draws |", "|---|---|---|---:|---:|"]
    for r in contrasts[contrasts.budget == .2].itertuples():
        lines.append(f"| {r.domain} | {r.criterion} | {r.policy_a} minus {r.policy_b} | {100*r.recall_difference:+.1f} [{100*r.lo:+.1f}, {100*r.hi:+.1f}] | {r.finite_replicates}/{r.replicates} |")
    lines += ["", "## Exclusive original-queue cases", "", cases.to_string(index=False), "",
              "Case profiles reuse original ratings and resolved follow-up labels. They are not newly adjudicated meanings or independent semantic codes.", "",
              "The 300-character policies slice annotated text using the source scorer's documented Python operation. Historical scorer invocation is unauthenticated, especially where transfer export text differs. These checks test the available length restriction without proving full input equivalence."]
    (out / "findings.md").write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261026)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    if args.replicates < 2000 and args.output.resolve() == OUT.resolve():
        parser.error("Use a separate output for pilot runs")
    started = time.monotonic()
    before = source_hashes(ROOT)
    frame, map_path = load_frame()
    args.output.mkdir(parents=True, exist_ok=True)
    performance, contrasts = [], []
    for domain in DOMAINS:
        a, b = analyze(frame[frame.domain == domain].reset_index(drop=True), args.replicates, args.seed)
        performance.append(a)
        contrasts.append(b)
        print(f"Completed {domain}: {args.replicates} paired draws", flush=True)
    performance, contrasts = pd.concat(performance), pd.concat(contrasts)
    performance.to_csv(args.output / "performance.csv", index=False)
    contrasts.to_csv(args.output / "paired_contrasts.csv", index=False)
    cases = exclusive_cases(frame, args.output)
    report(performance, contrasts, cases, args.output)
    original = pd.read_csv(ROOT / "facct/outputs/tables/screening.csv")
    old_policies = {"HumT": "high_H", "markers_full": "markers", "length_full": "length"}
    for row in performance[performance.policy.isin(old_policies)].itertuples():
        if row.criterion in {"D_ge3", "F_lt4", "OA_lt4"}:
            old = original[(original.domain == row.domain) & (original.criterion == row.criterion)
                           & (original.policy == old_policies[row.policy]) & (original.budget == row.budget)].iloc[0]
            assert row.caught == old.caught and row.selected == old.selected
    assert source_hashes(ROOT) == before, "Source mutation"
    paths = [Path(__file__), Path(__file__).with_name("protocol.md"), map_path,
             ROOT / "facct/analysis/screening.py", ROOT / "facct/analysis/uncertainty.py",
             ROOT / "facct/independent_annotation/outputs/resolved_labels.csv"]
    manifest = dict(date="2026-10-26", seed=args.seed, policy_seed=POLICY_SEED,
                    replicates=args.replicates, status="final_exploratory" if args.replicates >= 2000 else "pilot",
                    command=f".venv/bin/python -m facct.professor_revision.run --replicates {args.replicates} --seed {args.seed}",
                    runtime_seconds=round(time.monotonic()-started, 2),
                    git_revision=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                    sources_unchanged=True, original_counts_reproduced=True,
                    software={k: importlib.metadata.version(k) for k in ("numpy", "pandas", "scipy")},
                    source_hashes=before, additional_input_hashes={str(p): sha(p) for p in paths},
                    output_hashes={p.name: sha(p) for p in args.output.iterdir() if p.suffix in {".csv", ".md"}})
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Completed in {manifest['runtime_seconds']} seconds", flush=True)


if __name__ == "__main__":
    main()
