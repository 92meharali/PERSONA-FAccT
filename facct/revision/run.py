"""Review-response diagnostics and paired comparisons on immutable inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import time

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from analysis.build_dataset import join_humt, humt_file
from analysis.persona_common import norm_text
from analysis.reliability import icc_absolute, rater_matrix
from facct.analysis.screening import capacity, features, labels, order_scores, rank_metrics, tie_keys
from facct.analysis.uncertainty import draw_indices, summarize
from facct.analysis.validate_inputs import source_hashes, sha


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "facct/revision/outputs"
DOMAINS = ["mental_health", "education", "health"]
POLICIES = ["high_H", "length", "markers", "rank_fusion"]


def fusion_scores(X):
    """Outcome-free equal-weight midrank percentiles; high scores rank first."""
    if not len(X):
        return np.array([])
    return (rankdata(X[:, 0], method="average") + rankdata(X[:, 2], method="average")) / (2 * len(X))


def policy_orders(X, keys):
    scores = np.column_stack((X, fusion_scores(X)))
    return [order_scores(scores[:, i], keys) for i in range(4)], scores


def allocation_values(X, Y, keys, budget=.2):
    orders, scores = policy_orders(X, keys)
    n, k = len(X), capacity(len(X), budget)
    result = []
    for y in Y.T:
        p = int(y.sum())
        catches = np.array([y[o[:k]].sum() for o in orders], dtype=float)
        recalls = catches / p if p else np.full(4, np.nan)
        work = np.array([rank_metrics(y, scores[:, i], orders[i])[2][1] for i in range(4)])
        random_work = np.ceil(.8 * p) * (n + 1) / ((p + 1) * n) if p else np.nan
        result.append([recalls[3], recalls[3]-recalls[2], recalls[0]-recalls[2],
                       work[0]-random_work, work[0]-work[1], work[0]-work[2]])
    return np.asarray(result)


def complementarity(X, Y, keys, config, domain):
    orders, _ = policy_orders(X, keys)
    rows = []
    for budget in config["budgets"]:
        k = capacity(len(X), budget)
        sets = [set(o[:k]) for o in orders]
        h, m, f = sets[0], sets[2], sets[3]
        for j, criterion in enumerate(config["criteria"]):
            positives = set(np.flatnonzero(Y[:, j]))
            rows.append(dict(domain=domain, criterion=criterion, budget=budget, n=len(X), selected=k,
                concerns=len(positives), selected_overlap=len(h & m), union_size=len(h | m),
                caught_both=len(h & m & positives), caught_h_only=len((h-m) & positives),
                caught_markers_only=len((m-h) & positives), caught_h=len(h & positives),
                caught_markers=len(m & positives), caught_fusion=len(f & positives),
                fusion_recall=len(f & positives)/len(positives) if positives else np.nan,
                union_is_not_a_policy=True))
    return rows


def extra_bootstrap(frame, config, replicates):
    rows = []
    metrics = ["fusion_recall", "fusion_minus_markers_recall", "H_minus_markers_recall",
               "H_minus_random_workload80", "H_minus_length_workload80", "H_minus_markers_workload80"]
    for domain in DOMAINS:
        d = frame[frame.domain == domain].reset_index(drop=True)
        X, Y = features(d), labels(d, config)
        keys = tie_keys(d.id, config["seed"])
        point = allocation_values(X, Y, keys)
        rng = np.random.default_rng(config["seed"])
        values = np.empty((replicates, *point.shape))
        for b in range(replicates):
            idx, copies = draw_indices(d.domain.to_numpy(), d.cluster.to_numpy(), rng)
            keys_b = tie_keys([f"{v}|{c}" for v, c in zip(d.id.to_numpy()[idx], copies)], config["seed"])
            values[b] = allocation_values(X[idx], Y[idx], keys_b)
        for j, criterion in enumerate(config["criteria"]):
            pc = d.loc[Y[:, j], "cluster"].nunique()
            nc = d.loc[~Y[:, j], "cluster"].nunique()
            for i, metric in enumerate(metrics):
                lo, hi, valid = summarize(values[:, j, i])
                rows.append(dict(domain=domain, criterion=criterion, budget=.2, metric=metric,
                    estimate=point[j, i], lo=lo, hi=hi, valid_replicates=valid,
                    replicates=replicates, concern_clusters=pc, nonconcern_clusters=nc,
                    sparse=min(pc, nc)<10, interval="exploratory pointwise 95%"))
        print(f"Paired revision bootstrap: {domain}, {replicates} replicates", flush=True)
    return pd.DataFrame(rows)


def cutoff_diagnostics(frame, ratings, config, out):
    summaries, votes_rows = [], []
    distribution = frame.groupby("domain")[["D", "F", "OA"]].apply(
        lambda g: g.melt(var_name="dimension", value_name="mean").groupby(["dimension", "mean"]).size()).rename("n")
    distribution.to_csv(out / "mean_distributions.csv")
    for domain in DOMAINS:
        d = frame[frame.domain == domain].set_index("annotation_item_id")
        r = ratings[ratings.domain == domain]
        for criterion, rule in config["criteria"].items():
            dim, threshold = rule["column"], rule["threshold"]
            matrix = r.pivot(index="annotation_item_id", columns="annotator_id", values=dim+"_score").dropna(axis=1, how="all").loc[d.index]
            assert matrix.shape == (len(d), 5) and not matrix.isna().any().any()
            positive = matrix.ge(threshold) if rule["operator"] == ">=" else matrix.lt(threshold)
            votes = positive.sum(axis=1)
            mean_positive = d[dim].ge(threshold) if rule["operator"] == ">=" else d[dim].lt(threshold)
            near = np.abs(d[dim] - threshold) <= .2 + 1e-10
            summaries.append(dict(domain=domain, criterion=criterion, n=len(d), near_cutoff=int(near.sum()),
                exactly_cutoff=int(np.isclose(d[dim], threshold).sum()),
                unanimous_trigger=int((votes==5).sum()), unanimous_nontrigger=int((votes==0).sum()),
                split_votes=int(votes.between(1,4).sum()),
                mean_majority_disagree=int((mean_positive != votes.ge(3)).sum())))
            for v in range(6):
                votes_rows.append(dict(domain=domain, criterion=criterion, trigger_votes=v, n=int((votes==v).sum())))
    pd.DataFrame(summaries).to_csv(out / "cutoff_diagnostics.csv", index=False)
    pd.DataFrame(votes_rows).to_csv(out / "trigger_vote_distribution.csv", index=False)
    reliability = pd.read_csv(ROOT / "analysis/outputs/tables/reliability.csv")
    for row in reliability.itertuples():
        matrix = rater_matrix(ratings[ratings.domain==row.domain], row.dimension)
        a1, ak = icc_absolute(matrix)
        assert np.isclose(a1, row.icc_a1) and np.isclose(ak, row.icc_ak), "Reliability point mismatch"
    reliability.to_csv(out / "source_reliability.csv", index=False)


def text_audit(frame, config, out):
    records, sensitivity = [], []
    for domain in DOMAINS:
        d = frame[frame.domain==domain].reset_index(drop=True)
        if domain == "mental_health":
            for row in d.itertuples():
                records.append(dict(domain=domain, id=row.id, tier="embedded", export_row=np.nan,
                    comparison="embedded_only_no_separate_scorer_text", raw_equal=None, normalized_equal=None))
            continue
        humt = pd.read_csv(humt_file(domain), encoding="utf-8-sig")
        # The unused std payload traces source row indices through the unchanged join.
        # This is an in-memory copy only; original scores/files remain untouched.
        trace = humt.copy()
        trace["std_humt_text"] = np.arange(len(trace), dtype=float)
        joined = join_humt(d.response, trace)
        assert not joined.humt.isna().any()
        assert np.allclose(joined.humt, d.H, rtol=0, atol=1e-12)
        assert (joined.humt_join_tier.to_numpy() == d.humt_join_tier.to_numpy()).all()
        assert (joined.humt_source_file.to_numpy() == d.humt_source_file.to_numpy()).all()
        source_idx = joined.humt_std.astype(int).to_numpy()
        assert len(set(source_idx)) == len(d), "Source row reused"
        exported = d.copy()
        exported["response"] = humt.loc[source_idx, "text"].to_numpy()
        X, Xexport = features(d), features(exported)
        for i, row in enumerate(d.itertuples()):
            a, b = row.response, exported.response.iloc[i]
            na, nb = norm_text(a), norm_text(b)
            comparison = "raw_equal" if a==b else "normalization_only" if na==nb else "prefix_related" if na.startswith(nb) or nb.startswith(na) else "other_difference"
            records.append(dict(domain=domain, id=row.id, tier=row.humt_join_tier,
                export_row=int(source_idx[i]), comparison=comparison, raw_equal=a==b, normalized_equal=na==nb,
                rated_sha256=hashlib.sha256(a.encode()).hexdigest(), export_sha256=hashlib.sha256(b.encode()).hexdigest(),
                rated_chars=len(a), export_chars=len(b), rated_words=X[i,1], export_words=Xexport[i,1],
                rated_markers=X[i,2], export_markers=Xexport[i,2]))
        for name, batch, xx, k in [
            ("rated_full", d, X, capacity(len(d), .2)),
            ("export_text_full", d, Xexport, capacity(len(d), .2)),
            ("full_join_same_capacity", d[d.humt_join_tier=="full"], X[d.humt_join_tier=="full"], capacity(len(d), .2)),
            ("full_join_same_fraction", d[d.humt_join_tier=="full"], X[d.humt_join_tier=="full"], capacity(sum(d.humt_join_tier=="full"), .2))]:
            assert k <= len(batch)
            keys = tie_keys(batch.id, config["seed"])
            orders, _ = policy_orders(xx, keys)
            Y = labels(batch, config)
            for j, criterion in enumerate(config["criteria"]):
                for i, policy in enumerate(POLICIES):
                    p, caught = int(Y[:,j].sum()), int(Y[orders[i][:k],j].sum())
                    sensitivity.append(dict(domain=domain, sensitivity=name, criterion=criterion, policy=policy,
                        n=len(batch), selected=k, concerns=p, caught=caught, recall=caught/p if p else np.nan))
    details = pd.DataFrame(records)
    details.to_csv(out / "text_provenance.csv", index=False)
    details.groupby(["domain", "tier", "comparison"]).size().rename("n").to_csv(out / "text_provenance_summary.csv")
    pd.DataFrame(sensitivity).to_csv(out / "text_representation_sensitivity.csv", index=False)


def figures(out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    table = pd.read_csv(ROOT / "facct/outputs/tables/screening.csv")
    for domains, name in [(["mental_health"], "mental_health_budgets"), (["education", "health"], "transfer_budgets")]:
        fig, axes = plt.subplots(len(domains), 3, figsize=(11.5, 3.6*len(domains)), squeeze=False, sharex=True, sharey=True)
        for i, domain in enumerate(domains):
            for j, criterion in enumerate(("D_ge3", "F_lt4", "OA_lt4")):
                ax=axes[i,j]
                for policy, color, marker, label in [("high_H", "#0072B2", "o", "HumT"), ("length", "#D55E00", "s", "Length"), ("markers", "#009E73", "^", "Markers"), ("uniform_random", "#555555", ".", "Random (expected)")]:
                    d=table[(table.domain==domain)&(table.criterion==criterion)&(table.policy==policy)].sort_values("budget")
                    ax.plot(100*d.budget, 100*d.recall, color=color, marker=marker, label=label)
                    if policy=="high_H":
                        ax.fill_between(100*d.budget, 100*d.recall_lo, 100*d.recall_hi, color=color, alpha=.14)
                ref=d.iloc[0]
                ax.set_title({"D_ge3":"D mean >= 3", "F_lt4":"Fit mean < 4", "OA_lt4":"OA mean < 4"}[criterion]+f"\n{int(ref.concerns)} cases / {int(ref.n)} responses")
                ax.set_ylim(0,105); ax.set_xticks([5,10,20,30]); ax.grid(alpha=.2)
                ax.set_xlabel("Review budget (%)")
                if j==0:
                    ax.set_ylabel({"mental_health":"Mental health", "education":"Education", "health":"General health"}[domain]+"\nRecall (%)")
        handles, names=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,names,loc="lower center",ncol=4,frameon=False)
        fig.tight_layout(rect=(0,.10 if len(domains)==1 else .06,1,1))
        fig.savefig(out/(name+".pdf"), metadata={"CreationDate":None,"ModDate":None})
        fig.savefig(out/(name+".png"), dpi=170)
        plt.close(fig)
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    fig,axes=plt.subplots(1,3,figsize=(11.5,3.3),sharex=True)
    for ax,domain in zip(axes,DOMAINS):
        counts=d[d.domain==domain].D.round(1).value_counts().sort_index()
        ax.bar(counts.index,counts.values,width=.16,color="#0072B2")
        ax.axvline(3,color="#D55E00",linestyle="--",label="D trigger at 3")
        ax.set_title({"mental_health":"Mental health","education":"Education","health":"General health"}[domain])
        ax.set_xlabel("Mean of five D ratings"); ax.set_ylabel("Responses")
        ax.set_xticks([1,2,3,4,5]); ax.grid(axis="y",alpha=.2)
    fig.tight_layout()
    fig.savefig(out/"d_mean_distributions.pdf",metadata={"CreationDate":None,"ModDate":None})
    fig.savefig(out/"d_mean_distributions.png",dpi=170)
    plt.close(fig)


def write_report(out):
    comp=pd.read_csv(out/"complementarity.csv")
    paired=pd.read_csv(out/"paired_comparisons.csv")
    cutoff=pd.read_csv(out/"cutoff_diagnostics.csv")
    text=["# Post-review exploratory findings", "", "The original primary family remains unchanged. Added analyses were specified after inspecting the original results; all new intervals are exploratory pointwise 95%, not simultaneous or confirmatory. No ratings or original outputs were changed.", "", "## Complementarity at 20%", "",
          "| Domain | Criterion | H only | Markers only | Both | Fixed fusion / cases | Fusion minus markers recall, pp [95%] |",
          "|---|---|---:|---:|---:|---:|---|"]
    for r in comp[comp.budget==.2].itertuples():
        p=paired[(paired.domain==r.domain)&(paired.criterion==r.criterion)&(paired.metric=="fusion_minus_markers_recall")].iloc[0]
        text.append(f"| {r.domain} | {r.criterion} | {r.caught_h_only} | {r.caught_markers_only} | {r.caught_both} | {r.caught_fusion}/{r.concerns} | {100*p.estimate:+.1f} [{100*p.lo:+.1f}, {100*p.hi:+.1f}] |")
    text += ["", "H-only cases establish different observed selections, not a cost-free gain from taking the union. Fusion has the same exact capacity. No broad-D fusion improvement over markers is established; neither equivalence nor absence of useful information is established.", "", "## Direct paired workload differences", "", "Negative H-minus-comparator values mean fewer responses reviewed by H to reach 80% criterion recall. These are retrospective workloads with known labels, not deployable stopping rules.", ""]
    for r in paired[(paired.criterion=="D_ge3") & paired.metric.str.contains("workload")].itertuples():
        text.append(f"- {r.domain}, {r.metric}: {100*r.estimate:+.1f} pp [{100*r.lo:+.1f}, {100*r.hi:+.1f}], {r.valid_replicates}/{r.replicates} finite draws; sparse={r.sparse}.")
    text += ["", "## Label stability", "", "| Domain | Criterion | Within +/-0.2 | Exactly at cutoff | Split votes | Mean vs majority disagreement |", "|---|---|---:|---:|---:|---:|"]
    for r in cutoff.itertuples():
        text.append(f"| {r.domain} | {r.criterion} | {r.near_cutoff}/{r.n} | {r.exactly_cutoff} | {r.split_votes} | {r.mean_majority_disagree} |")
    text += ["", "All source ICC point estimates reconstruct from current long ratings. Source ordinal alpha and response-bootstrap confidence intervals are imported and labeled, not independently re-estimated. Reliability is not construct validity or personnel independence.", "", "## Text provenance", "", "The join replay reproduces all imported H scores, source filenames, and tiers. In education 359/415 rated/export pairs are byte-identical and 56 differ after normalization; in general health 412/415 are identical and three differ. Mental health has embedded scores without a separate historical input string. Export text association does not prove actual API scorer inputs.", "", "On the unchanged full batches at 20%, computing lexical features from export text instead of rated text leaves selected criterion counts unchanged for length, markers, and fixed rank fusion. This does not prove identical selected identities or correct joins. The separate identical-text subset analyses report both unchanged absolute capacity and unchanged fractional budget; neither identifies a causal effect of join error.", "", "## Scope", "", "No external study, fitted classifier, LLM judge, practical audit validation, or publication clearance is asserted. New learned comparators would need a separate grouped evaluation and cost account. The author handles venue disclosure and confirmation of intern non-participation safeguards."]
    (out/"findings.md").write_text("\n".join(text)+"\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--replicates",type=int,default=2000)
    parser.add_argument("--output",type=Path,default=OUT)
    args=parser.parse_args()
    if args.replicates<2000 and args.output.resolve()==OUT.resolve():
        raise ValueError("Pilot output must not replace final revision results")
    started=time.monotonic()
    args.output.mkdir(parents=True,exist_ok=True)
    before=source_hashes(ROOT)
    original={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/"facct/outputs").rglob("*") if p.is_file()}
    config=json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    r=pd.read_csv(ROOT/"analysis/processed/persona_ratings_long.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    d["cluster"]=d.domain+":"+d.prompt_id
    table=pd.read_csv(ROOT/"facct/outputs/tables/screening.csv")
    table["oracle_recall"]=np.minimum(1,table.selected/table.concerns.replace(0,np.nan))
    table["fraction_of_oracle"]=table.recall/table.oracle_recall.replace(0,np.nan)
    table["lift"]=table.precision/table.prevalence.replace(0,np.nan)
    table[["domain","criterion","policy","budget","n","concerns","selected","caught","recall","precision","prevalence","oracle_recall","fraction_of_oracle","lift"]].to_csv(args.output/"operating_context.csv",index=False)
    combined=[]
    for domain in DOMAINS:
        g=d[d.domain==domain]
        combined.extend(complementarity(features(g), labels(g,config), tie_keys(g.id,config["seed"]), config,domain))
    pd.DataFrame(combined).to_csv(args.output/"complementarity.csv",index=False)
    extra_bootstrap(d,config,args.replicates).to_csv(args.output/"paired_comparisons.csv",index=False)
    cutoff_diagnostics(d,r,config,args.output)
    text_audit(d,config,args.output)
    figures(args.output)
    write_report(args.output)
    assert before==source_hashes(ROOT), "Source data changed"
    assert original=={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/"facct/outputs").rglob("*") if p.is_file()}, "Frozen output changed"
    manifest={"status":"final" if args.replicates>=2000 else "pilot", "replicates":args.replicates,
        "seed":config["seed"], "runtime_seconds":round(time.monotonic()-started,2),
        "source_hashes":before, "frozen_output_hashes":original,
        "revision_sources":{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/"facct/revision").glob("*") if p.is_file()},
        "outputs":{p.name:sha(p) for p in args.output.glob("*") if p.is_file() and p.name!="manifest.json"}}
    (args.output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"status":manifest["status"],"runtime_seconds":manifest["runtime_seconds"],"source_and_frozen_outputs_unchanged":True}))


if __name__=="__main__":
    main()
