"""Generate review-facing summaries without changing frozen computations."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/"facct/paper/overleaf"
DOMAINS=(("mental_health","Mental health"),("education","Education"),("health","General health"))
CRITERIA=(("D_ge3","D"),("F_lt4","Fit"),("OA_lt4","OA"))


def save(fig,name):
    for ext in ("pdf","png"):
        fig.savefig(DEST/"figures"/(name+"."+ext),dpi=180,
                    metadata={"CreationDate":None,"ModDate":None} if ext=="pdf" else None)
    plt.close(fig)


def figures():
    original=pd.read_csv(ROOT/"facct/outputs/tables/screening.csv")
    conditional=pd.read_csv(ROOT/"facct/conditional/outputs/conditional_lift.csv")
    fig,axes=plt.subplots(1,2,figsize=(11,5.3),sharey=True,layout="constrained")
    labels=[]
    for i,(domain,title) in enumerate(DOMAINS):
        for j,(criterion,label) in enumerate(CRITERIA):
            pos=i*3+j
            r=original[original.domain.eq(domain)&original.criterion.eq(criterion)&original.policy.eq("high_H")&original.budget.eq(.2)].iloc[0]
            c=conditional[conditional.domain.eq(domain)&conditional.criterion.eq(criterion)&conditional.budget.eq(.2)].iloc[0]
            labels.append(f"{title}: {label}{' *' if r['sparse'] else ''}\n{int(r.concerns)} cases / {int(r.concern_clusters)} prompts")
            for ax,value,lo,hi,color in ((axes[0],r.delta_markers,r.delta_markers_lo,r.delta_markers_hi,"#0072B2"),
                                        (axes[1],c.conditional_lift,c.lo,c.hi,"#B35400")):
                ax.hlines(pos,lo*100,hi*100,color=color,lw=1.6)
                ax.plot(value*100,pos,"o",color=color,mfc="white" if r['sparse'] else color,ms=5)
    axes[0].set_yticks(range(9),labels,fontsize=8)
    axes[0].invert_yaxis()
    for ax in axes:
        ax.axvline(0,color="#444444",lw=.8,ls="--")
        ax.grid(axis="x",alpha=.18)
        for y in (2.5,5.5): ax.axhline(y,color="#cccccc",lw=.5)
        ax.set_xlabel("Paired recall difference (percentage points)",fontsize=9)
    axes[0].set_title("A. HumT minus markers\nFull-domain queues: 132 / 83 / 83 slots",fontsize=10,color="#0072B2")
    axes[1].set_title("B. Adding HumT to lexical LR\nHeld-out batches: 130 / 80 / 80 total slots",fontsize=10,color="#B35400")
    fig.suptitle("Different procedures, capacities and axis scales: do not compare panels directly\nExploratory 95% intervals; * fewer than 10 positive or negative supporting prompts",fontsize=10)
    save(fig,"paired_summary")

    fig,axes=plt.subplots(1,3,figsize=(11,3.9),sharey=True,layout="constrained")
    colors=("#0072B2","#B35400","#008060","#555555")
    policies=("high_H","length","markers","uniform_random")
    names=("HumT","Length","Markers","Random (expected)")
    targets=(50,80,90,100)
    for ax,(domain,title) in zip(axes,DOMAINS):
        d=original[original.domain.eq(domain)&original.criterion.eq("D_ge3")&original.budget.eq(.2)]
        for policy,name,color,marker in zip(policies,names,colors,("o","s","^","d")):
            r=d[d.policy.eq(policy)].iloc[0]
            means=[100*r[f"workload_{t}"] for t in targets]
            ax.plot(targets,means,color=color,marker=marker,label=name,lw=1,ms=4)
            for t,mean in zip(targets,means):
                ax.vlines(t,100*r[f"workload_{t}_lo"],100*r[f"workload_{t}_hi"],color=color,lw=.8,alpha=.6)
        r=d.iloc[0]
        ax.set_title(f"{title}\n{int(r.concerns)} D cases / {int(r.concern_clusters)} prompts",fontsize=10)
        ax.set_xticks(targets)
        ax.set_xlabel("Target recall (%)")
        ax.grid(alpha=.15)
        ax.set_ylim(0,105)
    axes[0].set_ylabel("Required batch fraction (%)")
    fig.legend(*axes[0].get_legend_handles_labels(),loc="outside lower center",ncol=4,fontsize=9)
    fig.suptitle("Retrospective workload at four specified targets\nAll policies: exploratory pointwise 95% intervals; lines only connect evaluated targets",fontsize=10)
    save(fig,"workload_targets")


def tables(table):
    d=pd.read_csv(ROOT/"facct/allocation/outputs/category_coverage.csv")
    pairs=pd.read_csv(ROOT/"facct/allocation/outputs/paired_policy_differences.csv")
    rows,slots=[],[]
    for domain,title in DOMAINS:
        for condition in ("natural","adversarial"):
            a=d[d.domain.eq(domain)&d.grouping.eq("condition")&d.group.eq(condition)&d.criterion.eq("D_ge3")]
            h=a[a.policy.eq("high_H")].iloc[0]; m=a[a.policy.eq("markers")].iloc[0]
            slots.append(" & ".join([title if condition=="natural" else "",condition.capitalize(),str(h.n),str(int(h.selected)),str(int(m.selected))])+r" \\")
        for criterion,label in CRITERIA:
            for condition in ("natural","adversarial"):
                a=d[d.domain.eq(domain)&d.grouping.eq("condition")&d.group.eq(condition)&d.criterion.eq(criterion)]
                h=a[a.policy.eq("high_H")].iloc[0]; m=a[a.policy.eq("markers")].iloc[0]
                p=pairs[pairs.domain.eq(domain)&pairs.grouping.eq("condition")&pairs.group.eq(condition)&pairs.criterion.eq(criterion)].iloc[0]
                delta="Undefined" if not np.isfinite(p.H_minus_markers) else f"{100*p.H_minus_markers:+.1f} [{100*p.lo:+.1f}, {100*p.hi:+.1f}]"
                flag=r"$^{\dagger}$" if h['sparse'] else ""
                rows.append(" & ".join([title+" / "+label if condition=="natural" else "",condition.capitalize()+flag,
                    f"{int(h.concerns)}/{int(h.concern_clusters)}",str(int(h.caught)),str(int(m.caught)),delta])+r" \\")
    table("common_queue_slots","llrrr",r"Domain & Condition & Responses & HumT slots & Marker slots",slots,
          r"Where review slots go in the common full-domain queues: 132 mental-health slots and 83 in each other domain. Category counts are projections of one queue, not independent quotas. Selection is label-free and identical across D/F/OA endpoints; natural/adversarial prompts are unmatched.")
    table("common_queue_conditions","lllrrr",r"Domain / target & Condition & Cases/prompts & H caught & M caught & H--M recall, pp [95\%]",rows,
          r"All condition-by-criterion results projected from common queues. Cases/prompts gives concern responses and supporting prompts. H and M denote HumT and markers; paired differences are exploratory pointwise, not simultaneous. $\dagger$ marks fewer than ten positive or negative supporting prompts; a zero-concern group has undefined recall, not perfect or zero coverage. All policies and model/scenario categories remain in the computational record.")
    macros=[]
    for domain,criterion,policy,name in (("mental_health","OA_lt4","high_H","MHQueueOAGap"),
                                       ("health","F_lt4","high_H","GHQueueFitGapH"),
                                       ("health","F_lt4","markers","GHQueueFitGapM")):
        r=d[d.domain.eq(domain)&d.criterion.eq(criterion)&d.policy.eq(policy)&d.grouping.eq("condition")&d.group.eq("adversarial")].iloc[0]
        field="group_minus_complement_recall"
        value=f"{100*r[field]:+.1f} [{100*r[field+'_lo']:+.1f}, {100*r[field+'_hi']:+.1f}]"
        macros.append("\\newcommand{\\"+name+"}{"+value+"}")
    with (DEST/"tables/numbers.tex").open("a") as stream:
        stream.write("\n% Common-queue adversarial-minus-natural recall, exploratory pp.\n"+"\n".join(macros)+"\n")
        p=pairs[pairs.domain.eq("health")&pairs.criterion.eq("F_lt4")&pairs.grouping.eq("condition")&pairs.group.eq("natural")].iloc[0]
        value=f"{100*p.H_minus_markers:+.1f} [{100*p.lo:+.1f}, {100*p.hi:+.1f}]"
        stream.write("\\newcommand{\\GHQueueNaturalFitContrast}{"+value+"}\n")


def build(table):
    figures()
    tables(table)
