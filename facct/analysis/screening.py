"""Fixed, label-free policies and exact-budget metrics."""
import hashlib
import math
import re

import numpy as np
from scipy.stats import hypergeom

MARKERS = frozenset("i me my mine myself we us our ours ourselves you your yours yourself yourselves hello hi hey thanks thank welcome sorry please".split())
POLICIES = ("high_H", "length", "markers")
METRICS = ("n", "concerns", "concern_clusters", "selected", "caught", "recall", "precision", "missed", "unselected_prevalence", "delta_random", "delta_length", "delta_markers", "ap", "auc", "workload_50", "workload_80", "workload_90", "workload_100")


def capacity(n, budget):
    if n < 0 or not 0 <= budget <= 1:
        raise ValueError("Invalid batch or budget")
    return math.floor(n * budget + 1e-12)


def tie_keys(ids, seed):
    return np.array([int.from_bytes(hashlib.sha256(f"{seed}|{v}".encode()).digest()[:8], "big") for v in ids], dtype=np.uint64)


def order_scores(scores, ties):
    scores = np.asarray(scores, dtype=float)
    if not np.isfinite(scores).all():
        raise ValueError("Missing or nonfinite scores must be resolved, not silently dropped")
    return np.lexsort((ties, -scores))


def features(frame):
    # Inputs are deliberately restricted; outcome columns cannot enter a policy.
    tokens = [re.findall(r"\b\w+\b", str(text).lower()) for text in frame["response"]]
    length = np.array([len(t) for t in tokens], dtype=float)
    markers = np.array([sum(w in MARKERS for w in t) / len(t) if t else 0 for t in tokens])
    return np.column_stack([frame["H"].to_numpy(float), length, markers])


def label(values, operator, threshold):
    return {">=": np.greater_equal, "<": np.less, "<=": np.less_equal}[operator](values, threshold)


def labels(frame, config):
    return np.column_stack([label(frame[c["column"]].to_numpy(), c["operator"], c["threshold"]) for c in config["criteria"].values()])


def rank_metrics(y, scores, order):
    """Tie-block AP/AUC, independently tested against scikit-learn."""
    y = np.asarray(y, dtype=bool)[order]
    scores = np.asarray(scores)[order]
    n, p = len(y), int(y.sum())
    if not p:
        return np.nan, np.nan, [np.nan] * 4
    ends = np.r_[np.flatnonzero(scores[:-1] != scores[1:]), n - 1]
    tp = np.cumsum(y)[ends]
    block_p = np.diff(np.r_[0, tp])
    total = ends + 1
    neg = total - tp
    block_n = np.diff(np.r_[0, neg])
    ap = float(np.sum(block_p * tp / total) / p)
    auc = float(np.sum(block_p * ((n - p) - neg + .5 * block_n)) / (p * (n - p))) if p < n else np.nan
    cumulative = np.cumsum(y)
    workload = [(np.searchsorted(cumulative, math.ceil(t * p)) + 1) / n for t in (.5, .8, .9, 1.)]
    return ap, auc, workload


def allocation(domains, k):
    names, counts = np.unique(domains, return_counts=True)
    raw = counts * k / counts.sum()
    sizes = np.floor(raw).astype(int)
    for i in np.lexsort((names, -(raw - sizes)))[:k - sizes.sum()]:
        sizes[i] += 1
    return dict(zip(names, sizes))


def evaluate(X, Y, domains, clusters, ties, config, pooled=False):
    """Returns deterministic point metrics; random rows are exact expectations."""
    n = len(Y)
    orders = [order_scores(X[:, i], ties) for i in range(3)]
    rows = []
    for j, criterion in enumerate(config["criteria"]):
        y = Y[:, j]
        p = int(y.sum())
        pc = len(np.unique(clusters[y]))
        ranks = [rank_metrics(y, X[:, i], orders[i]) for i in range(3)]
        for budget in config["budgets"]:
            k = capacity(n, budget)
            catches = [float(y[o[:k]].sum()) for o in orders]
            random_caught = k * p / n
            policies = list(POLICIES) + ["uniform_random"]
            caught = catches + [random_caught]
            if pooled:
                alloc = allocation(domains, k)
                caught.append(sum(size * y[domains == d].mean() for d, size in alloc.items()))
                policies.append("stratified_random")
            for i, policy in enumerate(policies):
                c = caught[i]
                ap, auc, workload = ranks[i] if i < 3 else (np.nan, np.nan, [np.nan] * 4)
                if policy == "uniform_random" and p:
                    workload = [math.ceil(t * p) * (n + 1) / (p + 1) / n for t in (.5, .8, .9, 1.)]
                vals = [n, p, pc, k, c, c/p if p else np.nan, c/k if k else np.nan,
                        p-c, (p-c)/(n-k) if n > k else np.nan,
                        (c-random_caught)/p if p else np.nan,
                        (c-catches[1])/p if p else np.nan,
                        (c-catches[2])/p if p else np.nan, ap, auc, *workload]
                rows.append((criterion, policy, budget, vals))
    return rows


def random_draw_limits(n, p, k):
    return hypergeom.ppf([.025, .975], n, p, k).tolist()
