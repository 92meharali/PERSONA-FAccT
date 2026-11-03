"""Shared helpers: binomial intervals, matched-queue-size flagging, CSV IO."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats


@dataclass(frozen=True)
class Interval:
    estimate: float
    lower: float
    upper: float

    def as_pp(self) -> "Interval":
        """Return the interval in percentage points."""
        return Interval(self.estimate * 100, self.lower * 100, self.upper * 100)

    def fmt(self, pp: bool = True, digits: int = 1) -> str:
        iv = self.as_pp() if pp else self
        unit = " pp" if pp else ""
        return f"{iv.estimate:.{digits}f}{unit} [{iv.lower:.{digits}f}, {iv.upper:.{digits}f}]"


def wilson_ci(successes: int, n: int, alpha: float = 0.05) -> Interval:
    """Wilson score interval for a binomial proportion.

    Preferred over Wald for the small positive counts in the follow-up
    (n = 19), where Wald intervals are badly miscalibrated.
    """
    if n == 0:
        return Interval(float("nan"), float("nan"), float("nan"))
    z = stats.norm.ppf(1 - alpha / 2)
    p = successes / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return Interval(p, max(0.0, centre - half), min(1.0, centre + half))


def flags_at_queue_size(
    scores: np.ndarray, k: int, rng: np.random.Generator | None = None
) -> np.ndarray:
    """Flag the top-``k`` responses by score, breaking ties at random.

    Matched queue size is the comparison unit used throughout the paper:
    every detector gets to send exactly ``k`` responses to review, so the
    comparison is on *which* responses are selected, not on how many.
    Random tie-breaking (seeded by the caller) avoids the optimistic bias of
    stable sorting when many responses share a score (common for count-based
    marker baselines).
    """
    scores = np.asarray(scores, dtype=float)
    n = scores.shape[0]
    if k <= 0:
        return np.zeros(n, dtype=bool)
    if k >= n:
        return np.ones(n, dtype=bool)
    rng = rng or np.random.default_rng(0)
    jitter = rng.random(n)
    order = np.lexsort((jitter, -scores))  # primary: score desc, secondary: random
    flags = np.zeros(n, dtype=bool)
    flags[order[:k]] = True
    return flags


def sensitivity(flags: np.ndarray, positive: np.ndarray) -> tuple[int, int]:
    """Return (caught, total) positives for a flag vector."""
    positive = np.asarray(positive, dtype=bool)
    flags = np.asarray(flags, dtype=bool)
    return int((flags & positive).sum()), int(positive.sum())


_WS = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Canonical form for comparing exported vs annotated texts.

    Collapses whitespace, normalizes unicode (NFKC), strips BOMs and
    zero-width characters, and lowercases. Differences that survive this
    normalization are substantive (words changed), not formatting noise.
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\ufeff", "").replace("\u200b", "")
    text = _WS.sub(" ", text).strip().lower()
    return text


def text_hash(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()[:16]


def read_table(path: str) -> pd.DataFrame:
    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    if path.endswith(".jsonl"):
        return pd.read_json(path, lines=True)
    return pd.read_csv(path)


def require_columns(df: pd.DataFrame, cols: list[str], where: str) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"{where}: missing required column(s) {missing}; have {list(df.columns)}")
