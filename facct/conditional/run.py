"""Reproduce the conditional-lift study and all trained comparison cells."""
from pathlib import Path
import argparse
import importlib.metadata
import json
import subprocess
import time

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from facct.analysis.screening import capacity, features, labels, tie_keys
from facct.analysis.uncertainty import summarize
from facct.analysis.validate_inputs import source_hashes, sha
from .analysis import METRICS, POLICIES, bootstrap, crossfit, evaluate, group_folds, serialize_audit


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "facct/conditional/outputs"
DOMAINS = ("mental_health", "education", "health")


def frozen_hashes():
    result = source_hashes(ROOT)
    for directory in ("facct/outputs", "facct/revision"):
        result.update({str(p.relative_to(ROOT)): sha(p) for p in (ROOT/directory).rglob("*")
                       if p.is_file() and "__pycache__" not in str(p)})
    return result


def domain_study(d, criteria, config):
    X, Y = features(d), labels(d, criteria)
    ids, clusters = d.id.to_numpy(), d.cluster.to_numpy()
    folds = group_folds(clusters, config["seed"], config["folds"])
    keys = tie_keys(ids, config["seed"])
    scores, audits, _ = crossfit(X, Y, folds, clusters, config, keep_audit=True)
    point, fold_records = evaluate(scores, Y, folds, keys, config["budgets"])
    domain = d.domain.iloc[0]
    samples, fallbacks = bootstrap(X, Y, folds, clusters, ids, config,
        lambda n: print(f"{domain}: {n}/{config['replicates']} paired refit draws", flush=True))
    criterion_names = list(criteria["criteria"])
    rows, comparisons, predictions, replicate_records = [], [], [], []
    for b, budget in enumerate(config["budgets"]):
        k = sum(capacity(int(sum(folds==f)), budget) for f in range(config["folds"]))
        for j, criterion in enumerate(criterion_names):
            p = int(Y[:, j].sum())
            pc, nc = len(np.unique(clusters[Y[:,j]])), len(np.unique(clusters[~Y[:,j]]))
            for policy_idx, policy in enumerate(POLICIES):
                row = dict(domain=domain, criterion=criterion, policy=policy, budget=budget,
                    n=len(d), concerns=p, concern_clusters=pc, nonconcern_clusters=nc,
                    selected=k, actual_budget=k/len(d), sparse=min(pc,nc)<config["minimum_class_clusters"])
                for m, metric in enumerate(METRICS):
                    row[metric] = point[b,j,policy_idx,m]
                    lo,hi,valid = summarize(samples[:,j,policy_idx,m]) if budget==config["reference_budget"] else (np.nan,np.nan,0)
                    row.update({metric+"_lo":lo, metric+"_hi":hi, metric+"_valid":valid})
                row["delta_random"] = point[b,j,policy_idx,1]-point[b,j,6,1]
                lo,hi,valid = summarize(samples[:,j,policy_idx,1]-samples[:,j,6,1]) if budget==config["reference_budget"] else (np.nan,np.nan,0)
                row.update(delta_random_lo=lo,delta_random_hi=hi,delta_random_valid=valid,
                    training_required=policy in ("reduced_lr","extended_lr"))
                rows.append(row)
            delta = point[b,j,5,1]-point[b,j,4,1]
            lo,hi,valid = summarize(samples[:,j,5,1]-samples[:,j,4,1]) if budget==config["reference_budget"] else (np.nan,np.nan,0)
            comparisons.append(dict(domain=domain,criterion=criterion,budget=budget,n=len(d),selected=k,
                concerns=p,concern_clusters=pc,nonconcern_clusters=nc,
                reduced_caught=point[b,j,4,0],extended_caught=point[b,j,5,0],
                reduced_recall=point[b,j,4,1],extended_recall=point[b,j,5,1],
                conditional_lift=delta,lo=lo,hi=hi,valid_replicates=valid,
                sparse=min(pc,nc)<config["minimum_class_clusters"],
                inference="exploratory pointwise; fixed-partition conditional" if budget==config["reference_budget"] else "descriptive; no interval"))
    for j, criterion in enumerate(criterion_names):
        for i in range(len(d)):
            predictions.append(dict(domain=domain,id=ids[i],cluster=clusters[i],fold=folds[i],criterion=criterion,
                concern=int(Y[i,j]),**{policy:scores[i,j,k] for k,policy in enumerate(POLICIES[:6])}))
        for b in range(config["replicates"]):
            replicate_records.append(dict(domain=domain,criterion=criterion,replicate=b,
                reduced_recall=samples[b,j,4,1],extended_recall=samples[b,j,5,1],
                conditional_lift=samples[b,j,5,1]-samples[b,j,4,1],fallback_fits_all_criteria=int(fallbacks[b])))
    for row in audits+fold_records:
        row["domain"] = domain
        row["criterion"] = criterion_names[row.pop("criterion_index")]
    assignment=d[["id","cluster","domain"]].copy()
    assignment["fold"] = folds
    split_rows=[]
    for seed in config["split_sensitivity_seeds"]:
        f = group_folds(clusters, seed, config["folds"])
        s,_,fallback = crossfit(X,Y,f,clusters,config)
        v,_=evaluate(s,Y,f,keys,[config["reference_budget"]])
        for j,criterion in enumerate(criterion_names):
            split_rows.append(dict(domain=domain,criterion=criterion,seed=seed,
                selected=sum(capacity(int(sum(f==k)),config["reference_budget"]) for k in range(config["folds"])),
                reduced_caught=v[0,j,4,0],extended_caught=v[0,j,5,0],
                conditional_lift=v[0,j,5,1]-v[0,j,4,1],fallback_fits=fallback))
    return rows,comparisons,predictions,audits,fold_records,assignment,replicate_records,split_rows


def report(out):
    comparison=pd.read_csv(out/"conditional_lift.csv")
    sensitivity=pd.read_csv(out/"split_sensitivity.csv")
    audits=pd.read_csv(out/"fit_audit.csv")
    text=["# Conditional-lift results", "", "Exploratory post-review analysis; original primary family unchanged. Conditional lift is the absolute recall difference when adding H to a fixed logistic screen using markers and log-length, evaluated in common held-out prompt batches. It is not a causal effect or universal information test.", "", "## All reference-budget comparisons", "",
        "| Domain | Criterion | Slots | Reduced / cases | Extended / cases | Recall change, pp [95%] | Positive prompts | Sparse | Split range, pp |",
        "|---|---|---:|---:|---:|---|---:|---|---|"]
    for r in comparison[comparison.budget==.2].itertuples():
        s=sensitivity[(sensitivity.domain==r.domain)&(sensitivity.criterion==r.criterion)]
        text.append(f"| {r.domain} | {r.criterion} | {r.selected}/{r.n} | {r.reduced_caught:g}/{r.concerns} | {r.extended_caught:g}/{r.concerns} | {100*r.conditional_lift:+.1f} [{100*r.lo:+.1f}, {100*r.hi:+.1f}] | {r.concern_clusters} | {r.sparse} | [{100*s.conditional_lift.min():+.1f}, {100*s.conditional_lift.max():+.1f}] |")
    text += ["", "The ten alternative partition results are sensitivity, not independent replication, a confidence interval, or a best-seed selection. Read the full seed-level table. All nine cells are reported, including sparse and negative effects.", "", "## Interpretation boundaries", "",
        "- Reduced and extended models share training prompts, labels, settings, and test quotas. Scalers are fitted on training data only; no tuning or threshold optimization is performed.",
        "- The 2,000 paired resamples retain original fold membership, resample whole prompts within folds, and refit both models. Intervals remain approximate and conditional on this partition, source judgments, and observed distribution. They are not independent-sample tests or simultaneous nine-cell coverage.",
        "- Counts aggregate held-out batches. Per-batch rounding means total selected count can differ from the original full-domain simulation. All competing fixed policies are re-evaluated in the same held-out batches; do not compare trained recall directly with the original table as if capacities/batches were identical.",
        "- Separate policies are trained for each criterion. The learned scores are ranking tools for these labels, not calibrated harm probabilities. A null or negative incremental result does not establish conditional independence or no possible value from H.",
        "- Different selected cases in the earlier overlap table are not proof of incremental improvement. The paired trained comparison, not a larger union, addresses the specified added-value question.",
        "", "## Label acquisition and safeguards", ""]
    for domain in DOMAINS:
        a=audits[audits.domain==domain]
        text.append(f"- {domain}: each fitted model uses {a.training_responses.min()}-{a.training_responses.max()} labeled training responses ({a.underlying_training_ratings.min()}-{a.underlying_training_ratings.max()} underlying criterion ratings). Labels are reused across fits; these numbers must not be summed as separate annotation purchases. Observed single-class point fits: {int(a.single_class_fallback.sum())}.")
    text += ["", "Historical annotations supply both retrospective training and held-out assessment. No new labels, external participant outcomes, annotation time/cost estimate, LLM judge, or deployment effectiveness is claimed. Training label requirements distinguish these models from the label-free baselines.", "", "## Reproduce", "", "Run `python -m facct.conditional.run` from the repository root with pinned facct requirements. This writes separate outputs and verifies source/earlier-output hashes. The manifest records measured runtime and software versions. Source code, seed, predictions, fold assignments, coefficients, and bootstrap replicate deltas are retained."]
    (out/"findings.md").write_text("\n".join(text)+"\n")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--replicates",type=int)
    parser.add_argument("--output",type=Path,default=OUT)
    args=parser.parse_args()
    config=json.loads((ROOT/"facct/conditional/config.json").read_text())
    if args.replicates is not None:
        config["replicates"]=args.replicates
    if config["replicates"]<2000 and args.output.resolve()==OUT.resolve():
        raise ValueError("Use a separate pilot output directory")
    args.output.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    before=frozen_hashes()
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    d["cluster"]=d.domain+":"+d.prompt_id
    assert not d.id.duplicated().any()
    criteria=json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    containers=[[] for _ in range(8)]
    with threadpool_limits(limits=1):
        for domain in DOMAINS:
            result=domain_study(d[d.domain==domain].reset_index(drop=True),criteria,config)
            for container,part in zip(containers,result):
                container.extend(part.to_dict("records") if isinstance(part,pd.DataFrame) else part)
    names=("performance","conditional_lift","oof_predictions","fit_audit","fold_performance","fold_assignments","bootstrap_differences","split_sensitivity")
    for name,rows in zip(names,containers):
        if name=="fit_audit":
            rows=[serialize_audit(r) for r in rows]
        pd.DataFrame(rows).to_csv(args.output/(name+".csv"),index=False)
    report(args.output)
    assert before==frozen_hashes(),"Immutable input or earlier output changed"
    manifest={"status":"final" if config["replicates"]>=2000 else "pilot", "config":config,
        "runtime_seconds":round(time.monotonic()-start,2), "frozen_hashes":before,
        "git_revision":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "software":{p:importlib.metadata.version(p) for p in ("numpy","pandas","scipy","scikit-learn","threadpoolctl")},
        "code_and_plan":{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/"facct/conditional").glob("*") if p.is_file()},
        "outputs":{p.name:sha(p) for p in args.output.glob("*") if p.is_file() and p.name!="manifest.json"}}
    (args.output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps({"status":manifest["status"],"runtime_seconds":manifest["runtime_seconds"],"immutable_files_unchanged":True}),flush=True)


if __name__=="__main__":
    main()
