import json

import numpy as np
import pandas as pd
import pytest

from facct.analysis.screening import tie_keys
from facct.conditional.analysis import crossfit, group_folds, resample_within_folds
from .analysis import measure, queue_pairs, random_counts, selections
from .run import HERE, ROOT, TRAIN


def test_hand_checked_off_diagonal_cells_and_pairs():
    scores = np.array([[4, 1], [3, 2], [2, 3], [1, 4]], float)[:, :, None]
    outcomes = np.array([[1, 0], [1, 0], [0, 1], [0, 1]], bool)
    masks = selections(scores, np.zeros(4), np.arange(4), .5)
    values = measure(masks, outcomes)
    np.testing.assert_array_equal(values[:, 0, :, 0], [[2, 0], [0, 2]])
    np.testing.assert_array_equal(values[:, 0, :, 1], [[1, 0], [0, 1]])
    pair = queue_pairs(masks, outcomes)[0]
    assert pair["intersection"] == 0 and pair["symmetric_difference"] == 4
    assert pair["jaccard"] == 0
    np.testing.assert_array_equal(pair["left_only_caught"], [2, 0])


def test_exact_fold_budget_not_pooled_budget_and_ties():
    scores = np.ones((6, 3, 2))
    folds = np.repeat([0, 1], 3)
    keys = tie_keys([f"a{i}" for i in range(6)], 42)
    first = selections(scores, folds, keys, .5)
    assert np.all(first.sum(axis=0) == 2)
    np.testing.assert_array_equal(first, selections(scores, folds, keys, .5))
    assert np.all(first == first[:, :1, :1])


def test_undefined_empty_and_all_positive_endpoints():
    scores = np.arange(4)[:, None, None]
    y = np.column_stack([np.zeros(4), np.ones(4)])
    mask = selections(scores, np.zeros(4), np.arange(4), .5)
    v = measure(mask, y)
    assert np.isnan(v[0, 0, 0, 1])
    assert v[0, 0, 1, 1] == .5 and v[0, 0, 1, 2] == 1
    zero = measure(selections(scores, np.zeros(4), np.arange(4), 0), y)
    assert np.isnan(zero[..., 2]).all()
    full = measure(selections(scores, np.zeros(4), np.arange(4), 1), y)
    assert np.isnan(full[..., 4]).all()
    with pytest.raises(ValueError):
        selections(scores*np.nan, np.zeros(4), np.arange(4), .5)
    with pytest.raises(ValueError):
        measure(mask, np.full((4, 1), -1))


def test_matched_random_uses_fold_prevalence():
    y = np.array([[1], [1], [0], [0], [0]], bool)
    f = np.array([0, 0, 1, 1, 1])
    np.testing.assert_allclose(random_counts(y, f, .5), [1.0])


def test_assessment_outcome_cannot_affect_queue():
    scores = np.arange(8)[:, None, None]
    mask = selections(scores, np.zeros(8), np.arange(8), .5)
    before = mask.copy()
    a = measure(mask, np.zeros((8, 1)))
    b = measure(mask, np.ones((8, 1)))
    np.testing.assert_array_equal(before, mask)
    assert a[0, 0, 0, 0] == 0 and b[0, 0, 0, 0] == 4


def test_bootstrap_preserves_prompt_partition_and_outcome_pairing():
    clusters = np.repeat(np.arange(10), 3)
    folds = group_folds(clusters, 42)
    idx, copies = resample_within_folds(folds, clusters, np.random.default_rng(3))
    assert len(idx) == 30
    for copy in np.unique(copies):
        sample = idx[copies == copy]
        assert len(sample) == 3 and len(set(clusters[sample])) == 1
        assert len(set(folds[sample])) == 1
    for c in np.unique(clusters[idx]):
        assert len(set(folds[idx][clusters[idx] == c])) == 1


def test_crossfit_rejects_prompt_leakage():
    config = json.loads((ROOT/"facct/conditional/config.json").read_text())
    X = np.array([[.1, 10, .2], [.2, 20, .1], [.3, 30, .3], [.4, 40, .2]])
    with pytest.raises(ValueError, match="prompt"):
        crossfit(X, np.array([[0], [1], [0], [1]]), np.array([0, 1, 0, 1]), np.array([1, 1, 2, 2]), config)


@pytest.mark.skipif(not (HERE/"outputs/manifest.json").exists(), reason="Final run not yet generated")
def test_complete_matrix_and_previous_diagonals():
    p = pd.read_csv(HERE/"outputs/performance.csv")
    assert len(p) == 240
    assert not p.duplicated(["domain", "budget", "model", "train_target", "evaluation_target"]).any()
    old = pd.read_csv(ROOT/"facct/conditional/outputs/performance.csv")
    for r in p.itertuples():
        if r.train_target != r.evaluation_target:
            continue
        prior = old[(old.domain == r.domain)&(old.criterion == r.train_target)&(old.budget == r.budget)
                    &(old.policy == ("reduced_lr" if r.model == "lexical_lr" else "extended_lr"))].iloc[0]
        assert r.caught == prior.caught and r.selected == prior.selected
        if r.budget == .2:
            np.testing.assert_allclose([r.recall_lo, r.recall_hi], [prior.recall_lo, prior.recall_hi], atol=1e-12)
    assert set(p.train_target) == set(TRAIN)
    follow = p[p.evaluation_target == "contextual_reviewworthiness"]
    assert set(follow.domain) == {"mental_health"} and set(follow.concerns) == {19}
