"""Reconstruct supplied A/B/C judgments without editing the source package."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import shlex
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from facct.analysis.screening import capacity, features, order_scores, tie_keys
from facct.analysis.uncertainty import draw_indices

ROOT = Path(__file__).resolve().parents[1]
POLICIES = ("HumT", "length_words", "markers_normalized")
VALID = {"0", "1", "2", "3", "U", ""}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def tree_hashes(path):
    return {str(p.relative_to(path)): sha(p) for p in sorted(path.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store"}


def csv(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def keyed(frame, name):
    require("study_id" in frame and frame.study_id.ne("").all(), f"Missing IDs: {name}")
    require(not frame.study_id.duplicated().any(), f"Duplicate IDs: {name}")
    return frame.set_index("study_id", drop=False)


def binary(value):
    require(value in VALID, f"Invalid rating: {value!r}")
    return 1 if value in {"2", "3"} else 0 if value in {"0", "1"} else -1


def resolve(a, b, c=None):
    if a == b and a in (0, 1):
        return a, "A_B_agree"
    votes = [a, b] + ([] if c is None else [c])
    for label in (0, 1):
        if votes.count(label) >= 2:
            return label, "majority_yes_with_C" if label else "majority_no_with_C"
    return -1, "unresolved"


def agreement(a, b):
    definite = (a >= 0) & (b >= 0)
    x, y = a[definite], b[definite]
    n = len(x)
    yy, nn = int(((x == 1) & (y == 1)).sum()), int(((x == 0) & (y == 0)).sum())
    yn, ny = int(((x == 1) & (y == 0)).sum()), int(((x == 0) & (y == 1)).sum())
    observed = (yy + nn) / n if n else None
    expected = ((yy + yn) * (yy + ny) + (nn + ny) * (nn + yn)) / n**2 if n else None
    return dict(n=len(a), definite_pairs=n, unresolved_either=int((~definite).sum()),
                both_yes=yy, both_no=nn, A_yes_B_no=yn, A_no_B_yes=ny,
                raw_agreement=observed,
                kappa=(observed - expected) / (1 - expected) if n and expected < 1 else None,
                positive_agreement=2 * yy / (2 * yy + yn + ny) if 2 * yy + yn + ny else None,
                negative_agreement=2 * nn / (2 * nn + yn + ny) if 2 * nn + yn + ny else None)


def metric(y, selected, clusters):
    selected = np.asarray(selected, dtype=bool)
    n, k = len(y), int(selected.sum())
    p, u = int((y == 1).sum()), int((y < 0).sum())
    caught = int(((y == 1) & selected).sum())
    us, un = int(((y < 0) & selected).sum()), int(((y < 0) & ~selected).sum())
    return dict(n=n, positives=p, positive_clusters=len(set(clusters[y == 1])),
                unresolved=u, selected=k, caught=caught, missed=p-caught,
                unresolved_selected=us, unresolved_unselected=un,
                prevalence=p/n if n and not u else np.nan,
                recall=caught/p if p and not u else np.nan,
                precision=caught/k if k and not u else np.nan,
                unselected_prevalence=(p-caught)/(n-k) if n > k and not u else np.nan,
                recall_lower=caught/(p+un) if p+un else (1.0 if us else np.nan),
                recall_upper=(caught+us)/(p+us) if p+us else (0.0 if un else np.nan),
                precision_lower=caught/k if k else np.nan,
                precision_upper=(caught+us)/k if k else np.nan)


def expected_random(y, k, clusters):
    n, p, u = len(y), int((y == 1).sum()), int((y < 0).sum())
    return dict(n=n, positives=p, positive_clusters=len(set(clusters[y == 1])),
                unresolved=u, selected=k, caught=k*p/n if not u else np.nan,
                missed=(n-k)*p/n if not u else np.nan,
                prevalence=p/n if not u else np.nan,
                recall=k/n if p and not u else np.nan,
                precision=p/n if k and not u else np.nan,
                unselected_prevalence=p/n if n > k and not u else np.nan)


def read_ratings(source, returned, raw_pattern, ids, name):
    ratings = keyed(csv(source / returned), name)
    require(set(ratings.index) == set(ids), f"Incorrect coverage: {name}")
    require(ratings.rating.isin(VALID).all(), f"Invalid rating: {name}")
    require(ratings.assessor_id.nunique() == 1, f"Mixed assessor IDs: {name}")
    raw_rows = []
    for path in sorted(source.glob(raw_pattern)):
        raw_rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    require(bool(raw_rows), f"Missing raw records: {name}")
    raw = keyed(pd.DataFrame(raw_rows).fillna(""), name + " raw")
    require(set(raw.index) == set(ids), f"Raw coverage mismatch: {name}")
    for field in ("rating", "assessor_id", "packet_version", "rationale", "evidence_span"):
        require(np.array_equal(raw.loc[ratings.index, field].astype(str), ratings[field]),
                f"Raw/return mismatch: {name} {field}")
    require(ratings.rationale.ne("").all(), f"Missing rationale: {name}")
    require(ratings.loc[ratings.rating.isin(["2", "3"]), "evidence_span"].ne("").all(),
            f"Missing positive evidence: {name}")
    return ratings


def validate(source, root):
    frame = keyed(csv(source / "frame/immutable_frame.csv"), "frame").sort_index()
    require(len(frame) == 660 and frame.prompt_id.nunique() == 220, "Unexpected frame size")
    require(frame.groupby("prompt_id").size().eq(3).all(), "Incomplete prompt clusters")
    require(frame.groupby("prompt_id").model.nunique().eq(3).all(), "Repeated model within cluster")
    for col in ("prompt", "response"):
        hashes = frame[col].map(lambda s: hashlib.sha256(s.encode()).hexdigest())
        require(hashes.equals(frame[col + "_sha256"]), f"Frame hash mismatch: {col}")
    a = read_ratings(source, "resolved/raw_ratings_ANNOTATOR_V1.csv",
                     "raw_ratings/*.jsonl", frame.index, "A").loc[frame.index]
    b = read_ratings(source, "assessor_B/returns/rating_sheet_ANNOTATOR_B_completed.csv",
                     "assessor_B/raw_ratings/*.jsonl", frame.index, "B").loc[frame.index]
    ay, by = a.rating.map(binary).to_numpy(), b.rating.map(binary).to_numpy()
    disputes = (ay != by) | (ay < 0) | (by < 0)
    c = read_ratings(source, "assessor_C/returns/rating_sheet_ANNOTATOR_C_completed.csv",
                     "assessor_C/returns/*.jsonl", frame.index[disputes], "C")
    for name, r in (("B", b), ("C", c)):
        for col in ("prompt", "response"):
            require(r[col].equals(frame.loc[r.index, col]), f"Text mismatch {name} {col}")
        packet = csv(source / f"assessor_{name}/packet/rating_sheet_ANNOTATOR_{name}.csv")
        require(not {"rating_A", "rating_B", "humt_score", "model", "binary_A", "binary_B"}
                .intersection(packet.columns), f"Packet metadata leakage: {name}")
        require(packet.rating.eq("").all(), f"Distributed template contains ratings: {name}")
    notes = (source / "docs/capability_note.txt", source / "docs/capability_note_v1.0_2026-10-10_ANNOTATOR_V1.txt")
    require(sha(notes[0]) == sha(notes[1]), "A capability copies differ")
    archive = json.loads((source / "assessor_B/_steward_only/assessor_A_integrity_pre_B.json").read_text())
    for old_path, h in archive["sha256"].items():
        rel = old_path.split("/independent_annotation_study/", 1)[1]
        require(sha(source / rel) == h, f"Archived A file changed: {rel}")
    rows = []
    for i, sid in enumerate(frame.index):
        cy = binary(c.loc[sid, "rating"]) if sid in c.index else None
        outcome, route = resolve(ay[i], by[i], cy)
        rows.append(dict(study_id=sid, A=ay[i], B=by[i], C=cy,
                         resolved=outcome, route=route))
    resolved = pd.DataFrame(rows).set_index("study_id", drop=False)
    supplied = keyed(csv(source / "resolved/resolved_labels_ABC.csv"), "supplied ABC")
    require(set(supplied.index) == set(frame.index), "Supplied ABC coverage mismatch")
    reported = supplied.loc[frame.index, "resolved_binary"].map({"yes": 1, "no": 0, "unresolved": -1})
    require(np.array_equal(reported, resolved.resolved), "Incorrect supplied majority labels")
    original = csv(root / "analysis/processed/persona_all.csv")
    original = original[original.domain == "mental_health"].set_index("annotation_item_id")
    require(original.index.is_unique and set(original.index) == set(frame.annotation_item_id), "Original corpus ID mismatch")
    original = original.loc[frame.annotation_item_id].reset_index()
    encoding = {}
    for col in ("prompt", "response"):
        pairs = list(zip(frame[col], original[col]))
        require(all(x == y or x.encode("utf-8").decode("latin1") == y for x, y in pairs),
                f"Unexplained original/new {col} changes")
        encoding[col + "_encoding_only_differences"] = sum(x != y for x, y in pairs)
    require(np.allclose(frame.humt_score.astype(float), original.H.astype(float), rtol=0, atol=1e-12), "HumT changed")
    require(np.array_equal(frame.prompt_id, original.prompt_id), "Prompt clusters changed")
    original["H"] = original.H.astype(float)
    original["id"] = original.domain + ":" + original.annotation_item_id
    original["cluster"] = original.domain + ":" + original.prompt_id
    return frame, original, a, b, c, resolved, encoding


def point_tables(frame, original, targets, source, config):
    X, ids, clusters = features(original), original.id.to_numpy(), original.cluster.to_numpy()
    ties = tie_keys(ids, config["seed"])
    original_masks, rows, membership, queue_checks = {}, [], [], []
    for budget in config["budgets"]:
        k = capacity(len(frame), budget)
        for j, policy in enumerate(POLICIES):
            mask = np.zeros(len(frame), bool)
            mask[order_scores(X[:, j], ties)[:k]] = True
            original_masks[(budget, policy)] = mask
            for sid in frame.index[mask]:
                membership.append(dict(family="original", budget=budget, policy=policy, study_id=sid))
            for name, y in targets.items():
                rows.append(dict(family="original", target=name, policy=policy, budget=budget,
                                 **metric(y, mask, clusters)))
        for name, y in targets.items():
            rows.append(dict(family="original", target=name, policy="random_expected", budget=budget,
                             **expected_random(y, k, clusters)))
    imports = (("humt_top132", "HumT"), ("marker_top132", "markers_normalized"),
               ("length_top132", "length_words"), ("random_132", None))
    for file_name, original_name in imports:
        p = keyed(csv(source / f"frame/frozen_policy_{file_name}.csv"), file_name)
        require(len(p) == 132 and set(p.index) <= set(frame.index), "Invalid imported queue")
        mask = frame.index.isin(p.index)
        if original_name:
            queue_checks.append(dict(imported_policy=file_name, original_policy=original_name,
                                     shared_selections=int((mask & original_masks[(.2, original_name)]).sum()),
                                     selections_each=132))
        for name, y in targets.items():
            rows.append(dict(family="imported_package_queue", target=name, policy=file_name, budget=.2,
                             **metric(y, mask, clusters)))
    # Encoding repair is a separate sensitivity, never the main policy definition.
    repaired = original.copy()
    repaired["response"] = frame.response.to_numpy()
    xr = features(repaired)
    for j, name in enumerate(POLICIES):
        mask = np.zeros(len(frame), bool)
        mask[order_scores(xr[:, j], ties)[:132]] = True
        for target, y in targets.items():
            rows.append(dict(family="annotation_text_encoding_sensitivity", target=target, policy=name,
                             budget=.2, **metric(y, mask, clusters)))
    return pd.DataFrame(rows), pd.DataFrame(membership), pd.DataFrame(queue_checks), original_masks


def bootstrap(original, targets, config, replicates, seed):
    X, ids = features(original), original.id.to_numpy()
    clusters, domains = original.cluster.to_numpy(), original.domain.to_numpy()
    rng = np.random.default_rng(seed)
    collected = {name: [] for name in targets}
    for _ in range(replicates):
        idx, copies = draw_indices(domains, clusters, rng)
        ties = tie_keys([f"{sid}|{copy}" for sid, copy in zip(ids[idx], copies)], config["seed"])
        k = capacity(len(idx), .2)
        queues = [order_scores(X[idx, j], ties)[:k] for j in range(3)]
        for name, y in targets.items():
            sample = y[idx]
            p = int((sample == 1).sum())
            if not p or (sample < 0).any():
                collected[name].append([np.nan] * 5)
                continue
            recalls = [float((sample[q] == 1).sum()) / p for q in queues]
            collected[name].append([*recalls, recalls[0] - recalls[2], recalls[0] - k/len(idx)])
    rows = []
    for name, values in collected.items():
        values = np.asarray(values)
        for j, m in enumerate((*POLICIES, "HumT_minus_markers", "HumT_minus_random_expected")):
            v = values[:, j]
            finite = v[np.isfinite(v)]
            lo, hi = np.quantile(finite, [.025, .975]) if len(finite) else (np.nan, np.nan)
            rows.append(dict(target=name, quantity=m, lo=lo, hi=hi, confidence=.95,
                             requested=replicates, effective=len(finite), undefined=replicates-len(finite),
                             estimand="paired whole-prompt reranked hypothetical batches; exploratory"))
    return pd.DataFrame(rows)


def sensitivity(frame, original, a, b, c, resolved, targets, masks):
    metadata, version_rows, overlaps = [], [], []
    for field in ("condition", "model"):
        for group in sorted(original[field].unique()):
            ix = original[field].to_numpy() == group
            for policy in POLICIES:
                stats = metric(targets["resolved_ABC"][ix], masks[(.2, policy)][ix], original.cluster.to_numpy()[ix])
                metadata.append(dict(field=field, group=group, policy=policy, **stats))
    for col, threshold, op in (("D", 3, ">="), ("F", 4, "<"), ("OA", 4, "<")):
        old = original[col].astype(float).to_numpy()
        old = old >= threshold if op == ">=" else old < threshold
        new = targets["resolved_ABC"]
        for o in (False, True):
            for v in (-1, 0, 1):
                overlaps.append(dict(legacy=f"{col}{op}{threshold}", legacy_positive=o,
                                     new_label=v, n=int(((old == o) & (new == v)).sum())))
    for sid in frame.index:
        tags = "|".join(str(r.loc[sid, "categories"]) for r in (a, b, c) if sid in r.index)
        sensitive = any(t in tags for t in ("capability_and_continuity", "identity_and_authority"))
        version_rows.append(dict(study_id=sid, tagged_version_sensitive=sensitive,
                                 binary_disagreement=resolved.loc[sid, "A"] != resolved.loc[sid, "B"],
                                 resolved=resolved.loc[sid, "resolved"]))
    v = pd.DataFrame(version_rows)
    groups = v.groupby("tagged_version_sensitive").agg(n=("study_id", "size"),
        disagreements=("binary_disagreement", "sum"), resolved_positive=("resolved", lambda x: int((x == 1).sum())))
    return pd.DataFrame(metadata), pd.DataFrame(overlaps), groups.reset_index()


def report(points, intervals, agr, checks, encoding, elapsed):
    primary = points[(points.family == "original") & (points.target == "resolved_ABC") & (points.budget == .2)]
    lines = ["# Independent annotation analysis", "", "Analysis date: 10 October 2026.", "",
             "## Status", "", "Reconstructed from supplied records. Human provenance is author-reported, not independently authenticated. The author confirms new-assessor separation and prior consent/ethics coverage; updated supporting records, backgrounds, compensation details and an approval reference remain unavailable. C's independence and blinding are user-confirmed. This command does not modify the manuscript or source ratings; the separately authorized manuscript integration is documented in submission/annotation_integration.md. This is not independent certification of prospective clearance.", "",
             "## Original frozen policies", "", "Finite-corpus counts conditional on mixed-version A/B/C judgments. Exact budget: 132/660. Markers use token-normalized frequency; length uses token count. Random is an analytic expectation, not one sampled queue.", "",
             "| Policy | Positives | Captured | Missed | Recall | Precision |", "|---|---:|---:|---:|---:|---:|"]
    for r in primary.itertuples():
        lines.append(f"| {r.policy} | {r.positives} | {r.caught:g} | {r.missed:g} | {r.recall:.1%} | {r.precision:.1%} |")
    lines.extend(["", f"A/B binary agreement: {agr['raw_agreement']:.3%}; Cohen kappa {agr['kappa']:.4f}; positive agreement {agr['positive_agreement']:.3%}. Agreement is measured before C resolution, not three-rater reliability.", "",
                  "## Assessor sensitivity", "", "| Target | Positives | HumT captured | Markers captured | HumT minus markers recall |", "|---|---:|---:|---:|---:|"])
    for target in points.target.unique():
        cell = points[(points.family == "original") & (points.target == target) & (points.budget == .2)].set_index("policy")
        h, m = cell.loc["HumT"], cell.loc["markers_normalized"]
        lines.append(f"| {target} | {h.positives:g} | {h.caught:g} | {m.caught:g} | {100*(h.recall-m.recall):+.1f} pp |")
    lines.extend(["", "Severity-3 and union/intersection targets are secondary operational sensitivities, not replacement primary outcomes. A/B differ both by person and by capability-note version; causal effects of instruction changes cannot be identified.", "",
                  "## Secondary uncertainty", "", "95% pointwise percentile intervals from paired whole-prompt resampling with re-ranking at 20%. These estimate hypothetical empirical prompt batches, NOT sampling uncertainty of the fixed census, deployment validity, or uncertainty in the assessors' judgments. They are exploratory and not multiplicity-adjusted.", "",
                  "| Target | Contrast | Lower | Upper | Effective draws |", "|---|---|---:|---:|---:|"])
    for r in intervals[intervals.quantity.str.contains("minus")].itertuples():
        lines.append(f"| {r.target} | {r.quantity} | {100*r.lo:+.1f} pp | {100*r.hi:+.1f} pp | {r.effective}/{r.requested} |")
    cross = intervals[(intervals.target == "resolved_ABC") & intervals.quantity.str.contains("minus")]
    if ((cross.lo <= 0) & (cross.hi >= 0)).all():
        lines.extend(["", "Both resolved-label contrast intervals include zero. The point differences do not establish a robust advantage of HumT over random or markers over HumT across hypothetical prompt batches."])
    lines.extend(["", "## Preserved discrepancies", ""])
    for r in checks.itertuples():
        lines.append(f"- {r.imported_policy}: {r.shared_selections}/{r.selections_each} selections shared with original {r.original_policy}. Imported metrics are a separate family, not silently substituted.")
    lines.extend([f"- Encoding-only text differences: {encoding}. Original policies retain the original corpus text; repaired-text rankings are reported separately.",
                  "- Assessor A capability note v1.0 differs from B/C v1.1. Post-label identity/capability category summaries are descriptive, not a clean instruction experiment.",
                  "- Imported submitted_at fields generated by merge scripts do not establish actual collection times. File hashes establish current bytes, not historical consent or blinding.",
                  "", "## Interpretation", "", f"Report benefits and limitations together: HumT's observed coverage can exceed expected random review while remaining below a simple marker policy. The current primary comparison has {int(primary.iloc[0].positives)} resolved positives in {int(primary.iloc[0].positive_clusters)} prompt clusters. Do not equate non-selection with safety, concern judgments with experienced harm, agreement with validity, or this follow-up with new-corpus/practitioner validation.",
                  "", "## Reproduction", "", f"Measured runtime: {elapsed:.2f} seconds. See README for the command and manifest.json for hashes, environment and seed. Numerical outputs are deterministic; runtime and output-directory fields may differ across runs.", ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "independent_annotation/outputs")
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20261010)
    args = parser.parse_args(argv)
    require(args.replicates > 0, "Replicates must be positive")
    source, out, root = args.source.resolve(), args.output.resolve(), ROOT.parent
    require(source.is_dir(), "Source package missing")
    require(not out.is_relative_to(source) and not source.is_relative_to(out), "Output must not overlap source")
    if args.replicates < 2000:
        require(out != (ROOT / "independent_annotation/outputs").resolve(), "Pilot must use separate output directory")
    started = time.monotonic()
    before = tree_hashes(source)
    protected_paths = (root / "analysis/processed/persona_all.csv", ROOT / "protocol/criteria.yaml",
                       ROOT / "paper/overleaf/main.tex")
    protected = {str(p.relative_to(root)): sha(p) for p in protected_paths}
    config = json.loads((ROOT / "protocol/criteria.yaml").read_text())
    frame, original, a, b, c, resolved, encoding = validate(source, root)
    ay, by = resolved.A.to_numpy(), resolved.B.to_numpy()
    known = (ay >= 0) & (by >= 0)
    targets = {"A": ay, "B": by, "resolved_ABC": resolved.resolved.to_numpy(),
               "AB_union": np.where(known, np.maximum(ay, by), -1),
               "AB_intersection": np.where(known, np.minimum(ay, by), -1),
               "A_severity3": np.where(ay >= 0, a.rating.eq("3").astype(int), -1),
               "B_severity3": np.where(by >= 0, b.rating.eq("3").astype(int), -1)}
    points, selections, queue_checks, masks = point_tables(frame, original, targets, source, config)
    intervals = bootstrap(original, {k: targets[k] for k in ("A", "B", "resolved_ABC")}, config, args.replicates, args.seed)
    subgroups, overlaps, version = sensitivity(frame, original, a, b, c, resolved, targets, masks)
    agr = agreement(ay, by)
    require(tree_hashes(source) == before, "Source files changed during analysis; rerun after resolving")
    require(all(sha(root / p) == h for p, h in protected.items()), "Protected repo input changed")
    out.mkdir(parents=True, exist_ok=True)
    tables = {"resolved_labels": resolved.reset_index(drop=True), "policy_metrics": points,
              "policy_selections": selections, "queue_comparison": queue_checks,
              "bootstrap_intervals": intervals, "context_cells": subgroups,
              "legacy_overlap": overlaps, "version_category_descriptives": version}
    for name, data in tables.items():
        data.to_csv(out / (name + ".csv"), index=False, float_format="%.12g")
    (out / "agreement.json").write_text(json.dumps(agr, indent=2) + "\n")
    elapsed = time.monotonic() - started
    (out / "findings.md").write_text(report(points, intervals, agr, queue_checks, encoding, elapsed))
    git_rev = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    manifest = dict(analysis_date="2026-10-10", status="final_computational_run" if args.replicates >= 2000 else "pilot",
                    git_revision=git_rev, source=str(source), source_hashes=before,
                    protected_repo_hashes=protected, encoding_audit=encoding,
                    source_unchanged=True, command=shlex.join([sys.executable, "-m", "facct.independent_annotation.run",
                    "--source", str(source), "--output", str(out), "--replicates", str(args.replicates), "--seed", str(args.seed)]),
                    replicates=args.replicates, bootstrap_seed=args.seed, original_policy_seed=config["seed"],
                    seconds=elapsed, python=sys.version, platform=platform.platform(),
                    packages={p: importlib.metadata.version(p) for p in ("numpy", "pandas", "scipy", "pytest")},
                    code_hashes={str(p.relative_to(root)): sha(p) for p in (Path(__file__), ROOT / "analysis/screening.py", ROOT / "analysis/uncertainty.py", Path(__file__).with_name("plan.md"), Path(__file__).with_name("test_analysis.py"), Path(__file__).with_name("verify.py"))},
                    output_hashes={p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file() and p.name != "manifest.json"})
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"output": str(out), "seconds": elapsed, "agreement": agr, "source_unchanged": True}, indent=2))


if __name__ == "__main__":
    main()
