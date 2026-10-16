import json

from .build_review_tables import ROOT, build, sha


def test_generated_review_reproducible(tmp_path):
    a=build(output=tmp_path/"a")
    b=build(output=tmp_path/"b")
    assert a==b
    text=(tmp_path/"a/computational_review_draft.md").read_text()
    assert "{{" not in text
    assert "42/165" in text and "7/12" in text and "10/23" in text
    assert "No new interviews" in text
    assert "not submission-ready" in text


def test_original_analysis_still_frozen():
    manifest=json.loads((ROOT/"facct/outputs/manifest.json").read_text())
    for relative,expected in manifest["code_and_protocol_hashes"].items():
        assert sha(ROOT/relative)==expected
    for relative,expected in manifest["output_hashes"].items():
        assert sha(ROOT/"facct/outputs"/relative)==expected
