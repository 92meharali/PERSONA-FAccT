"""Reproduce the exploratory criterion-to-decision amendment."""
import argparse
import importlib.metadata
import itertools
import json
from pathlib import Path
import subprocess
import time

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from facct.analysis.screening import features, labels, tie_keys
from facct.analysis.uncertainty import summarize
from facct.analysis.validate_inputs import sha, source_hashes
from facct.conditional.analysis import crossfit, group_folds, resample_within_folds
from .analysis import METRICS, measure, queue_pairs, random_counts, selections

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "facct/criterion_transfer"
TRAIN = ("D_ge3", "F_lt4", "OA_lt4")
MODELS = ("lexical_lr", "lexical_humt_lr")
FIXED = ("high_H", "length", "markers")


def frozen_hashes():
    hashes = source_hashes(ROOT)
    for directory in ("facct/outputs", "facct/conditional", "facct/independent_annotation/outputs",
                      "facct/revision/outputs", "facct/allocation/outputs", "facct/professor_revision"):
        hashes.update({str(p.relative_to(ROOT)): sha(p) for p in (ROOT/directory).rglob("*")
                       if p.is_file() and "__pycache__" not in p.parts})
    return hashes


def followup(d):
    """Join by audited response identity, never by an assumed CSV row order."""
    out = ROOT / "facct/independent_annotation/outputs"
    manifest = json.loads((out/"manifest.json").read_text())
    for name, digest in manifest["output_hashes"].items():
        assert sha(out/name) == digest, f"Changed follow-up output: {name}"
    frame_path = Path(manifest["source"]) / "frame/immutable_frame.csv"
    assert sha(frame_path) == manifest["source_hashes"]["frame/immutable_frame.csv"]
    frame = pd.read_csv(frame_path)
    resolved = pd.read_csv(out/"resolved_labels.csv")
    linked = frame.merge(resolved, on="study_id", validate="one_to_one")
    assert len(linked) == len(d) == 660
    assert set(linked.annotation_item_id) == set(d.annotation_item_id)
    linked = linked.set_index("annotation_item_id").loc[d.annotation_item_id]
    assert np.array_equal(linked.prompt_id, d.prompt_id)
    assert np.isin(linked.resolved, [0, 1]).all()
    assert np.allclose(linked.humt_score, d.H, rtol=0, atol=1e-12)
    return linked.resolved.to_numpy(bool), {"frame_sha256": sha(frame_path),
        "resolved_labels_sha256": sha(out/"resolved_labels.csv"),
        "assessment_manifest_sha256": sha(out/"manifest.json")}


def estimate(scores, outcomes, folds, keys, budget):
    masks = selections(scores[:, :, 4:6], folds, keys, budget)
    fixed_masks = selections(scores[:, 0, :3, None], folds, keys, budget)
    values = measure(masks, outcomes)
    fixed = measure(fixed_masks, outcomes)[:, 0]
    random = random_counts(outcomes, folds, budget)
    p = outcomes.sum(axis=0)
    random_recall = np.divide(random, p, out=np.full(len(p), np.nan), where=p > 0)
    return values, fixed, random, random_recall, masks, fixed_masks


def run_domain(d, config, criteria):
    domain = d.domain.iloc[0]
    X, Y = features(d), labels(d, criteria)
    outcomes, endpoints = Y.copy(), list(TRAIN)
    followup_audit = None
    if domain == "mental_health":
        target, followup_audit = followup(d)
        outcomes = np.column_stack([outcomes, target])
        endpoints.append("contextual_reviewworthiness")
    folds = group_folds(d.cluster.to_numpy(), config["seed"], config["folds"])
    clusters, ids = d.cluster.to_numpy(), d.id.to_numpy()
    keys = tie_keys(ids, config["seed"])
    scores, _, _ = crossfit(X, Y, folds, clusters, config)
    previous = pd.read_csv(ROOT/"facct/conditional/outputs/oof_predictions.csv")
    for j, target in enumerate(TRAIN):
        old = previous[(previous.domain == domain) & (previous.criterion == target)].set_index("id").loc[ids]
        assert np.array_equal(old.fold, folds)
        assert np.array_equal(old.concern, Y[:, j])
        np.testing.assert_allclose(old[["reduced_lr", "extended_lr"]], scores[:, j, 4:6], rtol=1e-10, atol=1e-12)
    points = {b: estimate(scores, outcomes, folds, keys, b) for b in config["budgets"]}
    draws, fixed_draws, random_draws, fallbacks = [], [], [], []
    rng = np.random.default_rng(config["seed"])
    for rep in range(config["replicates"]):
        idx, copies = resample_within_folds(folds, clusters, rng)
        sampled_scores, _, fallback = crossfit(X[idx], Y[idx], folds[idx], clusters[idx], config)
        sampled_keys = tie_keys([f"{v}|{c}" for v, c in zip(ids[idx], copies)], config["seed"])
        v, fixed, _, rand, _, _ = estimate(sampled_scores, outcomes[idx], folds[idx], sampled_keys, config["reference_budget"])
        draws.append(v)
        fixed_draws.append(fixed)
        random_draws.append(rand)
        fallbacks.append(fallback)
        if (rep+1) % 250 == 0:
            print(f"{domain}: {rep+1}/{config['replicates']} paired refit draws", flush=True)
    draws, fixed_draws, random_draws = map(np.asarray, (draws, fixed_draws, random_draws))
    rows, contrasts, overlaps, memberships, baselines = [], [], [], [], []
    p = outcomes.sum(axis=0)
    for budget, (values, fixed, rand, rand_recall, masks, fixed_masks) in points.items():
        k = int(masks[:, 0, 0].sum())
        assert np.all(masks.sum(axis=0) == k) and np.all(fixed_masks.sum(axis=0) == k)
        for t, model, e in itertools.product(range(3), range(2), range(len(endpoints))):
            row = dict(domain=domain, train_target=TRAIN[t], model=MODELS[model], evaluation_target=endpoints[e],
                budget=budget, n=len(d), selected=k, concerns=int(p[e]),
                concern_clusters=len(np.unique(clusters[outcomes[:, e]])),
                nonconcern_clusters=len(np.unique(clusters[~outcomes[:, e]])))
            row["sparse"] = min(row["concern_clusters"], row["nonconcern_clusters"]) < 10
            for m, name in enumerate(METRICS):
                row[name] = values[t, model, e, m]
                ci = summarize(draws[:, t, model, e, m]) if budget == .2 else (np.nan, np.nan, 0)
                row.update({name+"_lo": ci[0], name+"_hi": ci[1], name+"_valid": ci[2]})
            ci = summarize(draws[:, t, model, e, 1]-random_draws[:, e]) if budget == .2 else (np.nan, np.nan, 0)
            row.update(delta_random=values[t, model, e, 1]-rand_recall[e],
                delta_random_lo=ci[0], delta_random_hi=ci[1], delta_random_valid=ci[2])
            rows.append(row)
        for e, endpoint in enumerate(endpoints):
            for policy in range(4):
                value = fixed[policy, e] if policy < 3 else np.array([rand[e], rand_recall[e], rand[e]/k if k else np.nan,
                    p[e]-rand[e], (p[e]-rand[e])/(len(d)-k) if k<len(d) else np.nan])
                baselines.append(dict(domain=domain, evaluation_target=endpoint, budget=budget,
                    policy=FIXED[policy] if policy<3 else "uniform_random", n=len(d), selected=k,
                    concerns=int(p[e]), **dict(zip(METRICS, value))))
        for pair in queue_pairs(masks, outcomes):
            a, b, m = pair["left"], pair["right"], pair["model"]
            common = dict(domain=domain, budget=budget, model=MODELS[m],
                left_target=TRAIN[a], right_target=TRAIN[b])
            overlaps.append(dict(**common, selected=k, **{name: pair[name] for name in
                ("intersection", "union", "symmetric_difference", "jaccard")}))
            for e, endpoint in enumerate(endpoints):
                lo, hi, valid = summarize(draws[:, a, m, e, 1]-draws[:, b, m, e, 1]) if budget==.2 else (np.nan, np.nan, 0)
                contrasts.append(dict(**common, evaluation_target=endpoint, concerns=int(p[e]),
                    left_caught=values[a, m, e, 0], right_caught=values[b, m, e, 0],
                    left_only_caught=int(pair["left_only_caught"][e]), right_only_caught=int(pair["right_only_caught"][e]),
                    recall_difference=values[a, m, e, 1]-values[b, m, e, 1], lo=lo, hi=hi, valid_replicates=valid))
        for t, m in itertools.product(range(3), range(2)):
            memberships.extend(dict(domain=domain, budget=budget, train_target=TRAIN[t], model=MODELS[m], id=ids[i],
                cluster=clusters[i], fold=int(folds[i])) for i in np.flatnonzero(masks[:, t, m]))
    split_rows = []
    for seed in config["split_sensitivity_seeds"]:
        alt = group_folds(clusters, seed, config["folds"])
        alt_scores, _, _ = crossfit(X, Y, alt, clusters, config)
        value, _, _, _, mask, _ = estimate(alt_scores, outcomes, alt, keys, .2)
        for t, m, e in itertools.product(range(3), range(2), range(len(endpoints))):
            split_rows.append(dict(domain=domain, seed=seed, train_target=TRAIN[t], model=MODELS[m],
                evaluation_target=endpoints[e], selected=int(mask[:, t, m].sum()),
                concerns=int(p[e]), caught=value[t, m, e, 0], recall=value[t, m, e, 1]))
    return {"performance": rows, "contrasts": contrasts, "queue_overlap": overlaps,
            "selections": memberships, "baselines": baselines, "split_sensitivity": split_rows}, dict(
        predictions_match_previous=True, followup=followup_audit, fallback_draws=int(np.count_nonzero(fallbacks)),
        fallback_fits=int(sum(fallbacks))), draws, random_draws


def report(out, replicates):
    p = pd.read_csv(out/"performance.csv")
    c = pd.read_csv(out/"contrasts.csv")
    lines = ["# Criterion-to-decision results", "", f"{'FINAL' if replicates >= 2000 else 'PILOT'}: {replicates} resamples. Exploratory analysis; all cells retained. No new primary family, outcome labels, or algorithm.", "",
        "## Lexical screen, 20% reference fraction", "",
        "| Domain | Training target | Assessment target | Caught / cases | Slots | Recall [95%] |",
        "|---|---|---|---:|---:|---|"]
    for r in p[(p.budget==.2)&(p.model==MODELS[0])].itertuples():
        lines.append(f"| {r.domain} | {r.train_target} | {r.evaluation_target} | {r.caught:g}/{r.concerns} | {r.selected} | {100*r.recall:.1f} [{100*r.recall_lo:.1f}, {100*r.recall_hi:.1f}] |")
    lines += ["", "## All F-trained minus OA-trained contrasts (lexical, 20%)", "",
        "| Domain | Assessment target | Recall change pp [95%] | Finite draws |",
        "|---|---|---|---:|"]
    chosen = c[(c.budget==.2)&(c.model==MODELS[0])&(c.left_target=="F_lt4")&(c.right_target=="OA_lt4")]
    for r in chosen.itertuples():
        lines.append(f"| {r.domain} | {r.evaluation_target} | {100*r.recall_difference:+.1f} [{100*r.lo:+.1f}, {100*r.hi:+.1f}] | {r.valid_replicates} |")
    lines += ["", "## Boundaries", "",
        "All models use original training labels only. Follow-up outcomes never enter fitting. The follow-up is an additional outcome on the same corpus, not unseen validation data. Its 19 positives constrain inference.", "",
        f"Intervals refit and rerank {replicates:,} paired prompt-cluster resamples within original folds. They are pointwise, exploratory, and conditional on the empirical judgments and partition. Sparse targets, zero-positive draws and constant-score fallback fits remain explicit. Off-diagonal performance is criterion transfer, not domain transfer or causal evidence.", "",
        "Target changes include differences in prevalence, threshold and rubric content; they do not isolate pure construct effects. Queue differences do not demonstrate better review or experienced harm. Trained screens require historical labels, unlike fixed lexical/HumT rules. Every target pair and the H-augmented feature sensitivity remain in the tables; no winning screen is selected using follow-up results.", "",
        "Reproduce: `.venv/bin/python -m facct.criterion_transfer.run`. Runtime and source checks are in manifest.json. Source follow-up frame is required at the recorded local path; identifying consent/recruitment records are not read or packaged."]
    (out/"findings.md").write_text("\n".join(lines)+"\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=HERE/"outputs")
    args = parser.parse_args()
    if args.replicates < 1 or (args.replicates < 2000 and args.output.resolve() == (HERE/"outputs").resolve()):
        raise ValueError("Pilot runs require positive draws and a separate output directory")
    start = time.monotonic()
    before = frozen_hashes()
    config = json.loads((ROOT/"facct/conditional/config.json").read_text())
    config["replicates"] = args.replicates
    criteria = json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    assert tuple(criteria["criteria"]) == TRAIN
    d = pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"], d["cluster"] = d.domain+":"+d.annotation_item_id, d.domain+":"+d.prompt_id
    assert not d.id.duplicated().any()
    args.output.mkdir(parents=True, exist_ok=True)
    collected, audits = {}, {}
    with threadpool_limits(limits=1):
        for domain in ("mental_health", "education", "health"):
            rows, audit, draws, random_draws = run_domain(d[d.domain==domain].reset_index(drop=True), config, criteria)
            for key, value in rows.items():
                collected.setdefault(key, []).extend(value)
            audits[domain] = audit
            np.savez_compressed(args.output/f"bootstrap_{domain}.npz", values=draws, random_recall=random_draws)
    for name, rows in collected.items():
        pd.DataFrame(rows).to_csv(args.output/f"{name}.csv", index=False)
    report(args.output, args.replicates)
    assert before == frozen_hashes(), "Source or prior analysis changed"
    manifest = dict(status="final" if args.replicates>=2000 else "pilot", config=config,
        training_targets=TRAIN, models=MODELS, metrics=METRICS,
        bootstrap_axes=["replicate", "training_target", "model", "evaluation_target", "metric"],
        evaluation_targets={dom: list(TRAIN)+(["contextual_reviewworthiness"] if dom=="mental_health" else []) for dom in audits},
        audits=audits, frozen_hashes=before, runtime_seconds=round(time.monotonic()-start, 2),
        git_revision=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        software={p: importlib.metadata.version(p) for p in ("numpy", "pandas", "scikit-learn", "scipy", "threadpoolctl")},
        code_and_plan={str(p.relative_to(ROOT)): sha(p) for p in HERE.glob("*") if p.is_file()},
        outputs={p.name: sha(p) for p in args.output.glob("*") if p.is_file() and p.name not in {"manifest.json", "paper_assets.json", "verification.json"}})
    (args.output/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps({"status": manifest["status"], "runtime_seconds": manifest["runtime_seconds"], "source_and_previous_outputs_unchanged": True}))


if __name__ == "__main__":
    main()
