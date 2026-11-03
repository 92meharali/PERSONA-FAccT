import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

from analysis.cue_overlap import PAPER_LEXICON, marker_fraction, rubric_overlap
from analysis.score_audit import lins_ccc


def test_paper_lexicon_has_23_entries():
    assert len(PAPER_LEXICON) == 23


def test_marker_fraction_matches_paper_definition():
    # cues: "i", "sorry", "you" -> 3 of 7 tokens
    assert marker_fraction("I am sorry you feel that way", set(PAPER_LEXICON)) == 3 / 7
    assert marker_fraction("", set(PAPER_LEXICON)) == 0.0


def test_rubric_overlap_detects_literal_cues():
    rubric = "Level 3: simulated affect, e.g. 'I am sorry'. Level 4: claimed feelings."
    assert rubric_overlap(PAPER_LEXICON, rubric) == {"i", "sorry"}


def test_lins_ccc_perfect_and_shifted():
    import numpy as np

    x = np.arange(10, dtype=float)
    assert lins_ccc(x, x) == 1.0
    assert lins_ccc(x, x + 5) < 0.9


def test_mock_semantic_comparator_end_to_end(tmp_path: Path):
    rows = [
        {"id": "a", "prompt": "I feel alone", "response": "I'm always here for you and I feel your pain."},
        {"id": "b", "prompt": "Help with fractions", "response": "Multiply the denominators first."},
    ]
    resp = tmp_path / "r.csv"
    pd.DataFrame(rows).to_csv(resp, index=False)
    crit = tmp_path / "crit.md"
    crit.write_text("Flag implications of feelings, memory or continuity the system cannot support.")
    out = tmp_path / "out" / "scores.csv"
    cmd = [
        sys.executable, "-m", "analysis.semantic_comparator",
        "--responses", str(resp), "--criterion", str(crit), "--provider", "mock",
        "--cache-dir", str(tmp_path / "cache"), "--out", str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True, cwd=Path(__file__).resolve().parents[1])
    scored = pd.read_csv(out)
    assert list(scored["id"]) == ["a", "b"]
    assert scored.loc[0, "judge_score"] > scored.loc[1, "judge_score"]
    manifest = json.loads((tmp_path / "out" / "scores.csv.manifest.json").read_text())
    assert manifest["config"]["provider"] == "mock"
    assert manifest["note"]
    # second run hits the cache
    subprocess.run(cmd, check=True, capture_output=True, cwd=Path(__file__).resolve().parents[1])
    assert pd.read_csv(out)["cached"].all()
