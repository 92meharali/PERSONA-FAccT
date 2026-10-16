"""Paired domain-stratified prompt-cluster bootstrap, re-ranking every draw."""
import itertools
import numpy as np
import pandas as pd

from .screening import METRICS, evaluate, features, labels, tie_keys


def draw_indices(domains, clusters, rng):
    indices, copies = [], []
    copy = 0
    for domain in np.unique(domains):
        groups = [np.flatnonzero((domains == domain) & (clusters == c)) for c in np.unique(clusters[domains == domain])]
        for chosen in rng.integers(0, len(groups), len(groups)):
            ids = groups[chosen]
            indices.extend(ids)
            copies.extend([copy] * len(ids))
            copy += 1
    return np.asarray(indices), np.asarray(copies)


def summarize(values, confidence=.95):
    finite = np.asarray(values)[np.isfinite(values)]
    if not len(finite):
        return np.nan, np.nan, 0
    q = (1 - confidence) / 2
    lo, hi = np.quantile(finite, [q, 1-q])
    return float(lo), float(hi), len(finite)


def bootstrap(frame, config, replicates):
    X, Y = features(frame), labels(frame, config)
    domains = frame.domain.to_numpy()
    clusters = frame.cluster.to_numpy()
    ids = frame.id.to_numpy()
    ties = tie_keys(ids, config["seed"])
    pooled = len(np.unique(domains)) > 1
    point = evaluate(X, Y, domains, clusters, ties, config, pooled)
    samples = np.empty((replicates, len(point), len(METRICS)))
    rng = np.random.default_rng(config["seed"])
    # Original cluster identity is retained for counting distinct supporting clusters;
    # occurrence keys distinguish repeated copies only for fair score tie-breaking.
    for b in range(replicates):
        idx, copies = draw_indices(domains, clusters, rng)
        keys = tie_keys([f"{v}|{c}" for v, c in zip(ids[idx], copies)], config["seed"])
        rows = evaluate(X[idx], Y[idx], domains[idx], clusters[idx], keys, config, pooled)
        samples[b] = np.array([row[3] for row in rows])
    records = []
    for i, (criterion, policy, budget, vals) in enumerate(point):
        row = dict(criterion=criterion, policy=policy, budget=budget)
        for j, (metric, value) in enumerate(zip(METRICS, vals)):
            lo, hi, count = summarize(samples[:, i, j])
            row.update({metric: value, metric+"_lo": lo, metric+"_hi": hi, metric+"_valid": count})
        lo, hi, count = summarize(samples[:, i, METRICS.index("delta_random")], 1-.05/3)
        row.update(primary_adjusted_delta_lo=lo, primary_adjusted_delta_hi=hi, primary_adjusted_valid=count)
        records.append(row)
    comparisons = []
    for policy in ("high_H", "length", "markers"):
        for budget in config["budgets"]:
            for a,b in itertools.combinations(config["criteria"],2):
                ia=next(i for i,row in enumerate(point) if row[:3]==(a,policy,budget))
                ib=next(i for i,row in enumerate(point) if row[:3]==(b,policy,budget))
                m=METRICS.index("recall")
                lo,hi,valid=summarize(samples[:,ia,m]-samples[:,ib,m])
                comparisons.append(dict(policy=policy,budget=budget,criterion_a=a,criterion_b=b,
                                        recall_difference=point[ia][3][m]-point[ib][3][m],lo=lo,hi=hi,valid_replicates=valid,
                                        caveat="different prevalences/thresholds; not proof of normative disagreement"))
    result=pd.DataFrame(records)
    result.attrs["criterion_comparisons"]=comparisons
    return result
