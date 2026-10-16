"""Leakage-resistant conditional recall lift in common held-out batches."""
import json
import warnings

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from facct.analysis.screening import capacity, order_scores, tie_keys
from facct.revision.run import fusion_scores


POLICIES = ("high_H", "length", "markers", "rank_fusion", "reduced_lr", "extended_lr", "uniform_random")
METRICS = ("caught", "recall", "precision", "missed", "unselected_prevalence")


def group_folds(clusters, seed, n_folds=5):
    clusters = np.asarray(clusters)
    unique = np.unique(clusters)
    if len(unique) < n_folds:
        raise ValueError("Fewer prompt groups than folds")
    rng = np.random.default_rng(seed)
    chunks = np.array_split(rng.permutation(unique), n_folds)
    mapping = {group: fold for fold, chunk in enumerate(chunks) for group in chunk}
    return np.array([mapping[group] for group in clusters], dtype=int)


def model_inputs(X, extended):
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or X.shape[1] != 3 or not np.isfinite(X).all() or (X[:, 1] < 0).any():
        raise ValueError("Expected finite H, nonnegative length, marker features")
    base = np.column_stack((X[:, 2], np.log1p(X[:, 1])))
    return np.column_stack((base, X[:, 0])) if extended else base


def fit_predict(train_X, train_y, test_X, extended, config):
    train_y = np.asarray(train_y, dtype=int)
    if not len(train_y) or not np.isin(train_y, [0, 1]).all():
        raise ValueError("Nonempty binary training labels required")
    scaler = StandardScaler()
    train = scaler.fit_transform(model_inputs(train_X, extended))
    test = scaler.transform(model_inputs(test_X, extended))
    audit = {"scaler_mean": scaler.mean_.tolist(), "scaler_scale": scaler.scale_.tolist(),
             "training_prevalence": float(train_y.mean()), "single_class_fallback": len(np.unique(train_y)) == 1}
    if audit["single_class_fallback"]:
        audit.update(coefficients=None, intercept=None, iterations=0)
        return np.full(len(test), train_y.mean()), audit
    model = LogisticRegression(**config["logistic"], class_weight=None, fit_intercept=True)
    with warnings.catch_warnings():
        warnings.simplefilter("error", ConvergenceWarning)
        model.fit(train, train_y)
    audit.update(coefficients=model.coef_[0].tolist(), intercept=float(model.intercept_[0]), iterations=int(model.n_iter_[0]))
    prediction = model.predict_proba(test)[:, 1]
    if not np.isfinite(prediction).all():
        raise ValueError("Nonfinite predictions")
    return prediction, audit


def crossfit(X, Y, folds, clusters, config, keep_audit=False):
    """Every prediction is produced without labels from its original prompt group."""
    n, criteria = Y.shape
    scores = np.full((n, criteria, 6), np.nan)
    audits = []
    fallback_count = 0
    for fold in np.unique(folds):
        test = np.flatnonzero(folds == fold)
        train = np.flatnonzero(folds != fold)
        if set(clusters[train]) & set(clusters[test]):
            raise ValueError("A prompt occurs in both training and held-out batch")
        scores[test, :, :3] = np.broadcast_to(X[test, None, :], (len(test), criteria, 3))
        scores[test, :, 3] = fusion_scores(X[test])[:, None]
        for criterion in range(criteria):
            for extended, column in ((False, 4), (True, 5)):
                pred, info = fit_predict(X[train], Y[train, criterion], X[test], extended, config)
                scores[test, criterion, column] = pred
                fallback_count += int(info["single_class_fallback"])
                if keep_audit:
                    audits.append(dict(fold=int(fold), criterion_index=criterion, policy=POLICIES[column],
                        training_responses=len(train), test_responses=len(test),
                        training_prompts=len(np.unique(clusters[train])), test_prompts=len(np.unique(clusters[test])),
                        training_positive=int(Y[train, criterion].sum()),
                        training_negative=int(len(train)-Y[train, criterion].sum()),
                        underlying_training_ratings=5*len(train), **info))
    if not np.isfinite(scores).all():
        raise ValueError("Missing out-of-fold predictions")
    return scores, audits, fallback_count


def evaluate(scores, Y, folds, keys, budgets):
    """Micro-average counts, never pooled cross-model rankings or mean fold recall."""
    n, criteria, _ = scores.shape
    values = np.empty((len(budgets), criteria, len(POLICIES), len(METRICS)))
    fold_records = []
    for bidx, budget in enumerate(budgets):
        caught = np.zeros((criteria, len(POLICIES)))
        selected = 0
        for fold in np.unique(folds):
            idx = np.flatnonzero(folds == fold)
            k = capacity(len(idx), budget)
            selected += k
            for j in range(criteria):
                p = int(Y[idx, j].sum())
                for policy in range(len(POLICIES)):
                    if policy == 6:
                        c = k*p/len(idx)
                    else:
                        order = order_scores(scores[idx, j, policy], keys[idx])
                        c = float(Y[idx[order[:k]], j].sum())
                    caught[j, policy] += c
                    fold_records.append(dict(budget=budget, fold=int(fold), criterion_index=j,
                        policy=POLICIES[policy], n=len(idx), selected=k, concerns=p, caught=c))
        for j in range(criteria):
            p = int(Y[:, j].sum())
            for i, c in enumerate(caught[j]):
                values[bidx, j, i] = [c, c/p if p else np.nan, c/selected if selected else np.nan,
                    p-c, (p-c)/(n-selected) if selected<n else np.nan]
    return values, fold_records


def resample_within_folds(folds, clusters, rng):
    indices, copies = [], []
    copy = 0
    for fold in np.unique(folds):
        groups = [np.flatnonzero((folds == fold) & (clusters == c)) for c in np.unique(clusters[folds == fold])]
        for group in rng.integers(0, len(groups), len(groups)):
            idx = groups[group]
            indices.extend(idx)
            copies.extend([copy]*len(idx))
            copy += 1
    return np.asarray(indices), np.asarray(copies)


def bootstrap(X, Y, folds, clusters, ids, config, progress=None):
    rng = np.random.default_rng(config["seed"])
    draws = []
    fallbacks = []
    for b in range(config["replicates"]):
        idx, copies = resample_within_folds(folds, clusters, rng)
        scores, _, fallback = crossfit(X[idx], Y[idx], folds[idx], clusters[idx], config)
        keys = tie_keys([f"{v}|{c}" for v, c in zip(ids[idx], copies)], config["seed"])
        values, _ = evaluate(scores, Y[idx], folds[idx], keys, [config["reference_budget"]])
        draws.append(values[0])
        fallbacks.append(fallback)
        if progress and (b+1) % 250 == 0:
            progress(b+1)
    return np.asarray(draws), np.asarray(fallbacks)


def serialize_audit(row):
    return {key: json.dumps(value) if isinstance(value, (list, dict)) else value for key, value in row.items()}
