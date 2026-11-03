"""Evaluate frozen semantic rankings against existing follow-up labels.

No model calls, new labels, or policy tuning. Private inputs are read in place;
only aggregate results and hashes are written. Run from this repository with
--repo pointing to PERSONA-FAccT and --study to independent_annotation_study.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from analysis.extension_run import load, SEED

BUDGETS = (.05, .10, .20, .30)
NAMES = {"high_H": "HumT", "markers": "Markers", "length": "Length",
         "embed_sim": "Similarity", "nli_zero_shot": "NLI", "random": "Random"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check(condition, message):
    if not condition:
        raise ValueError(message)


def checked_join(corpus, frame, labels):
    """Use stored IDs, not fuzzy text, and reject incomplete or ambiguous joins."""
    mh = corpus[corpus.domain.eq("mental_health")].copy()
    for data, key in ((mh, "annotation_item_id"), (frame, "annotation_item_id"),
                      (frame, "study_id"), (labels, "study_id")):
        check(data[key].notna().all() and data[key].is_unique, f"Invalid unique key: {key}")
    check(set(mh.annotation_item_id) == set(frame.annotation_item_id), "Frame coverage differs")
    check(set(frame.study_id) == set(labels.study_id), "Label coverage differs")
    ordered = frame.set_index("annotation_item_id").loc[mh.annotation_item_id]
    check(np.allclose(ordered.humt_score.astype(float), mh.H, rtol=0, atol=1e-12), "HumT differs")
    check(np.array_equal(ordered.prompt_id.to_numpy(), mh.prompt_id), "Prompt groups differ")
    for col in ("prompt", "response"):
        check(all(a == b or a.encode("utf-8").decode("latin1") == b
                  for a, b in zip(ordered[col], mh[col])), f"Unexplained {col} differences")
    target = labels.set_index("study_id").loc[ordered.study_id, "resolved"].to_numpy(int)
    check(np.isin(target, [0, 1]).all(), "Unresolved follow-up labels")
    return mh, ordered.study_id.to_numpy(), target.astype(bool)


def selected(scores, ties, k, screening):
    mask = np.zeros(len(scores), bool)
    mask[screening.order_scores(scores, ties)[:k]] = True
    check(mask.sum() == k, "Incorrect review capacity")
    return mask


def interval(values):
    x = np.asarray(values, float)
    finite = x[np.isfinite(x)]
    if not len(finite):
        return np.nan, np.nan, 0
    lo, hi = np.quantile(finite, [.025, .975])
    return lo, hi, len(finite)


def evaluate(mh, targets, scores, screening, uncertainty, replicates, seed):
    ties = screening.tie_keys(mh.id.to_numpy(), SEED)
    n = len(mh)
    names = list(scores) + ["random"]
    point, intervals, contrasts = [], [], []
    draws = {(c, b, name): [] for c in targets for b in BUDGETS for name in names}
    for b in BUDGETS:
        k = screening.capacity(n, b)
        masks = {name: selected(s, ties, k, screening) for name, s in scores.items()}
        for c, y in targets.items():
            p = int(y.sum())
            for name in names:
                caught = k * p / n if name == "random" else int((masks[name] & y).sum())
                point.append(dict(criterion=c, budget=b, policy=name, n=n, concerns=p,
                                  concern_clusters=mh.loc[y, "cluster"].nunique(), selected=k,
                                  caught=caught, missed=p-caught, recall=caught/p if p else np.nan,
                                  precision=caught/k if k else np.nan,
                                  unselected_prevalence=(p-caught)/(n-k) if n>k else np.nan))
    rng = np.random.default_rng(seed)
    for _ in range(replicates):
        idx, copies = uncertainty.draw_indices(mh.domain.to_numpy(), mh.cluster.to_numpy(), rng)
        keys = screening.tie_keys([f"{v}|{c}" for v, c in zip(mh.id.to_numpy()[idx], copies)], SEED)
        orders = {name: screening.order_scores(s[idx], keys) for name, s in scores.items()}
        for b in BUDGETS:
            k = screening.capacity(len(idx), b)
            for c, labels in targets.items():
                y = labels[idx]
                p = y.sum()
                for name in names:
                    recall = (k/len(idx) if name == "random" else y[orders[name][:k]].sum()/p) if p else np.nan
                    draws[c, b, name].append(recall)
    for c in targets:
        for b in BUDGETS:
            for name in names:
                lo, hi, valid = interval(draws[c, b, name])
                intervals.append(dict(criterion=c, budget=b, policy=name, lo=lo, hi=hi, finite=valid))
                for other in ("high_H", "markers", "random"):
                    if name == other:
                        continue
                    delta = np.array(draws[c, b, name]) - np.array(draws[c, b, other])
                    lo, hi, valid = interval(delta)
                    contrasts.append(dict(criterion=c, budget=b, policy=name, versus=other,
                                          lo_pp=100*lo, hi_pp=100*hi, finite=valid))
    points = pd.DataFrame(point).merge(pd.DataFrame(intervals), validate="one_to_one")
    diffs = pd.DataFrame(contrasts)
    lookup = points.set_index(["criterion", "budget", "policy"]).recall
    diffs["diff_pp"] = [100*(lookup[c,b,p]-lookup[c,b,v])
                        for c,b,p,v in diffs[["criterion","budget","policy","versus"]].itertuples(index=False, name=None)]
    return points, diffs


def texnumber(value, signed=False):
    return f"{value:+.1f}" if signed else f"{value:.1f}"


def make_outputs(points, diffs, out, paper):
    table = [r"\begin{table}[t]", r"\centering\small",
             r"\caption{Existing independent mental-health assessments: 19 concern cases in 13 prompt groups, 132 of 660 responses selected. All policies use the same fixed capacity. Differences are policy minus HumT recall in percentage points with paired prompt-cluster 95\% intervals (2,000 draws, seed 20261010). Random counts are expectations. These exploratory comparisons use previously inspected labels.}",
             r"\label{tab:semantic_followup}", r"\begin{tabular}{lrrrrl}", r"\toprule",
             r"Policy & Caught & Missed & Recall (\%) & Precision (\%) & Difference vs HumT \\", r"\midrule"]
    p = points[(points.criterion == "followup") & points.budget.eq(.2)].set_index("policy")
    d = diffs[(diffs.criterion == "followup") & diffs.budget.eq(.2) & diffs.versus.eq("high_H")].set_index("policy")
    for name in ("high_H", "markers", "length", "embed_sim", "nli_zero_shot", "random"):
        row = p.loc[name]
        contrast = "--" if name == "high_H" else "$" + texnumber(d.loc[name,"diff_pp"], True) + " [" + texnumber(d.loc[name,"lo_pp"], True) + ", " + texnumber(d.loc[name,"hi_pp"], True) + "]$"
        count = f"{row.caught:.1f}" if name == "random" else f"{row.caught:.0f}"
        missed = f"{row.missed:.1f}" if name == "random" else f"{row.missed:.0f}"
        table.append(f"{NAMES[name]} & {count} & {missed} & {100*row.recall:.1f} & {100*row.precision:.1f} & {contrast} " + r"\\")
    table += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (paper / "tables/semantic_followup.tex").write_text("\n".join(table)+"\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family":"serif", "font.size":9, "pdf.fonttype":42,
                         "axes.spines.top":False, "axes.spines.right":False})
    fig, axes = plt.subplots(1, 2, figsize=(7.05, 2.75), sharex=True)
    styles = {"high_H":("#222222","o","-"), "markers":("#0072B2","s","-"),
              "length":("#777777","v",":"), "embed_sim":("#009E73","D","--"),
              "nli_zero_shot":("#D55E00","^","-."), "random":("#999999",None,"--")}
    for ax, c, title in zip(axes, ("D", "followup"),
                            ("Original broad criterion (165 cases)", "Independent contextual criterion (19 cases)")):
        for name, (color, marker, linestyle) in styles.items():
            rows = points[(points.criterion==c) & (points.policy==name)].sort_values("budget")
            ax.plot(rows.budget*100, rows.recall*100, color=color, marker=marker,
                    linestyle=linestyle, markersize=3.5, linewidth=1.2, label=NAMES[name])
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("Review capacity (% of 660 responses)")
        ax.set_xticks([5,10,20,30]); ax.set_ylim(0,100); ax.set_yticks([0,20,40,60,80,100])
        ax.grid(axis="y", color="0.9", linewidth=.5)
    axes[0].set_ylabel("Concern cases selected (%)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=6, frameon=False, fontsize=8)
    fig.tight_layout(rect=[0,.13,1,1])
    fig.savefig(paper / "figures/review_budget_comparison.pdf", bbox_inches="tight",
                metadata={"CreationDate":None,"ModDate":None})
    fig.savefig(out / "review_budget_comparison.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--study", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("analysis_outputs/professor_revision"))
    parser.add_argument("--paper", type=Path, default=Path("paper"))
    parser.add_argument("--replicates", type=int, default=2000)
    args = parser.parse_args()
    start = time.monotonic()
    args.out.mkdir(parents=True, exist_ok=True)
    corpus_path = args.repo / "analysis/processed/persona_all.csv"
    old_manifest = json.loads(Path("analysis_outputs/manifest.json").read_text())
    expected = old_manifest.get("corpus_sha256") or old_manifest.get("corpus_sha")
    check(expected == sha(corpus_path), "Cached scores cannot be aligned to a changed corpus")
    corpus, screening, uncertainty, _ = load(args.repo)
    frame_path = args.study / "frame/immutable_frame.csv"
    labels_path = args.repo / "facct/independent_annotation/outputs/resolved_labels.csv"
    inputs = {str(p):sha(p) for p in (corpus_path, frame_path, labels_path)}
    mh, sids, y = checked_join(corpus, pd.read_csv(frame_path), pd.read_csv(labels_path))
    check((len(mh), int(y.sum()), mh.loc[y,"cluster"].nunique()) == (660,19,13), "Unexpected follow-up counts")
    X = screening.features(mh)
    scores = dict(high_H=X[:,0], length=X[:,1], markers=X[:,2])
    for name, filename in (("embed_sim","embed_scores.npy"),("nli_zero_shot","nli_scores.npy")):
        path = Path("analysis_outputs/cache") / filename
        inputs[str(path)] = sha(path)
        array = np.load(path, allow_pickle=False)
        check(array.shape==(len(corpus),) and np.isfinite(array).all(), "Invalid cached score array")
        scores[name] = array[mh.index.to_numpy()]
    archived = pd.read_csv(args.repo / "facct/independent_annotation/outputs/policy_selections.csv")
    ties = screening.tie_keys(mh.id.to_numpy(), SEED)
    for b in BUDGETS:
        for name, old in (("high_H","HumT"),("length","length_words"),("markers","markers_normalized")):
            mask = selected(scores[name], ties, screening.capacity(len(mh),b), screening)
            expected_ids = set(archived[(archived.family=="original") & archived.budget.eq(b) & (archived.policy==old)].study_id)
            check(set(sids[mask]) == expected_ids, "Existing queue identities did not reproduce")
    targets = {"D":mh.D.ge(3).to_numpy(), "F":mh.F.lt(4).to_numpy(),
               "OA":mh.OA.lt(4).to_numpy(), "followup":y}
    points, diffs = evaluate(mh, targets, scores, screening, uncertainty, args.replicates, 20261010)
    points.to_csv(args.out/"mental_health_budget_metrics.csv", index=False)
    diffs.to_csv(args.out/"mental_health_budget_contrasts.csv", index=False)
    rank_rows = []
    for criterion, labels in targets.items():
        for policy, sc in scores.items():
            ap, auc, _ = screening.rank_metrics(labels, sc, screening.order_scores(sc, ties))
            check(np.isclose(ap, average_precision_score(labels,sc)), "AP independent check failed")
            check(np.isclose(auc, roc_auc_score(labels,sc)), "AUC independent check failed")
            rank_rows.append(dict(criterion=criterion, policy=policy, prevalence=labels.mean(), ap=ap, auc=auc))
    pd.DataFrame(rank_rows).to_csv(args.out/"rank_metrics_verified.csv", index=False)
    make_outputs(points, diffs, args.out, args.paper)
    check(all(sha(p)==h for p,h in inputs.items()), "An immutable input changed")
    manifest = dict(input_hashes=inputs, source_unchanged=True, joined_rows=660, concerns=19,
                    concern_clusters=13, old_queue_identity_checks=12, cached_scores_only=True,
                    new_model_calls=0, bootstrap_seed=20261010, policy_seed=SEED, replicates=args.replicates,
                    status="final" if args.replicates>=2000 else "pilot",
                    seconds=round(time.monotonic()-start,2),
                    packages={p:importlib.metadata.version(p) for p in ("numpy","pandas","scikit-learn","scipy","matplotlib")},
                    code_sha256=sha(__file__))
    (args.out/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(points[(points.criterion=="followup") & points.budget.eq(.2)].to_string(index=False))
    print(diffs[(diffs.criterion=="followup") & diffs.budget.eq(.2) & diffs.policy.isin(["embed_sim","nli_zero_shot"])].to_string(index=False))
    print("Seconds:", manifest["seconds"])


if __name__ == "__main__":
    main()
