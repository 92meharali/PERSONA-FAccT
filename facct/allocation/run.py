"""Audit category coverage after selection from a common domain-wide queue."""
from pathlib import Path
import argparse
import importlib.metadata
import json
import subprocess
import time

import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits

from facct.analysis.screening import capacity, features, labels, order_scores, tie_keys
from facct.analysis.uncertainty import draw_indices, summarize
from facct.analysis.validate_inputs import sha
from facct.conditional.run import frozen_hashes
from facct.revision.run import fusion_scores

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "facct/allocation/outputs"
DOMAINS = ("mental_health", "education", "health")
POLICIES = ("high_H", "length", "markers", "rank_fusion", "uniform_random")
GROUPINGS = ("condition", "model", "scenario_type")
METRICS = ("selected", "caught", "recall", "precision", "missed", "unselected_prevalence",
           "selection_rate", "group_minus_complement_recall", "delta_random")


def protected_hashes():
    result = frozen_hashes()
    result.update({str(p.relative_to(ROOT)): sha(p) for p in (ROOT/"facct/conditional").rglob("*")
                   if p.is_file() and "__pycache__" not in str(p)})
    return result


def divide(a, b):
    a, b = np.broadcast_arrays(np.asarray(a, float), np.asarray(b, float))
    return np.divide(a, b, out=np.full(a.shape, np.nan), where=b != 0)


def membership(frame):
    groups, columns = [], []
    for grouping in GROUPINGS:
        values = frame[grouping].fillna("<missing>").astype(str).to_numpy()
        for value in sorted(set(values)):
            groups.append((grouping, value))
            columns.append(values == value)
    return groups, np.column_stack(columns).astype(float)


def evaluate(X, Y, groups, keys, budget=.2):
    n = len(X)
    if not n:
        raise ValueError("A nonempty domain batch is required")
    k = capacity(n, budget)
    scores = np.column_stack((X, fusion_scores(X)))
    selection = np.zeros((n, len(POLICIES)))
    for policy in range(4):
        selection[order_scores(scores[:, policy], keys)[:k], policy] = 1
    selection[:, 4] = k/n
    ng = groups.sum(axis=0)
    pg = groups.T @ Y.astype(float)
    selected = groups.T @ selection
    caught = (groups.T @ (Y[:, :, None]*selection[:, None, :]).reshape(n, -1)).reshape(len(ng), Y.shape[1], len(POLICIES))
    total_caught = Y.astype(float).T @ selection
    recall = divide(caught, pg[:, :, None])
    rest = divide(total_caught[None, :, :]-caught, Y.sum(axis=0)[None, :, None]-pg[:, :, None])
    missed = pg[:, :, None]-caught
    arrays = (np.broadcast_to(selected[:, None, :], caught.shape), caught, recall,
              divide(caught, selected[:, None, :]), missed,
              divide(missed, ng[:, None, None]-selected[:, None, :]),
              np.broadcast_to(divide(selected, ng[:, None])[:, None, :], caught.shape),
              recall-rest, recall-k/n)
    return np.stack(arrays, axis=-1), selection


def study(frame, criteria, config):
    X, Y = features(frame), labels(frame, criteria)
    groups, G = membership(frame)
    ids, clusters = frame.id.to_numpy(), frame.cluster.to_numpy()
    point, selections = evaluate(X, Y, G, tie_keys(ids, config["seed"]))
    samples = np.empty((config["replicates"], *point.shape))
    rng = np.random.default_rng(config["seed"])
    domains = frame.domain.to_numpy()
    for b in range(config["replicates"]):
        idx, copies = draw_indices(domains, clusters, rng)
        keys = tie_keys([f"{v}|{c}" for v, c in zip(ids[idx], copies)], config["seed"])
        samples[b], _ = evaluate(X[idx], Y[idx], G[idx], keys)
    rows, differences = [], []
    domain = frame.domain.iloc[0]
    for g, (grouping, value) in enumerate(groups):
        mask = G[:, g].astype(bool)
        for j, criterion in enumerate(criteria["criteria"]):
            pc = len(set(clusters[mask & Y[:, j]]))
            nc = len(set(clusters[mask & ~Y[:, j]]))
            rest_pc = len(set(clusters[~mask & Y[:, j]]))
            rest_nc = len(set(clusters[~mask & ~Y[:, j]]))
            context = dict(domain=domain, grouping=grouping, group=value, criterion=criterion,
                n=int(mask.sum()), concerns=int(Y[mask, j].sum()), concern_clusters=pc,
                nonconcern_clusters=nc, complement_concern_clusters=rest_pc,
                complement_nonconcern_clusters=rest_nc, sparse=min(pc, nc)<10,
                contrast_sparse=min(pc, nc, rest_pc, rest_nc)<10,
                domain_n=len(frame), domain_selected=capacity(len(frame), .2), budget=.2)
            for p, policy in enumerate(POLICIES):
                row = dict(context, policy=policy)
                for m, metric in enumerate(METRICS):
                    lo, hi, valid = summarize(samples[:, g, j, p, m])
                    row.update({metric:point[g,j,p,m], metric+"_lo":lo, metric+"_hi":hi, metric+"_valid":valid})
                rows.append(row)
            delta = samples[:, g, j, 0, 2]-samples[:, g, j, 2, 2]
            lo, hi, valid = summarize(delta)
            differences.append(dict(context, H_minus_markers=point[g,j,0,2]-point[g,j,2,2],
                                    lo=lo, hi=hi, valid_replicates=valid))
    selected = frame[["id", "cluster", "domain", *GROUPINGS]].copy()
    for p, policy in enumerate(POLICIES):
        selected[policy] = selections[:, p]
    return rows, differences, selected


def report(out):
    d = pd.read_csv(out/"category_coverage.csv")
    text = ["# Common-queue allocation audit", "", "Exploratory third amendment. Each domain is ranked once at 20% capacity; the selected queue is then described by category. Subgroups do not receive independent quotas. Earlier studies and primary comparisons remain unchanged.", "",
            "## Complete condition view", "", "| Domain | Criterion | Condition | N | Cases / positive prompts | H slots | H caught | H missed | Marker slots | Marker caught | Sparse |",
            "|---|---|---|---:|---|---:|---:|---:|---:|---:|---|"]
    for row in d[(d.grouping=="condition") & (d.policy=="high_H")].itertuples():
        marker = d[(d.domain==row.domain)&(d.grouping==row.grouping)&(d.group==row.group)&(d.criterion==row.criterion)&(d.policy=="markers")].iloc[0]
        text.append(f"| {row.domain} | {row.criterion} | {row.group} | {row.n} | {row.concerns} / {row.concern_clusters} | {row.selected:g} | {row.caught:g} | {row.missed:g} | {marker.selected:g} | {marker.caught:g} | {row.sparse} |")
    text += ["", "## Interpretation contract", "",
             "- All condition, model, and scenario cells, including zero-concern and sparse cells, are retained in category_coverage.csv. Intervals are paired prompt-bootstrap pointwise summaries, not simultaneous subgroup tests.",
             "- Selection rate describes access to review. Recall describes coverage conditional on the recorded criterion. A larger missed count may reflect more concerns rather than a poorer ranking; read rates and counts together.",
             "- H-minus-marker contrasts are paired within the same group and full-domain quota. Group-minus-complement contrasts compare coverage under one common policy, not a counterfactual intervention. Shared prompt clusters remain together across model categories.",
             "- Random expected group slots and caught counts use the full-domain budget fraction. Expected-count precision is a ratio of expectations; random single-draw variability is not what its bootstrap interval estimates.",
             "- Category labels are existing corpus metadata, not validated demographic groups. Natural/adversarial prompts are unmatched. Patterns describe this corpus and criterion, not causal discrimination or deployment harm.",
             "- Changing the concern threshold does not change these label-free selections. It changes which selected and unselected items count as concerns. No subgroup has been given a quota or policy recommendation on the basis of these exploratory results.",
             "", "Run `python -m facct.allocation.run` from the repository root. The manifest records runtime, software, seeds, source hashes and all output hashes. Selection identities are retained without raw text."]
    (out/"findings.md").write_text("\n".join(text)+"\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    if args.replicates<2000 and args.output.resolve()==OUT.resolve():
        raise ValueError("Pilot output must use a separate directory")
    start=time.monotonic()
    before=protected_hashes()
    config=dict(version="3.0.0", seed=20261002, replicates=args.replicates, budget=.2,
                groupings=GROUPINGS, policies=POLICIES, sparse_class_clusters=10)
    criteria=json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    d["cluster"]=d.domain+":"+d.prompt_id
    rows, contrasts, selected=[], [], []
    with threadpool_limits(limits=1):
        for domain in DOMAINS:
            r,c,s=study(d[d.domain==domain].reset_index(drop=True),criteria,config)
            rows.extend(r); contrasts.extend(c); selected.append(s)
            print(f"{domain}: {args.replicates} paired common-queue draws completed",flush=True)
    args.output.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(args.output/"category_coverage.csv",index=False)
    pd.DataFrame(contrasts).to_csv(args.output/"paired_policy_differences.csv",index=False)
    pd.concat(selected,ignore_index=True).to_csv(args.output/"selection_register.csv",index=False)
    report(args.output)
    assert before==protected_hashes(),"Protected source or earlier result changed"
    manifest=dict(status="final" if args.replicates>=2000 else "pilot",config=config,
        runtime_seconds=round(time.monotonic()-start,2),frozen_hashes=before,
        git_revision=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        software={p:importlib.metadata.version(p) for p in ("numpy","pandas","scipy","scikit-learn","threadpoolctl")},
        code_and_plan={str(p.relative_to(ROOT)):sha(p) for p in Path(__file__).parent.glob("*") if p.is_file()},
        outputs={p.name:sha(p) for p in args.output.glob("*") if p.is_file() and p.name!="manifest.json"})
    (args.output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(dict(status=manifest["status"],runtime_seconds=manifest["runtime_seconds"],protected_unchanged=True)))


if __name__=="__main__":
    main()
