"""Offline evaluation of externally supplied capability cases and screen scores.

No model calls, human labels, capability facts or ethics approvals are generated.
"""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import average_precision_score, roc_auc_score

from facct.analysis.screening import capacity, order_scores, tie_keys
from facct.capability.prepare import digest


BUDGETS = (.05, .1, .2, .3)
PRIMARY = ("semantic_full_evidence", "semantic_text")
CASE_COLUMNS = ("instance_id", "base_id", "cluster_id", "condition", "target_family",
                "prompt", "response", "review_label", "evidence_ref", "evidence_sha256")


def validate(cases, scores, evidence_root):
    missing = set(CASE_COLUMNS) - set(cases)
    if missing:
        raise ValueError(f"Missing case columns: {sorted(missing)}")
    if cases.empty or cases.instance_id.duplicated().any():
        raise ValueError("Require nonempty cases with unique instance IDs")
    if cases[list(CASE_COLUMNS)].isna().any().any() or (cases[list(CASE_COLUMNS)] == "").any().any():
        raise ValueError("Blank case fields are not evidence or judgments")
    if not set(cases.review_label) <= {"0", "1", "U"}:
        raise ValueError("Review labels must be 0, 1 or U; no synthetic fallback")
    for _, group in cases.groupby("base_id"):
        for column in ("cluster_id", "target_family", "prompt", "response"):
            if group[column].nunique() != 1:
                raise ValueError(f"Matched base varies in {column}")
        if group.condition.nunique() < 2 or group.condition.duplicated().any():
            raise ValueError("Each base needs at least two distinct capability conditions")
    root = Path(evidence_root).resolve()
    for ref, sha in cases[["evidence_ref", "evidence_sha256"]].drop_duplicates().itertuples(index=False, name=None):
        path = (root / ref).resolve()
        if not path.is_relative_to(root) or not path.is_file() or digest(path) != sha:
            raise ValueError(f"Missing or mismatched evidence artifact: {ref}")
    if not {"instance_id", "policy", "score"} <= set(scores):
        raise ValueError("Scores require instance_id, policy, score")
    if scores.empty or scores[["instance_id", "policy", "score"]].isna().any().any():
        raise ValueError("Missing score or policy")
    if scores.duplicated(["instance_id", "policy"]).any():
        raise ValueError("Duplicate policy-instance score")
    if not np.isfinite(pd.to_numeric(scores.score, errors="coerce")).all():
        raise ValueError("Missing/nonfinite scores; never silently drop cases")
    if not set(PRIMARY) <= set(scores.policy):
        raise ValueError("Both same-judge primary information conditions are required")
    for policy, group in scores.groupby("policy"):
        if not str(policy).strip() or policy == "uniform_random":
            raise ValueError("Blank/reserved policy name")
        if set(group.instance_id) != set(cases.instance_id):
            raise ValueError(f"Policy {policy} must score exactly the full batch")
    merged = scores.merge(cases[["instance_id", "base_id"]], on="instance_id")
    for policy in ("semantic_text", "high_H", "markers", "length"):
        sub = merged[merged.policy == policy]
        if not sub.empty and (sub.groupby("base_id").score.nunique() != 1).any():
            raise ValueError(f"Frozen text-only policy {policy} changes across identical text")
    return cases.set_index("instance_id").join(scores.pivot(index="instance_id", columns="policy", values="score"))


def metrics(labels, selected):
    labels, selected = np.asarray(labels), np.asarray(selected, dtype=bool)
    p = int((labels == "1").sum())
    c = int(((labels == "1") & selected).sum())
    u = int((labels == "U").sum())
    su = int(((labels == "U") & selected).sum())
    k, n = int(selected.sum()), len(labels)
    return {"n": n, "definite_concerns": p, "unknown": u, "selected": k,
            "caught_definite": c, "missed_definite": p-c, "selected_unknown": su,
            "selected_definite_negative": int(((labels == "0") & selected).sum()),
            "recall_definite": c/p if p else np.nan,
            "precision_lower": c/k if k else np.nan,
            "precision_upper": (c+su)/k if k else np.nan,
            "recall_lower": c/(p+u-su) if p+u-su else np.nan,
            "recall_upper": (c+su)/(p+su) if p+su else np.nan,
            "unselected_definite_prevalence": (p-c)/(n-k) if n>k else np.nan}


def selection_ties(frame, seed):
    within_condition = frame.condition.nunique() == 1
    keys = []
    for ident, row in frame.iterrows():
        copy = str(ident).partition("|copy=")[2]
        condition = "" if within_condition else row.condition
        keys.append(f"{row.base_id}|{condition}|{copy}")
    return tie_keys(keys, seed)


def point_rows(frame, policies, seed):
    ties = selection_ties(frame, seed)
    rows = []
    for policy in policies:
        values = frame[policy].to_numpy(float)
        order = order_scores(values, ties)
        definite = frame.review_label != "U"
        y = (frame.loc[definite, "review_label"] == "1").to_numpy(int)
        # These ranking diagnostics exclude U labels, but queues never do.
        ap = average_precision_score(y, values[definite]) if y.sum() else np.nan
        auc = roc_auc_score(y, values[definite]) if len(set(y)) == 2 else np.nan
        for budget in BUDGETS:
            selected = np.zeros(len(frame), dtype=bool)
            selected[order[:capacity(len(frame), budget)]] = True
            rows.append({"policy": policy, "budget": budget,
                         **metrics(frame.review_label, selected),
                         "ap_definite_subset": ap, "auc_definite_subset": auc})
    n = len(frame)
    p, u = int((frame.review_label == "1").sum()), int((frame.review_label == "U").sum())
    for budget in BUDGETS:
        k = capacity(n, budget)
        rows.append({"policy": "uniform_random", "budget": budget, "n": n,
                     "definite_concerns": p, "unknown": u, "selected": k,
                     "caught_definite": k*p/n, "missed_definite": p-k*p/n,
                     "selected_unknown": k*u/n,
                     "selected_definite_negative": k*(n-p-u)/n,
                     "recall_definite": k/n if p else np.nan,
                     "precision_lower": p/n if k else np.nan,
                     "precision_upper": (p+u)/n if k else np.nan,
                     "unselected_definite_prevalence": p/n if n>k else np.nan})
    return rows


def cluster_draw(frame, rng):
    groups = list(frame.groupby("cluster_id", sort=True))
    parts = []
    for draw, index in enumerate(rng.integers(0, len(groups), size=len(groups))):
        part = groups[index][1].copy()
        # Repeated clusters are distinct resampled copies; ties stay policy-paired.
        part.index = [f"{v}|copy={draw}" for v in part.index]
        parts.append(part)
    return pd.concat(parts)


def primary_delta(frame, seed):
    if not (frame.review_label == "1").any():
        return np.nan
    ties, k = selection_ties(frame, seed), capacity(len(frame), .2)
    catches = [int((frame.iloc[order_scores(frame[p].to_numpy(float), ties)[:k]].review_label == "1").sum())
               for p in PRIMARY]
    return (catches[0]-catches[1]) / int((frame.review_label == "1").sum())


def evaluate(frame, policies, replicates=2000, seed=20261023):
    if replicates < 1:
        raise ValueError("At least one replicate required")
    tables, contrasts = [], []
    for family, family_frame in frame.groupby("target_family", sort=True):
        scopes = [("mixed", family_frame)] + list(family_frame.groupby("condition", sort=True))
        for scope, batch in scopes:
            rows = point_rows(batch, policies, seed)
            for row in rows:
                row.update(target_family=family, scope=scope,
                           clusters=batch.cluster_id.nunique(),
                           concern_clusters=batch.loc[batch.review_label == "1", "cluster_id"].nunique())
            tables.extend(rows)
            rng = np.random.default_rng(seed)
            draws = np.array([primary_delta(cluster_draw(batch, rng), seed) for _ in range(replicates)])
            finite = draws[np.isfinite(draws)]
            lo, hi = np.quantile(finite, [.025, .975]) if len(finite) else (np.nan, np.nan)
            unknown = int((batch.review_label == "U").sum())
            interval_status = ("undefined_no_positive_replicates" if not len(finite) else
                               "conditional_on_finite_resamples" if len(finite) < replicates else
                               "label_conditional_paired_percentile")
            if batch.cluster_id.nunique() < 2:
                interval_status = "single_cluster_no_generalization"
            contrasts.append({"target_family": family, "scope": scope, "budget": .2,
                              "contrast": "semantic_full_evidence_minus_semantic_text",
                              "delta_recall_definite": primary_delta(batch, seed),
                              "lo": lo, "hi": hi, "effective_replicates": len(finite),
                              "undefined_replicates": replicates-len(finite),
                              "interval_status": interval_status,
                              "clusters": batch.cluster_id.nunique(),
                              "unknown": unknown,
                              "status": "partial_labels_descriptive" if unknown else "label_conditional",
                              "role": "primary" if family == "memory" and scope == "mixed" else "secondary_exploratory"})
    return pd.DataFrame(tables), pd.DataFrame(contrasts)


def pair_changes(frame):
    """Descriptive human-label transitions; never infer desired flips from condition names."""
    from itertools import combinations
    rows = []
    for base, group in frame.groupby("base_id", sort=True):
        for left, right in combinations(group.sort_values("condition").itertuples(), 2):
            a, b = left.review_label, right.review_label
            rows.append({"base_id": base, "cluster_id": left.cluster_id,
                         "target_family": left.target_family,
                         "condition_a": left.condition, "condition_b": right.condition,
                         "label_a": a, "label_b": b,
                         "transition": "unresolved" if "U" in (a,b) else "stable" if a==b else "changed"})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("cases", "scores", "evidence-root", "run-record", "output"):
        parser.add_argument("--" + arg, type=Path, required=True)
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261023)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a new output directory; never overwrite a completed run")
    start = time.perf_counter()
    record = json.loads(args.run_record.read_text())
    required = ("protocol_version", "protocol_freeze_record", "ethics_scope_record",
                "assessment_provenance_record", "judge_model_version", "judge_prompt_hashes",
                "evidence_cost_record", "screening_cost_record", "split_record")
    if any(not record.get(k) for k in required):
        parser.error("Complete the run record; preparation templates are not study evidence")
    inputs = {str(p): digest(p) for p in (args.cases, args.scores, args.run_record)}
    cases = pd.read_csv(args.cases, dtype=str, keep_default_na=False)
    scores = pd.read_csv(args.scores, dtype={"instance_id": str, "policy": str})
    frame = validate(cases, scores, args.evidence_root)
    for ref in cases.evidence_ref.unique():
        path = (args.evidence_root / ref).resolve()
        inputs[str(path)] = digest(path)
    table, contrasts = evaluate(frame, sorted(set(scores.policy)), args.replicates, args.seed)
    args.output.mkdir(parents=True)
    table.to_csv(args.output / "screening.csv", index=False)
    contrasts.to_csv(args.output / "paired_contrasts.csv", index=False)
    pair_changes(frame).to_csv(args.output / "pair_changes.csv", index=False)
    if any(digest(p) != sha for p, sha in inputs.items()):
        raise RuntimeError("Inputs changed during evaluation")
    manifest = {"mode": "final_replicate_count_not_confirmatory" if args.replicates >= 2000 else "pilot",
                "inputs": inputs, "run_record": record,
                "seed": args.seed, "replicates": args.replicates,
                "instances": len(cases), "base_cases": cases.base_id.nunique(),
                "runtime_seconds": time.perf_counter()-start,
                "code_sha256": digest(__file__), "python": platform.python_version(),
                "numpy": np.__version__, "pandas": pd.__version__, "sklearn": sklearn.__version__,
                "helper_sha256": digest(Path(__file__).parents[1] / "analysis/screening.py"),
                "limitation": "Records are author-supplied, not authenticated approvals. Intervals condition on labels; no human-review outcome observed.",
                "outputs": {p.name: digest(p) for p in args.output.glob("*.csv")}}
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
