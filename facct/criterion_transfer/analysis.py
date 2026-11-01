"""Evaluate target-dependent queues without using assessment labels as inputs."""
import numpy as np

from facct.analysis.screening import capacity, order_scores


METRICS = ("caught", "recall", "precision", "missed", "unselected_prevalence")


def selections(scores, folds, keys, budget):
    """Return n x training-target x feature-set masks, ranked within each fold."""
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 3 or not np.isfinite(scores).all():
        raise ValueError("Finite three-dimensional scores required")
    if len(folds) != len(scores) or len(keys) != len(scores):
        raise ValueError("Misaligned score metadata")
    masks = np.zeros(scores.shape, dtype=bool)
    for fold in np.unique(folds):
        idx = np.flatnonzero(folds == fold)
        k = capacity(len(idx), budget)
        for train in range(scores.shape[1]):
            for model in range(scores.shape[2]):
                order = order_scores(scores[idx, train, model], keys[idx])
                masks[idx[order[:k]], train, model] = True
    return masks


def measure(masks, outcomes):
    """All training-target by feature-set by assessment-target cells."""
    masks, outcomes = np.asarray(masks, bool), np.asarray(outcomes)
    if outcomes.ndim != 2 or len(masks) != len(outcomes) or not np.isin(outcomes, [0, 1]).all():
        raise ValueError("Aligned binary assessment outcomes required")
    n = len(outcomes)
    p = outcomes.sum(axis=0)
    k = masks.sum(axis=0)
    caught = np.einsum("ntm,ne->tme", masks.astype(float), outcomes.astype(float))
    result = np.full(caught.shape + (len(METRICS),), np.nan)
    result[..., 0] = caught
    np.divide(caught, p, out=result[..., 1], where=p > 0)
    np.divide(caught, k[..., None], out=result[..., 2], where=k[..., None] > 0)
    result[..., 3] = p - caught
    np.divide(p - caught, n-k[..., None], out=result[..., 4], where=n-k[..., None] > 0)
    return result


def random_counts(outcomes, folds, budget):
    return sum(capacity(int(sum(folds == f)), budget) * outcomes[folds == f].mean(axis=0)
               for f in np.unique(folds))


def queue_pairs(masks, outcomes):
    rows = []
    for a in range(masks.shape[1]):
        for b in range(a+1, masks.shape[1]):
            for model in range(masks.shape[2]):
                left, right = masks[:, a, model], masks[:, b, model]
                union = int((left | right).sum())
                rows.append(dict(left=a, right=b, model=model,
                    intersection=int((left & right).sum()), union=union,
                    symmetric_difference=int((left ^ right).sum()),
                    jaccard=int((left & right).sum())/union if union else np.nan,
                    left_only_caught=outcomes[left & ~right].sum(axis=0),
                    right_only_caught=outcomes[right & ~left].sum(axis=0)))
    return rows
