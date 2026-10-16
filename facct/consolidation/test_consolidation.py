import pandas as pd
import pytest

from facct.consolidation.audit import ROOT, equality_mask, protected_hashes
from facct.consolidation.verify import compare_outputs


def test_equality_uses_strings_not_join_tier():
    frame = pd.DataFrame({"id": ["a", "b"]})
    prov = pd.DataFrame({"id": ["b", "a"], "comparison": ["raw_equal", "other_difference"],
                         "tier": ["fuzzy", "full"]})
    assert equality_mask(frame, prov).tolist() == [False, True]
    with pytest.raises(ValueError):
        equality_mask(frame, prov.iloc[:1])
    with pytest.raises(ValueError):
        equality_mask(frame, pd.concat([prov, prov]))


def test_output_comparison_rejects_changed_missing_and_extra_files(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir()
    b.mkdir()
    (a / "table.csv").write_text("n\n1\n")
    with pytest.raises(ValueError):
        compare_outputs(a, b)
    (b / "table.csv").write_text("n\n2\n")
    with pytest.raises(ValueError):
        compare_outputs(a, b)
    (b / "table.csv").write_text("n\n1\n")
    assert list(compare_outputs(a, b)) == ["table.csv"]
    (b / "extra.csv").write_text("n\n1\n")
    with pytest.raises(ValueError):
        compare_outputs(a, b)


def test_generated_provenance_counts_and_protected_inputs():
    import json
    out = ROOT / "facct/consolidation/outputs"
    assert json.loads((out / "protected_before.json").read_text()) == protected_hashes()
    comp = pd.read_csv(out / "subset_composition.csv")
    for domain in ("education", "health"):
        for criterion in ("D_ge3", "F_lt4", "OA_lt4"):
            g = comp[(comp.domain == domain) & (comp.criterion == criterion) &
                     (comp.category == "all")].set_index("batch")
            for column in ("n", "concerns"):
                assert g.loc["full", column] == g.loc["byte_identical", column] + g.loc["different_text", column]
    assert len(pd.read_csv(out / "verified_subset_operating_points.csv")) == 48
    checks = pd.read_csv(out / "provenance_checks.csv")
    assert checks.export_trunc_equals_export_first300.sum() == 830
    assert checks.export_trunc_equals_rated_first300.sum() == 783
    assert checks.differing_pairs_with_same_recorded_prefix.sum() == 12
    assert not checks.scorer_invocation_authenticated.any()


def test_aggregate_checker_uses_reference_budget(capsys):
    from facct.consolidation.review_aggregates import main
    main()
    assert '"incremental_cells": 9' in capsys.readouterr().out


def test_candidate_excludes_raw_text_and_identity_fields(tmp_path):
    from facct.consolidation.build_artifact import safe_csv, payload
    example = tmp_path / "example.csv"
    example.write_text("domain,response\nhealth,private text\n")
    assert not safe_csv(example)
    example.write_text("domain,annotator_id\nhealth,person\n")
    assert not safe_csv(example)
    included = payload()
    assert not any("manifest.json" in n for n in included)
    assert not any(n.startswith(("data/", "submission/", "analysis/processed/")) for n in included)
    assert b"NOT A FULL DATA RELEASE" in included["README.md"]
