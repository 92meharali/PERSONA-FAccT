"""Generate completeness tables from unchanged source outputs and cached scores."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from analysis.extension_run import load, SEED, DOMAINS

DOM = dict(mental_health="Mental health", education="Education", health="General health")
CRIT = {"D_ge3":r"$\overline D\geq3$", "F_lt4":r"$\overline F<4$", "OA_lt4":r"$\overline{\mathrm{OA}}<4$"}
POL = dict(high_H="HumT", markers="Markers", length="Length", embed_sim="Similarity", nli_zero_shot="NLI",
           uniform_random="Uniform random", stratified_random="Stratified random")


def table(caption, label, cols, heading, rows):
    return "\n".join([r"\begin{table}[p]",r"\centering\footnotesize",r"\caption{"+caption+"}",
                      r"\label{"+label+"}",r"\begin{tabular}{"+cols+"}",r"\toprule",heading+r" \\",
                      r"\midrule"]+rows+[r"\bottomrule",r"\end{tabular}",r"\end{table}",""])


def main():
    p=argparse.ArgumentParser(); p.add_argument("--repo",type=Path,required=True); args=p.parse_args()
    out=Path("analysis_outputs/professor_revision"); out.mkdir(exist_ok=True)
    tab=Path("paper/tables")
    corpus,s,u,_=load(args.repo)
    cache={p:np.load(Path("analysis_outputs/cache")/f,allow_pickle=False) for p,f in
           (("embed_sim","embed_scores.npy"),("nli_zero_shot","nli_scores.npy"))}
    original=pd.read_csv(args.repo/"facct/outputs/tables/screening.csv")
    allrows=[]
    for domain in DOMAINS:
        g=corpus[corpus.domain.eq(domain)]
        X=s.features(g); scores=dict(high_H=X[:,0],length=X[:,1],markers=X[:,2])
        scores.update({p:arr[g.index] for p,arr in cache.items()})
        ties=s.tie_keys(g.id,SEED)
        rows=[]
        for crit,col,op in (("D_ge3","D",lambda x:x>=3),("F_lt4","F",lambda x:x<4),("OA_lt4","OA",lambda x:x<4)):
            y=op(g[col].to_numpy())
            for policy in ("high_H","markers","length","embed_sim","nli_zero_shot"):
                ap,auc,_=s.rank_metrics(y,scores[policy],s.order_scores(scores[policy],ties))
                assert np.isclose(ap,average_precision_score(y,scores[policy]))
                assert np.isclose(auc,roc_auc_score(y,scores[policy]))
                if policy in ("high_H","markers","length"):
                    old=original[(original.domain==domain)&(original.criterion==crit)&(original.policy==policy)&original.budget.eq(.2)].iloc[0]
                    assert np.isclose(ap,old.ap) and np.isclose(auc,old.auc)
                rows.append(f"{CRIT[crit]} & {POL[policy]} & {y.sum()} & {y.mean():.3f} & {ap:.3f} & {auc:.3f} "+r"\\")
                allrows.append(dict(domain=domain,criterion=crit,policy=policy,P=int(y.sum()),prevalence=y.mean(),ap=ap,auc=auc))
            rows.append(r"\addlinespace")
        (tab/f"ranking_{domain}.tex").write_text(table(
            f"{DOM[domain]}: full-ranking average precision (AP) and ROC-AUC with class prevalence. Scores and labels are unchanged; tie-aware metrics were independently checked against scikit-learn. These point estimates are descriptive and do not replace matched-budget comparisons.",
            f"tab:ranking_{domain}","llrrrr",r"Criterion & Policy & Cases & Prevalence & AP & ROC-AUC",rows))
    pd.DataFrame(allrows).to_csv(out/"all_rank_metrics.csv",index=False)
    ties=pd.read_csv(args.repo/"facct/outputs/tables/tie_sensitivity.csv")
    summary=ties.groupby(["domain","criterion","policy"]).agg(seeds=("seed","nunique"),
             caught_min=("caught","min"),caught_max=("caught","max"),slots_min=("selected","min"),slots_max=("selected","max")).reset_index()
    assert summary.seeds.eq(100).all()
    summary.to_csv(out/"tie_summary.csv",index=False)
    rows=[]
    for domain in DOMAINS:
        for crit in CRIT:
            r=summary[(summary.domain==domain)&(summary.criterion==crit)].set_index("policy")
            cells=[f"{r.loc[pol,'caught_min']:.0f}--{r.loc[pol,'caught_max']:.0f}" for pol in ("high_H","markers","length")]
            rows.append(f"{DOM[domain]} & {CRIT[crit]} & "+" & ".join(cells)+r" \\")
    (tab/"tie_summary.tex").write_text(table("Original fixed policies: minimum and maximum concern captures across 100 tie-breaking seeds at the same 20\\% budget. Each seed changes tie resolution, not scores, labels or capacity.","tab:ties","llrrr",r"Domain & Criterion & HumT & Markers & Length",rows))
    pooled=original[(original.domain=="pooled")&original.budget.eq(.2)].copy()
    assert len(pooled)==15, f"Unexpected pooled cells: {len(pooled)}"
    pooled.to_csv(out/"pooled_reference.csv",index=False)
    rows=[]
    for r in pooled.itertuples():
        rows.append(f"{CRIT[r.criterion]} & {POL[r.policy]} & {r.concerns:.0f} & {r.selected:.0f} & {r.caught:.1f} & {100*r.recall:.1f} & $[{100*r.recall_lo:.1f}, {100*r.recall_hi:.1f}]$ "+r"\\")
    (tab/"pooled_reference.tex").write_text(table("Secondary pooled analysis at 20\\% (298/1,490 slots). Random counts are expectations; domain-stratified random allocates slots in proportion to domain sizes using largest remainders. Pointwise 95\\% intervals use domain-stratified prompt resampling. The observed domain mixture is not a deployment prevalence estimate.","tab:pooled","llrrrrl",r"Criterion & Policy & Cases & Slots & Caught & Recall (\%) & Interval",rows))
    hx=pd.read_csv("analysis_outputs/heldout_contrasts.csv")
    rows=[]
    for domain in DOMAINS:
        for criterion,tex in (("D>=3",CRIT["D_ge3"]),("F<4",CRIT["F_lt4"]),("OA<4",CRIT["OA_lt4"])):
            cells=[]
            for model in ("lex+emb+H","lex+emb16+H"):
                r=hx[(hx.domain==domain)&(hx.criterion==criterion)&(hx.model==model)].iloc[0]
                cells.append(f"${r.diff_pp:+.1f} [{r.lo_pp:+.1f}, {r.hi_pp:+.1f}]$")
            rows.append(f"{DOM[domain]} & {tex} & "+" & ".join(cells)+r" \\")
    (tab/"semantic_increments.tex").write_text(table("All 18 HumT additions to embedding-augmented screens. Recall differences in percentage points are (Lex+Emb+H) minus (Lex+Emb), and the corresponding Emb16 contrast. Intervals use 1,000 paired refitted domain-level prompt resamples retaining fold membership; all include zero. The Emb16 representation was selected after inspecting the full-dimensional results.","tab:semantic_increments","llll",r"Domain & Criterion & Full embedding & 16-component embedding",rows))
    budgets=pd.read_csv(out/"mental_health_budget_metrics.csv")
    diffs=pd.read_csv(out/"mental_health_budget_contrasts.csv")
    rows=[]
    for r in budgets[budgets.criterion.eq("followup")].itertuples():
        name="Random" if r.policy=="random" else POL[r.policy]
        rows.append(f"{100*r.budget:.0f} & {r.selected} & {name} & {r.caught:.1f} & {100*r.recall:.1f} & $[{100*r.lo:.1f}, {100*r.hi:.1f}]$ & {r.finite} "+r"\\")
    (tab/"followup_budgets_all.tex").write_text(table("All policies and budgets for the 19-case follow-up target. Recall intervals are pointwise 95\\% from 2,000 paired prompt draws; finite counts are shown. Random entries describe analytical expectations, not variability of an individual random queue.","tab:followup_budgets_all","rrlrrlr",r"Budget (\%) & Slots & Policy & Caught & Recall (\%) & Interval & Draws",rows))
    rows=[]
    for r in diffs[diffs.criterion.eq("followup") & diffs.budget.eq(.2)].itertuples():
        a="Random" if r.policy=="random" else POL[r.policy]
        b="Random" if r.versus=="random" else POL[r.versus]
        rows.append(f"{a} & {b} & ${r.diff_pp:+.1f}$ & $[{r.lo_pp:+.1f}, {r.hi_pp:+.1f}]$ & {r.finite} "+r"\\")
    (tab/"semantic_followup_all.tex").write_text(table("Complete follow-up contrasts at 132 slots. Each row is first policy minus comparator recall, in percentage points. Intervals are exploratory pointwise 95\\%, paired on the same resampled prompts, without multiplicity adjustment.","tab:semantic_followup_all","llrlr",r"Policy & Comparator & Difference & Interval & Draws",rows))
    rows=[]
    for r in budgets[budgets.criterion.eq("D")].itertuples():
        name="Random" if r.policy=="random" else POL[r.policy]
        rows.append(f"{100*r.budget:.0f} & {r.selected} & {name} & {r.caught:.1f} & {100*r.recall:.1f} & $[{100*r.lo:.1f}, {100*r.hi:.1f}]$ "+r"\\")
    (tab/"broad_budget_all.tex").write_text(table("All six mental-health policies and four capacities for broad D (165 cases). Exploratory pointwise 95\\% intervals use the same 2,000 prompt draws as the semantic follow-up extension. These later-seed marginal intervals do not replace the original adjusted primary contrasts.","tab:broad_budget_all","rrlrrl",r"Budget (\%) & Slots & Policy & Caught & Recall (\%) & Interval",rows))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family":"serif", "font.size":9, "pdf.fonttype":42})
    for domains,name in [(["mental_health"],"mental_health_budgets"),(["education","health"],"transfer_budgets")]:
        fig,axes=plt.subplots(len(domains),3,figsize=(9.5,2.9*len(domains)),squeeze=False,sharex=True,sharey=True)
        for i,domain in enumerate(domains):
            for j,criterion in enumerate(CRIT):
                ax=axes[i,j]
                for policy,color,marker in [("high_H","#0072B2","o"),("length","#D55E00","s"),("markers","#009E73","^"),("uniform_random","#555555",".")]:
                    r=original[(original.domain==domain)&(original.criterion==criterion)&(original.policy==policy)].sort_values("budget")
                    ax.plot(100*r.budget,100*r.recall,color=color,marker=marker,label=POL[policy],markersize=4)
                    if policy=="high_H": ax.fill_between(100*r.budget,100*r.recall_lo,100*r.recall_hi,color=color,alpha=.12)
                title={"D_ge3":r"$\overline{D}\geq 3$","F_lt4":r"$\overline{F}<4$","OA_lt4":r"$\overline{\mathrm{OA}}<4$"}[criterion]
                ax.set_title(title+f"\n{int(r.iloc[0].concerns)} cases / {int(r.iloc[0].n)} responses")
                ax.set_ylim(0,105); ax.set_xticks([5,10,20,30]); ax.grid(alpha=.2); ax.set_xlabel("Review budget (%)")
                if j==0: ax.set_ylabel(DOM[domain]+"\nRecall (%)")
        handles,names=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,names,loc="lower center",ncol=4,frameon=False)
        fig.tight_layout(rect=(0,.12 if len(domains)==1 else .06,1,1))
        fig.savefig(Path("paper/figures")/(name+".pdf"),metadata={"CreationDate":None,"ModDate":None})
        plt.close(fig)
    print("Verified ranking, pooled, tie and 18 incremental-comparison tables generated.")


if __name__=="__main__": main()
