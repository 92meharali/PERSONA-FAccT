import numpy as np
import pytest

from analysis.common import flags_at_queue_size, normalize_text, wilson_ci
from analysis.paired_detection import (
    cluster_bootstrap_diff,
    mcnemar_exact,
    positives_needed,
    posterior_a_better,
    summarize_counts,
)


def test_mcnemar_exact_known_values():
    # 7 vs 1 discordant: 2 * P(X <= 1 | n=8, p=.5) = 2 * 9/256
    assert mcnemar_exact(7, 1) == pytest.approx(18 / 256)
    assert mcnemar_exact(12, 6) == pytest.approx(0.2379, abs=1e-3)
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(5, 5) == 1.0


def test_posterior_monotone_in_evidence():
    assert posterior_a_better(0, 0) == pytest.approx(0.5)
    assert posterior_a_better(7, 1) > posterior_a_better(12, 6) > 0.9


def test_wilson_ci_matches_reference():
    iv = wilson_ci(12, 19)
    assert iv.estimate == pytest.approx(12 / 19)
    assert iv.lower == pytest.approx(0.410, abs=2e-3)
    assert iv.upper == pytest.approx(0.809, abs=2e-3)


def test_paper_follow_up_counts_feasible_range():
    rep = summarize_counts(19, 12, 6, None, "markers", "humt")
    ps = [r["mcnemar_exact_p"] for r in rep["by_overlap"]]
    # Overlap 0..6 is arithmetically feasible; the paper bounds it at 5.
    assert ps[0] == pytest.approx(0.238, abs=1e-3)
    assert ps[5] == pytest.approx(0.070, abs=1e-3)
    assert all(p > 0.05 for p in ps[:6])
    post = [r["posterior_P(markers>humt)"] for r in rep["by_overlap"][:6]]
    assert min(post) >= 0.91 and max(post) <= 0.985
    need = rep["replication_positives_for_80pct_power"]
    assert need["min_discordance"] == 23
    assert need["max_discordance"] == 73


def test_positives_needed_rejects_impossible_discordance():
    with pytest.raises(ValueError):
        positives_needed(0.6, 0.3, 0.1)


def test_flags_at_queue_size_exact_capacity_with_ties():
    scores = np.array([1.0, 1.0, 1.0, 0.5, 0.0])
    flags = flags_at_queue_size(scores, 2, np.random.default_rng(1))
    assert flags.sum() == 2
    assert not flags[3] and not flags[4]


def test_cluster_bootstrap_recovers_point_estimate():
    rng = np.random.default_rng(0)
    n = 400
    cluster = np.repeat(np.arange(100), 4)
    positive = rng.random(n) < 0.1
    fa = rng.random(n) < 0.6
    fb = rng.random(n) < 0.3
    iv = cluster_bootstrap_diff(positive, fa, fb, cluster, n_boot=300, seed=1)
    pos = positive
    expected = (fa & pos).sum() / pos.sum() - (fb & pos).sum() / pos.sum()
    assert iv.estimate == pytest.approx(expected)
    assert iv.lower < expected < iv.upper


def test_normalize_text_collapses_formatting_only():
    assert normalize_text("Hello,\u00a0 World\n") == normalize_text("hello, world")
    assert normalize_text("I feel sad") != normalize_text("I felt sad")
