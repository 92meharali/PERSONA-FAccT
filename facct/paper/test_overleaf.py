"""Integrity checks for the portable typesetting package, not a TeX compiler."""
import csv
import json
import re
import zipfile

from facct.paper.build_overleaf import DEST, ROOT, DOMAINS, sha, validate


def test_sources_assets_and_citations():
    assert validate()["cited_references"] == 24


def test_submission_uses_completed_evidence_not_future_protocol():
    main = (DEST / "main.tex").read_text()
    assert "When Tone Scores Allocate Attention" in main
    assert "RQ1: Enrichment." in main
    assert "RQ2: Comparative allocation." in main
    assert "RQ3: Incremental value." in main
    assert "RQ4: Distribution of coverage." in main
    assert "sec:capability_study" not in main
    assert "Capability-Study Readiness" not in main
    assert "Neither experiment is part of the present evidence." in main
    assert "Generative AI usage statement" in main
    assert "Ethics statement" in main
    assert "\\clearpage\n\\bibliographystyle" in main


def test_generated_reference_counts():
    with (ROOT / "facct/outputs/tables/screening.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    coverage = (DEST / "tables/coverage.tex").read_text()
    numbers = (DEST / "tables/numbers.tex").read_text()
    for domain, _, prefix in DOMAINS:
        selected = [r for r in rows if r["domain"] == domain and r["policy"] == "high_H"
                    and float(r["budget"]) == .2]
        assert len(selected) == 3
        for row in selected:
            assert f"{int(float(row['caught']))}/{row['concerns']}" in coverage
        d = next(r for r in selected if r["criterion"] == "D_ge3")
        assert ("\\newcommand{\\" + prefix + "Recall}{" + f"{100 * float(d['recall']):.1f}" + r"\%}") in numbers


def test_archive_and_manifest():
    manifest = json.loads((DEST / "package_manifest.json").read_text())
    assert manifest["analysis_manifest_sha256"] == sha(ROOT / "facct/outputs/manifest.json")
    assert manifest["screening_table_sha256"] == sha(ROOT / "facct/outputs/tables/screening.csv")
    assert manifest["revision_manifest_sha256"] == sha(ROOT / "facct/revision/outputs/manifest.json")
    assert manifest["conditional_manifest_sha256"] == sha(ROOT / "facct/conditional/outputs/manifest.json")
    assert manifest["allocation_manifest_sha256"] == sha(ROOT / "facct/allocation/outputs/manifest.json")
    assert manifest["consolidation_manifest_sha256"] == sha(ROOT / "facct/consolidation/outputs/manifest.json")
    assert manifest["annotation_manifest_sha256"] == sha(ROOT / "facct/independent_annotation/outputs/manifest.json")
    for relative, expected in manifest["files"].items():
        assert sha(DEST / relative) == expected, relative
    with zipfile.ZipFile(ROOT / manifest.get("release_archive", "facct/releases/PERSONA_FAccT_2027_Overleaf.zip")) as archive:
        assert archive.testzip() is None
        assert "main.tex" in archive.namelist()
        for name in archive.namelist():
            assert not name.startswith("/") and ".." not in name.split("/")
            assert archive.read(name) == (DEST / name).read_bytes()
    assert (DEST / "acmart.cls").read_bytes() == (ROOT / "paper/acmart.cls").read_bytes()
    assert (DEST / "ACM-Reference-Format.bst").read_bytes() == (ROOT / "paper/ACM-Reference-Format.bst").read_bytes()


def test_no_unresolved_generated_macros():
    main = (DEST / "main.tex").read_text()
    definitions = (DEST / "tables/numbers.tex").read_text() + (DEST / "tables/annotation_numbers.tex").read_text()
    used = set(re.findall(r"\\((?:MH|ED|GH|IA)[A-Za-z]+)\b", main))
    defined = set(re.findall(r"\\newcommand\{\\([A-Za-z]+)\}", definitions))
    assert used <= defined


def test_complete_conditional_tables():
    with (ROOT / "facct/conditional/outputs/performance.csv").open() as stream:
        rows = [r for r in csv.DictReader(stream) if float(r["budget"]) == .2]
    assert len(rows) == 63
    for domain, _, _ in DOMAINS:
        held = (DEST / f"tables/held_{domain}.tex").read_text()
        full = (DEST / f"tables/full_{domain}.tex").read_text()
        # Data rows follow the header and precede booktabs' bottom rule.
        assert len(held.split(r"\midrule")[1].split(r"\bottomrule")[0].strip().splitlines()) == 21
        assert len(full.split(r"\midrule")[1].split(r"\bottomrule")[0].strip().splitlines()) == 15
        for r in rows:
            if r["domain"] != domain:
                continue
            caught = (f"{float(r['caught']):.2f}" if r["policy"] == "uniform_random"
                      else str(int(float(r["caught"]))))
            assert f"{caught}/{r['concerns']}" in held
            ci = f"{100*float(r['recall']):.1f} [{100*float(r['recall_lo']):.1f}, {100*float(r['recall_hi']):.1f}]"
            assert ci in held
    with (ROOT / "facct/conditional/outputs/conditional_lift.csv").open() as stream:
        contrasts = [r for r in csv.DictReader(stream) if float(r["budget"]) == .2]
    assert len(contrasts) == 9
    assert all(float(r["lo"]) <= 0 <= float(r["hi"]) for r in contrasts)
    main = (DEST / "main.tex").read_text()
    for domain, _, _ in DOMAINS:
        assert "\\input{tables/held_" + domain + "}" in main
        assert "\\input{tables/full_" + domain + "}" in main
    assert r"\input{tables/conditional}" in main
    assert "No trained policy requires" not in main
    assert "No policy is trained" not in main


def test_common_queue_presentation_complete():
    table=(DEST/"tables/common_queue_conditions.tex").read_text()
    assert len(table.split(r"\midrule")[1].split(r"\bottomrule")[0].strip().splitlines())==18
    slots=(DEST/"tables/common_queue_slots.tex").read_text()
    assert len(slots.split(r"\midrule")[1].split(r"\bottomrule")[0].strip().splitlines())==6
    main=(DEST/"main.tex").read_text()
    assert "figures/paired_summary.pdf" in main and "figures/workload_targets.pdf" in main
    assert "not which responses enter the queue" in main
    assert "algebraically, not coincidentally" in main
    coverage = (DEST / "tables/coverage.tex").read_text()
    assert all(count in coverage for count in ("42/165", "7/12", "10/23"))
    assert "We do not perform equivalence testing" in main


def test_annotation_counts_and_all_sensitivity_targets():
    source = ROOT / "facct/independent_annotation/outputs"
    with (source / "policy_metrics.csv").open() as stream:
        rows = [r for r in csv.DictReader(stream) if r["family"] == "original"
                and float(r["budget"]) == .2]
    coverage = (DEST / "tables/annotation_coverage.tex").read_text()
    for row in rows:
        if row["target"] == "resolved_ABC":
            assert f"{float(row['caught']):g}/{row['positives']}" in coverage
    sensitivity = (DEST / "tables/annotation_sensitivity.tex").read_text()
    assert len(sensitivity.split(r"\midrule")[1].split(r"\bottomrule")[0].strip().splitlines()) == 7
    for target in {r["target"] for r in rows}:
        h = next(r for r in rows if r["target"] == target and r["policy"] == "HumT")
        m = next(r for r in rows if r["target"] == target and r["policy"] == "markers_normalized")
        expected = f"{h['positives']} & {float(h['caught']):g} & {float(m['caught']):g}"
        assert expected in sensitivity
    with (source / "bootstrap_intervals.csv").open() as stream:
        for row in csv.DictReader(stream):
            if row["quantity"] == "HumT_minus_markers":
                assert f"[{100*float(row['lo']):+.1f}, {100*float(row['hi']):+.1f}]" in sensitivity


def test_annotation_reporting_boundaries_and_package_privacy():
    main = (DEST / "main.tex").read_text()
    for name in ("annotation_coverage", "annotation_sensitivity", "annotation_budgets", "annotation_overlap"):
        assert "\\input{tables/" + name + "}" in main
    assert "collects no new human-participant data" not in main
    assert "no external participant evidence is claimed" not in main
    assert "same-instruction reliability" in main
    assert "Both intervals include zero" in main
    assert "not uncertainty in the exact corpus counts" in main
    assert "uses original labels rather than the follow-up target" in main
    assert "informed consent and institutional ethics coverage preceded annotation" in main
    assert "pending forms" not in main and "internal-review draft" not in main
    assert "There is no comparison with an LLM judge or semantic screen." in main
    assert "Relationship to the Companion Study" in main
    manifest = json.loads((DEST / "package_manifest.json").read_text())
    with zipfile.ZipFile(ROOT / manifest.get("release_archive", "facct/releases/PERSONA_FAccT_2027_Overleaf.zip")) as archive:
        assert not any("raw_ratings" in n or "rating_sheet" in n or "private_study_id" in n
                       for n in archive.namelist())


def test_annotation_build_rejects_changed_evidence(tmp_path, monkeypatch):
    import pytest
    from facct.paper import build_annotation_assets
    (tmp_path / "manifest.json").write_text(json.dumps({"output_hashes": {"changed.csv": "incorrect"}}))
    (tmp_path / "changed.csv").write_text("tampered\n")
    monkeypatch.setattr(build_annotation_assets, "SOURCE", tmp_path)
    with pytest.raises(AssertionError, match="Annotation output changed"):
        build_annotation_assets.build(lambda *args: None)
