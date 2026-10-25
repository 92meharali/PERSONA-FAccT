import numpy as np
import pandas as pd
import pytest

from facct.professor_revision.run import analyze, catches, recall, score_matrix, targets


def sample():
    return pd.DataFrame(dict(response=["hello " + "x"*294 + " sorry", "you please", "plain", "other", "hello"],
                             H=[5, 4, 3, 2, 1], D=[3, 3.2, 4, 1, 2], F=[5, 3, 4, 5, 5], OA=[5, 4, 3, 5, 5],
                             id=list("abcde"), domain=["test"]*5, cluster=["p1", "p1", "p2", "p2", "p3"]))


def test_prefix_slices_characters_before_tokenization():
    x = score_matrix(sample())
    assert x[0, 1] == 2/3 and x[0, 2] == 1/2
    assert x[0, 3] == 3 and x[0, 4] == 2
    assert np.array_equal(x[:, 0], sample().H)


def test_strict_cutoff_differs_from_stronger_anchor():
    names, y = targets(sample())
    assert y[:, names.index("D_ge3")].sum() == 3
    assert y[:, names.index("D_gt3")].sum() == 2
    assert y[:, names.index("D_ge4")].sum() == 1


def test_exact_capacity_ties_random_and_hand_counts():
    x = np.ones((5, 5))
    y = np.array([[True], [False], [False], [False], [False]])
    c = catches(x, y, np.arange(5))
    assert np.array_equal(c[:2], np.zeros((2, 1, 6)))
    assert np.array_equal(c[2, 0, :5], np.ones(5))
    assert c[2, 0, -1] == .2
    assert np.isnan(recall(c, np.array([0]))).all()
    x[0, 0] = np.nan
    with pytest.raises(ValueError, match="Missing score"):
        catches(x, y, np.arange(5))


def test_paired_resampling_is_reproducible_and_inputs_immutable():
    d = sample()
    before = d.copy(deep=True)
    a, b = analyze(d, 20, 42)
    aa, bb = analyze(d, 20, 42)
    pd.testing.assert_frame_equal(a, aa)
    pd.testing.assert_frame_equal(b, bb)
    pd.testing.assert_frame_equal(d, before)
    assert a.finite_replicates.le(20).all()
    assert (a.selected == np.floor(a.n * a.budget)).all()


def test_generated_counts_and_immutable_original_inputs():
    import json
    from facct.analysis.validate_inputs import sha, source_hashes
    from facct.professor_revision.run import OUT, ROOT
    manifest = json.loads((OUT / "manifest.json").read_text())
    assert source_hashes(ROOT) == manifest["source_hashes"]
    for name, digest in manifest["output_hashes"].items():
        assert sha(OUT / name) == digest
    p = pd.read_csv(OUT / "performance.csv")
    expected = {"D_ge3": (165, 42, 63, 68), "D_gt3": (57, 13, 26, 22),
                "followup": (19, 6, 12, 10)}
    for target, (n, h, full, prefix) in expected.items():
        rows = p[(p.domain == "mental_health") & (p.criterion == target) & (p.budget == .2)].set_index("policy")
        assert rows.concerns.eq(n).all() and rows.selected.eq(132).all()
        assert [rows.loc[k, "caught"] for k in ("HumT", "markers_full", "markers_300")] == [h, full, prefix]
        table = (ROOT / "facct/paper/overleaf/tables/prefix_threshold.tex").read_text()
        assert f"& {h} & {full} & {prefix} &" in table
    assert not p[(p.domain != "mental_health") & (p.criterion == "followup")].size
