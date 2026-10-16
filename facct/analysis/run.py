"""Run without touching any source annotation, CHI manuscript or CHI output."""
import argparse
import importlib.metadata
import json
import platform
import subprocess
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import model_comparisons, reporting, sample_cases, sensitivity
from .screening import labels, random_draw_limits
from .uncertainty import bootstrap
from .validate_inputs import sha, source_hashes, validate

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF = Path.home() / "Downloads/Beyond_Human_Likeness__A_Context_Aware_Framework_for_Evaluating_Appropriateness_in_Anthropomorphic_AI_Responses__2_-5.pdf"


def figures(table, out):
    colors = {"high_H":"#0072B2", "length":"#D55E00", "markers":"#009E73", "uniform_random":"#555555"}
    fig, axes = plt.subplots(3, 3, figsize=(12, 10), sharex=True, sharey=True, layout="constrained")
    for row, domain in enumerate(("mental_health","education","health")):
        for col, criterion in enumerate(("D_ge3","F_lt4","OA_lt4")):
            ax = axes[row,col]
            group = table[(table.domain==domain)&(table.criterion==criterion)]
            first = group.iloc[0]
            for policy, color in colors.items():
                g = group[group.policy == policy].sort_values("budget")
                styles={"high_H":("o","-"), "length":("s","--"), "markers":("^","-."), "uniform_random":(".",":")}
                marker,style=styles[policy]
                ax.plot(g.selected/g.n*100, g.recall, marker=marker, linestyle=style, label=policy, color=color)
                if policy=="high_H":
                    ax.fill_between(g.selected/g.n*100, g.recall_lo, g.recall_hi, color=color, alpha=.16)
            ax.set_title(f"{domain.replace('_',' ')} | {criterion}\n{int(first.concerns)}/{int(first.n)} concerns; {int(first.concern_clusters)} clusters", fontsize=9)
            ax.grid(alpha=.2)
            ax.set_ylim(0,1)
            if row==2: ax.set_xlabel("Batch selected for review (%)")
            if col==0: ax.set_ylabel("Concern recall")
    handles, names = axes[0,0].get_legend_handles_labels()
    fig.legend(handles,names,loc="outside lower center",ncol=4)
    fig.suptitle("Proposed review allocation: recall is criterion- and domain-dependent\nShading: HumT pointwise 95% paired prompt-cluster bootstrap intervals",fontsize=13)
    for suffix in ("png","pdf"):
        metadata={"CreationDate":None,"ModDate":None} if suffix=="pdf" else None
        fig.savefig(out / "figures" / f"recall_budgets.{suffix}",dpi=180,metadata=metadata)
    plt.close(fig)
    g = table[(table.policy=="high_H") & (table.budget==.2) & (table.domain!="pooled")].copy()
    fig, ax = plt.subplots(figsize=(9,5),layout="constrained")
    x = np.arange(len(g))
    ax.barh(x,g.caught,label="Concern cases selected",color="#0072B2")
    ax.barh(x,g.missed,left=g.caught,label="Concern cases unreviewed",color="#D55E00")
    ax.set_yticks(x,[f"{r.domain} | {r.criterion}" for r in g.itertuples()])
    ax.set_xlabel("Responses meeting the specified concern criterion")
    ax.set_title("20% high-H review budget: selected versus unreviewed concern cases")
    ax.legend(loc="lower right")
    fig.savefig(out / "figures/selected_and_missed.png",dpi=180)
    plt.close(fig)


def report(table, out, replicates, elapsed):
    g = table[(table.policy=="high_H") & (table.budget==.2) & (table.domain!="pooled")]
    text = ["# Screening simulation results", "", f"Exploratory reuse of PERSONA. {replicates:,} paired prompt-cluster bootstrap replicates; computational runtime {elapsed:.1f} seconds before report/manifest finalization.",
            "", "## 20% reference budget", "", "Intervals below are pointwise 95%, not simultaneous. Random recall is an exact expectation at the same integer budget, not one sampled draw.", "",
            "| Domain | Criterion | Selected / n | Caught / concerns | Recall (95% CI) | Expected random recall | Difference (95% CI) | Missed |", "|---|---|---:|---:|---|---:|---|---:|"]
    for r in g.itertuples():
        text.append(f"| {r.domain} | {r.criterion} | {int(r.selected)}/{int(r.n)} | {int(r.caught)}/{int(r.concerns)} | {r.recall:.3f} [{r.recall_lo:.3f}, {r.recall_hi:.3f}] | {r.selected/r.n:.3f} | {r.delta_random:+.3f} [{r.delta_random_lo:+.3f}, {r.delta_random_hi:+.3f}] | {int(r.missed)} |")
    text += ["", "## Primary comparison family", "", "D >= 3 only, high_H minus expected uniform random recall at 20%. Bonferroni 98.3333% percentile intervals across three domains; already-explored data and approximate intervals prevent confirmatory claims.", ""]
    for r in g[g.criterion=="D_ge3"].itertuples():
        text.append(f"- {r.domain}: {r.delta_random:+.3f}, adjusted interval [{r.primary_adjusted_delta_lo:+.3f}, {r.primary_adjusted_delta_hi:+.3f}]; {int(r.concern_clusters)} concern-bearing clusters. Sparse flag: {r.sparse}.")
    text += ["", "## Simple baselines", "", "Paired pointwise 95% intervals for the difference in recall (HumT minus baseline), D >= 3 at 20%:", ""]
    for r in g[g.criterion=="D_ge3"].itertuples():
        text.append(f"- {r.domain}: versus length {r.delta_length:+.3f} [{r.delta_length_lo:+.3f}, {r.delta_length_hi:+.3f}]; versus markers {r.delta_markers:+.3f} [{r.delta_markers_lo:+.3f}, {r.delta_markers_hi:+.3f}].")
    text += ["", "## Interpretation and limits", "", "These estimates concern review allocation for existing rubric judgments, not user harm or successful interventions. Useful enrichment and missed cases can coexist. Domain fit, anthropomorphic implication risk, and holistic appropriateness are separate criteria. The data do not establish real organizational use of HumT screening.",
             "", "screening.csv includes precision, missed counts, unselected prevalence, AP/AUC, target-recall workload, uncertainty and valid replicate counts. random_draw_intervals.csv reports hypergeometric variability for one random draw, not an uncertainty interval for expected random performance. Bootstrap intervals are conditional on the fixed released ratings; rater/threshold sensitivities are separate.",
             "", "Sensitivity tables include anchor thresholds, 3/5 and 5/5 votes, individual raters, tie seeds, join provenance, conditions/scenarios/models, exact criterion intersections, and continuous relationships. Context point estimates are descriptive; small cells do not justify rankings. Model comparisons restrict primary pairings to complete three-model prompts. Mixtures and review-cost ratios are hypothetical.",
             "", "## Decision gates", "", "1. Computational feasibility: passed for the released corpus. Historical provenance is only provisionally linked: matching repository supplement bytes and manuscript numbers do not authenticate what was submitted. Resolve collection-history/payment records and confirm the submitted supplement before definitive methods claims.",
             "2. Scientific value: the screening question is computable and can reveal useful criterion-specific enrichment; assess all baselines and sensitivities, not only comparisons favorable to HumT.",
             "3. New contribution: not yet established as an independent paper. This is the same corpus and concern constructs as CHI. External evaluation and a tested decision artifact remain pending. Treat the current package as a methods-study candidate, not proven submission novelty.",
             "4. Eligibility: no self-certification. Official policies and any written chair guidance must govern. No communication or submission has been sent."]
    (out / "reports/results.md").write_text("\n".join(text)+"\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output", type=Path, default=ROOT / "facct/outputs")
    args = parser.parse_args()
    if args.replicates < 2:
        parser.error("At least two bootstrap replicates are needed")
    out = args.output.resolve()
    if not out.is_relative_to(ROOT / "facct"):
        parser.error("Outputs must stay under facct/; CHI sources are protected")
    if args.replicates < 2000 and out == ROOT / "facct/outputs":
        parser.error("Pilot runs require a different --output under facct/")
    for part in ("tables", "figures", "reports"):
        (out / part).mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    config_path = ROOT / "facct/protocol/criteria.yaml"
    config = json.loads(config_path.read_text())
    before = source_hashes(ROOT)
    d, r, pdf = validate(ROOT,out,args.pdf)
    tables, criterion_comparisons = [], []
    for domain, frame in list(d.groupby("domain",sort=True))+[("pooled",d)]:
        print(f"Bootstrap {domain}: {len(frame)} responses; {args.replicates} draws",flush=True)
        result = bootstrap(frame, config, args.replicates)
        criterion_comparisons.extend(dict(domain=domain,**row) for row in result.attrs.pop("criterion_comparisons"))
        result.insert(0,"domain",domain)
        y = labels(frame,config)
        negative_clusters = {criterion: frame.loc[~y[:,j],"cluster"].nunique() for j,criterion in enumerate(config["criteria"])}
        result["nonconcern_clusters"] = result.criterion.map(negative_clusters)
        result["sparse"] = (result.concern_clusters < config["minimum_concern_clusters_for_comparison"]) | (result.nonconcern_clusters < config["minimum_nonconcern_clusters_for_comparison"])
        result["prevalence"] = result.concerns/result.n
        result["random_values_are_expectations"] = result.policy.str.contains("random")
        tables.append(result)
    results = pd.concat(tables,ignore_index=True)
    results.to_csv(out / "tables/screening.csv",index=False)
    pd.DataFrame(criterion_comparisons).to_csv(out / "tables/criterion_recall_differences.csv",index=False)
    random_rows=[]
    for row in results[results.policy=="uniform_random"].itertuples():
        lo,hi=random_draw_limits(int(row.n),int(row.concerns),int(row.selected))
        random_rows.append(dict(domain=row.domain,criterion=row.criterion,budget=row.budget,expected_caught=row.caught,draw_caught_lo=lo,draw_caught_hi=hi,interpretation="central 95% hypergeometric prediction range for one exact-budget random draw"))
    pd.DataFrame(random_rows).to_csv(out / "tables/random_draw_intervals.csv",index=False)
    sensitivity.run(d,r,config,out)
    sensitivity.scenarios(results,out)
    model_comparisons.run(d,config,args.replicates,out)
    sample_cases.run(d,config,out)
    reporting.write(results,out)
    figures(results,out)
    elapsed=time.perf_counter()-start
    report(results,out,args.replicates,elapsed)
    after=source_hashes(ROOT)
    if before != after:
        raise RuntimeError("Source hashes changed during run")
    code_files=list((ROOT / "facct/analysis").glob("*.py"))+list((ROOT / "facct/protocol").glob("*"))+list((ROOT / "facct/tests").glob("*.py"))+[ROOT/"facct/requirements.txt"]
    manifest=dict(protocol=config["version"],analysis_date="2026-10-02",seed=config["seed"],replicates=args.replicates,run_kind="final_exploratory" if args.replicates>=2000 else "pilot",runtime_seconds=time.perf_counter()-start,
                  git_revision=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
                  command=f"python -m facct.analysis.run --replicates {args.replicates}",python=platform.python_version(),
                  software={p:importlib.metadata.version(p) for p in ("numpy","pandas","scipy","scikit-learn","matplotlib","pypdf")},
                  source_hashes=before,code_and_protocol_hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(code_files)},submitted_pdf=pdf,
                  output_hashes={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob("*")) if p.is_file() and p.suffix in (".csv",".png",".pdf",".md")},
                  sources_unchanged=True,human_study_status="not conducted")
    (out / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"Completed in {manifest['runtime_seconds']:.1f}s; sources unchanged. Outputs: {out}",flush=True)


if __name__ == "__main__":
    main()
