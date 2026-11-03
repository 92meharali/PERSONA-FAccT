"""Rubric-cue ablation for the marker baseline (label-alignment diagnostic).

The paper's Section on rubric alignment tests the alignment hypothesis
through its observable implications. This module adds the direct test that
needs response text: remove from the marker lexicon every cue that overlaps
the rubric's wording (or a named cue category), re-rank at the same exact
capacity, and report how much of the marker advantage survives.

Inputs
------
responses.csv   id, prompt_id, response, positive  (+ optional humt column)
lexicon.txt     one cue per line; optional "cue<TAB>category"
rubric.txt      the criterion text whose overlap with the lexicon is audited

CLI
---
    python -m analysis.cue_overlap --responses r.csv --lexicon lexicon.txt \
        --rubric rubric_D.txt --capacity 132 [--drop-category sympathy] [--humt humt]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from .common import flags_at_queue_size, read_table, require_columns, sensitivity, wilson_ci

TOKEN = re.compile(r"\b\w+\b")

# The paper's fixed 23-word dictionary (Appendix: Implementation).
PAPER_LEXICON = {
    "i": "pronoun", "me": "pronoun", "my": "pronoun", "mine": "pronoun", "myself": "pronoun",
    "we": "pronoun", "us": "pronoun", "our": "pronoun", "ours": "pronoun", "ourselves": "pronoun",
    "you": "pronoun", "your": "pronoun", "yours": "pronoun", "yourself": "pronoun", "yourselves": "pronoun",
    "hello": "greeting", "hi": "greeting", "hey": "greeting",
    "thanks": "politeness", "thank": "politeness", "welcome": "politeness", "please": "politeness",
    "sorry": "sympathy",
}


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(str(text).lower())


def marker_fraction(text: str, lexicon: set[str]) -> float:
    toks = tokenize(text)
    if not toks:
        return 0.0
    return sum(t in lexicon for t in toks) / len(toks)


def load_lexicon(path: str | None) -> dict[str, str]:
    if path is None:
        return dict(PAPER_LEXICON)
    lex: dict[str, str] = {}
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        lex[parts[0].strip().lower()] = parts[1].strip().lower() if len(parts) > 1 else "uncategorized"
    return lex


def rubric_overlap(lexicon: dict[str, str], rubric_text: str) -> set[str]:
    """Cues that literally appear in the rubric text (after tokenization)."""
    rubric_tokens = set(tokenize(rubric_text))
    return {cue for cue in lexicon if cue in rubric_tokens}


def evaluate(df: pd.DataFrame, lexicon: set[str], capacity: int, seed: int) -> dict:
    scores = df["response"].map(lambda t: marker_fraction(t, lexicon)).to_numpy()
    flags = flags_at_queue_size(scores, capacity, np.random.default_rng(seed))
    caught, total = sensitivity(flags, df["positive"].to_numpy())
    return {"caught": caught, "positives": total, "recall": wilson_ci(caught, total).fmt(), "n_cues": len(lexicon)}


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--responses", required=True)
    ap.add_argument("--lexicon", help="defaults to the paper's 23-word list")
    ap.add_argument("--rubric", required=True)
    ap.add_argument("--capacity", type=int, required=True, help="exact slots, e.g. 132")
    ap.add_argument("--drop-category", action="append", default=[], help="lexicon category to ablate (repeatable)")
    ap.add_argument("--humt", help="column with recorded HumT scores, for a same-capacity reference")
    ap.add_argument("--seed", type=int, default=20261002)
    args = ap.parse_args(argv)

    df = read_table(args.responses)
    require_columns(df, ["id", "response", "positive"], args.responses)
    df["positive"] = df["positive"].astype(int)
    lex = load_lexicon(args.lexicon)
    rubric = Path(args.rubric).read_text()
    overlap = rubric_overlap(lex, rubric)

    report: dict = {
        "capacity": args.capacity,
        "lexicon_size": len(lex),
        "cues_overlapping_rubric": sorted(overlap),
        "variants": {},
    }
    report["variants"]["full_lexicon"] = evaluate(df, set(lex), args.capacity, args.seed)
    report["variants"]["minus_rubric_overlap"] = evaluate(df, set(lex) - overlap, args.capacity, args.seed)
    for cat in args.drop_category:
        kept = {c for c, k in lex.items() if k != cat}
        report["variants"][f"minus_category_{cat}"] = evaluate(df, kept, args.capacity, args.seed)
    if args.humt and args.humt in df.columns:
        flags = flags_at_queue_size(df[args.humt].to_numpy(dtype=float), args.capacity, np.random.default_rng(args.seed))
        c, t = sensitivity(flags, df["positive"].to_numpy())
        report["humt_reference"] = {"caught": c, "positives": t, "recall": wilson_ci(c, t).fmt()}
    report["reading"] = (
        "If the marker advantage over HumT disappears once rubric-overlapping cues are removed, "
        "alignment explains it; if it persists, alignment is at most a partial contributor."
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
