"""Historical-vs-rescored HumT authentication audit.

Given the recorded (historical) HumT score, the annotated text, the export
text used for the historical scorer call (where available) and a fresh
rescoring of the annotated text with the public HumT implementation, this
module reports:

* text provenance: how many annotated/export pairs are byte-identical,
  identical after normalization, or substantively different;
* score agreement: Pearson, Spearman, Lin's concordance, mean absolute
  difference, and the share of items whose rank changes by more than a
  tolerance;
* decision invariance: whether the fixed-capacity selection and the number
  of captured positives change when the rescored values replace the
  historical ones, overall and on the byte-identical subset.

The rescoring itself must be produced with the authors' pinned HumT
implementation (GPT-2 He/She-vs-It contrast on the 300-character prefix);
record its commit hash and seed in the manifest you pass with ``--note``.

CLI
---
    python -m analysis.score_audit --table scores.csv --capacity 132 \
        --historical humt_recorded --rescored humt_rescored \
        [--annotated response] [--export export_text] [--positive positive]
"""

from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from scipy import stats

from .common import flags_at_queue_size, normalize_text, read_table, require_columns, sensitivity


def lins_ccc(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    mx, my = x.mean(), y.mean()
    vx, vy = x.var(), y.var()
    cov = ((x - mx) * (y - my)).mean()
    denom = vx + vy + (mx - my) ** 2
    return float(2 * cov / denom) if denom > 0 else float("nan")


def provenance(df: pd.DataFrame, annotated: str, export: str) -> dict:
    a = df[annotated].astype(str)
    e = df[export].astype(str)
    byte_identical = (a == e)
    norm_identical = a.map(normalize_text) == e.map(normalize_text)
    prefix_identical = a.str[:300] == e.str[:300]
    return {
        "pairs": int(len(df)),
        "byte_identical": int(byte_identical.sum()),
        "identical_after_normalization": int((norm_identical & ~byte_identical).sum()),
        "substantively_different": int((~norm_identical).sum()),
        "prefix300_differs": int((~prefix_identical).sum()),
    }


def agreement(h: np.ndarray, r: np.ndarray, rank_tol: int) -> dict:
    ok = np.isfinite(h) & np.isfinite(r)
    h, r = h[ok], r[ok]
    rank_h = stats.rankdata(-h, method="average")
    rank_r = stats.rankdata(-r, method="average")
    return {
        "n": int(ok.sum()),
        "pearson": round(float(stats.pearsonr(h, r)[0]), 4),
        "spearman": round(float(stats.spearmanr(h, r)[0]), 4),
        "lin_ccc": round(lins_ccc(h, r), 4),
        "mean_abs_diff": round(float(np.abs(h - r).mean()), 4),
        "max_abs_diff": round(float(np.abs(h - r).max()), 4),
        f"rank_moves_more_than_{rank_tol}": int((np.abs(rank_h - rank_r) > rank_tol).sum()),
    }


def decision_invariance(df: pd.DataFrame, hist: str, resc: str, capacity: int, positive: str | None, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    f_h = flags_at_queue_size(df[hist].to_numpy(float), capacity, np.random.default_rng(seed))
    f_r = flags_at_queue_size(df[resc].to_numpy(float), capacity, rng)
    out = {
        "capacity": capacity,
        "selected_by_both": int((f_h & f_r).sum()),
        "selected_only_historical": int((f_h & ~f_r).sum()),
        "selected_only_rescored": int((~f_h & f_r).sum()),
        "jaccard": round(float((f_h & f_r).sum() / max(1, (f_h | f_r).sum())), 4),
    }
    if positive and positive in df.columns:
        pos = df[positive].astype(int).to_numpy()
        ch, t = sensitivity(f_h, pos)
        cr, _ = sensitivity(f_r, pos)
        out["positives"] = t
        out["caught_historical"] = ch
        out["caught_rescored"] = cr
    return out


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", required=True)
    ap.add_argument("--historical", default="humt_recorded")
    ap.add_argument("--rescored", default="humt_rescored")
    ap.add_argument("--annotated", default=None, help="annotated text column")
    ap.add_argument("--export", default=None, help="export text column used for the historical call")
    ap.add_argument("--positive", default="positive")
    ap.add_argument("--capacity", type=int, required=True)
    ap.add_argument("--rank-tol", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20261002)
    ap.add_argument("--note", default="", help="rescoring provenance (implementation commit, seed, date)")
    args = ap.parse_args(argv)

    df = read_table(args.table)
    require_columns(df, [args.historical, args.rescored], args.table)
    report: dict = {"rescoring_note": args.note or None}
    if args.annotated and args.export and args.annotated in df.columns and args.export in df.columns:
        report["text_provenance"] = provenance(df, args.annotated, args.export)
        ident = df[df[args.annotated].astype(str) == df[args.export].astype(str)]
        report["decision_invariance_byte_identical_subset"] = decision_invariance(
            ident.reset_index(drop=True), args.historical, args.rescored, min(args.capacity, len(ident)), args.positive, args.seed
        )
    report["score_agreement"] = agreement(
        df[args.historical].to_numpy(float), df[args.rescored].to_numpy(float), args.rank_tol
    )
    report["decision_invariance_full_batch"] = decision_invariance(
        df, args.historical, args.rescored, args.capacity, args.positive, args.seed
    )
    report["reading"] = (
        "High concordance plus unchanged captured-positive counts means the recorded scores are "
        "decision-equivalent to a fresh run; residual rank moves bound how much a reviewer's queue "
        "could differ. This authenticates the values, not the historical invocation itself."
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
