"""Synthetic unit fixtures only; none are participant or study results."""
import json

import numpy as np
import pandas as pd
import pytest

from facct.capability.evaluate import (cluster_draw, evaluate, metrics, pair_changes, point_rows,
                                       primary_delta, selection_ties, validate)
from facct.capability.prepare import digest, prepare


@pytest.fixture
def inputs(tmp_path):
    (tmp_path / "evidence.md").write_text("SYNTHETIC UNIT TEST EVIDENCE ONLY")
    rows, scores = [], []
    for i in range(10):
        for condition in ("supported", "unsupported"):
            ident = f"{i}-{condition}"
            rows.append(dict(instance_id=ident, base_id=f"b{i}", cluster_id=f"c{i//2}",
                             condition=condition, target_family="memory", prompt=f"p{i}",
                             response=f"r{i}", review_label=str(int(i<3 and condition=="unsupported")),
                             evidence_ref="evidence.md", evidence_sha256=digest(tmp_path / "evidence.md")))
            for policy, score in (("semantic_text", float(i)),
                                  ("semantic_full_evidence", float(i<3 and condition=="unsupported"))):
                scores.append(dict(instance_id=ident, policy=policy, score=score))
    return pd.DataFrame(rows), pd.DataFrame(scores), tmp_path


def test_exact_budget_ties_random_and_primary(inputs):
    cases, scores, root = inputs
    frame = validate(cases, scores, root)
    rows = point_rows(frame, sorted(set(scores.policy)), 21)
    for row in rows:
        assert row["selected"] == int(len(frame)*row["budget"])
    ref = next(r for r in rows if r["budget"] == .2 and r["policy"] == "uniform_random")
    assert ref["caught_definite"] == pytest.approx(.6)
    assert ref["recall_definite"] == .2
    assert primary_delta(frame, 21) == 1
    assert rows == point_rows(frame, sorted(set(scores.policy)), 21)


def test_hand_calculated_unknown_bounds():
    m = metrics(["1", "0", "U", "U", "1"], [True, True, True, False, False])
    assert m["selected"] == 3
    assert m["caught_definite"] == 1
    assert m["selected_definite_negative"] == 1
    assert m["selected_unknown"] == 1
    assert m["recall_lower"] == pytest.approx(1/3)
    assert m["recall_upper"] == pytest.approx(2/3)
    assert m["recall_definite"] == .5


def test_missing_score_rejected(inputs):
    cases, scores, root = inputs
    with pytest.raises(ValueError, match="full batch"):
        validate(cases, scores.iloc[1:], root)
    scores.loc[0, "score"] = np.nan
    with pytest.raises(ValueError, match="Missing"):
        validate(cases, scores, root)


def test_capability_hash_and_fixed_text_checked(inputs):
    cases, scores, root = inputs
    cases.loc[0, "response"] = "changed"
    with pytest.raises(ValueError, match="response"):
        validate(cases, scores, root)
    cases.loc[0, "response"] = "r0"
    cases.loc[0, "evidence_sha256"] = "0"*64
    with pytest.raises(ValueError, match="evidence artifact"):
        validate(cases, scores, root)


def test_text_only_cannot_see_configuration(inputs):
    cases, scores, root = inputs
    scores.loc[0, "score"] = 999
    with pytest.raises(ValueError, match="text-only"):
        validate(cases, scores, root)


def test_cluster_copies_preserve_every_twin(inputs):
    frame = validate(*inputs)
    drawn = cluster_draw(frame, np.random.default_rng(17))
    assert len(drawn) == len(frame)
    for cluster, group in drawn.groupby("cluster_id"):
        assert len(group) % 4 == 0
        assert set(group.condition) == {"supported", "unsupported"}
    assert drawn.index.is_unique


def test_bootstrap_reproducible_and_unknown_not_dropped(inputs):
    cases, scores, root = inputs
    cases.loc[0, "review_label"] = "U"
    frame = validate(cases, scores, root)
    t1, c1 = evaluate(frame, sorted(set(scores.policy)), 20, 4)
    t2, c2 = evaluate(frame, sorted(set(scores.policy)), 20, 4)
    pd.testing.assert_frame_equal(t1, t2)
    pd.testing.assert_frame_equal(c1, c2)
    assert t1[t1.scope == "mixed"].n.eq(20).all()
    assert c1[c1.scope == "mixed"].status.eq("partial_labels_descriptive").all()
    assert (c1.effective_replicates + c1.undefined_replicates).eq(20).all()


def test_zero_events_and_tiny_batch_are_undefined(inputs):
    cases, scores, root = inputs
    cases.review_label = "0"
    frame = validate(cases, scores, root)
    table, contrasts = evaluate(frame, sorted(set(scores.policy)), 3, 1)
    assert table.recall_definite.isna().all()
    assert table.ap_definite_subset.isna().all()
    assert contrasts.effective_replicates.eq(0).all()
    assert contrasts.lo.isna().all()
    tiny = metrics(["1"], [False])
    assert np.isnan(tiny["precision_lower"])
    assert tiny["recall_definite"] == 0


def test_tied_average_precision_all_positive(inputs):
    cases, scores, root = inputs
    cases.review_label = "1"
    scores.score = 1.0
    table = pd.DataFrame(point_rows(validate(cases, scores, root), ["semantic_text"], 1))
    ranked = table[table.policy == "semantic_text"]
    assert ranked.ap_definite_subset.eq(1).all()
    assert ranked.auc_definite_subset.isna().all()
    assert ranked.caught_definite.eq(ranked.selected).all()


def test_condition_ties_coupled_and_transitions(inputs):
    frame = validate(*inputs)
    a = frame[frame.condition == "supported"].sort_values("base_id")
    b = frame[frame.condition == "unsupported"].sort_values("base_id")
    assert np.array_equal(selection_ties(a, 10), selection_ties(b, 10))
    changes = pair_changes(frame)
    assert len(changes) == 10
    assert (changes.transition == "changed").sum() == 3
    assert (changes.transition == "stable").sum() == 7


def test_preparation_is_blinded_reproducible_immutable(tmp_path):
    source = tmp_path / "source.csv"
    pd.DataFrame([dict(domain="mental_health", annotation_item_id=f"a{i}", prompt_id=f"p{i//2}",
                       prompt="p", response="r", D=5, H=.9, model="secret") for i in range(12)]).to_csv(source, index=False)
    before = digest(source)
    prepare(source, tmp_path / "one", 4, 10)
    prepare(source, tmp_path / "two", 4, 10)
    assert digest(source) == before
    assert digest(tmp_path / "one/candidates.csv") == digest(tmp_path / "two/candidates.csv")
    candidate = pd.read_csv(tmp_path / "one/candidates.csv")
    assert set(candidate) == {"base_id", "prompt", "response", "candidate_status"}
    assert len(pd.read_csv(tmp_path / "one/source_map.csv").prompt_id.unique()) == 4
    assert "PREPARATION_ONLY" in json.loads((tmp_path / "one/manifest.json").read_text())["status"]
    with pytest.raises(ValueError, match="immutable"):
        prepare(source, tmp_path / "one", 4, 10)
