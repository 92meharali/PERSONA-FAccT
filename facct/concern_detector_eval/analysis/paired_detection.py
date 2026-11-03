"""Paired comparison of two screening policies on the same positive cases.

Addresses the follow-up inference problem: with few positives (the
contextual-reviewworthiness target has 19 across 13 prompts) a wide cluster
bootstrap interval is uninformative on its own. This module reports the
complementary quantities that make the evidence interpretable:

* exact McNemar test on the discordant positives (which cases only one
  policy caught), across the full range of possible overlaps when the
  overlap is unknown;
* Wilson intervals for each policy's sensitivity;
* a paired prompt-cluster bootstrap for the sensitivity difference;
* the Bayesian posterior probability that policy A beats policy B on
  discordant cases (Beta(1,1) prior);
* the number of positives a replication needs for 80% power at the
  observed effect size.

CLI
---
    python -m analysis.paired_detection --csv flags.csv --a markers --b humt
    python -m analysis.paired_detection --counts 19 12 6        # unknown overlap
    python -m analysis.paired_detection --counts 19 12 6 --both 5

``flags.csv`` needs columns ``positive`` (0/1), the two flag columns, and
optionally ``prompt_id`` for the cluster bootstrap.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from scipy import stats

from .common import Interval, read_table, require_columns, wilson_ci


@dataclass
class DiscordantTable:
    both: int
    a_only: int
    b_only: int
    neither: int

    @property
    def n(self) -> int:
        return self.both + self.a_only + self.b_only + self.neither


def mcnemar_exact(a_only: int, b_only: int) -> float:
    """Two-sided exact McNemar p-value from the discordant counts."""
    n_disc = a_only + b_only
    if n_disc == 0:
        return 1.0
    k = min(a_only, b_only)
    return float(min(1.0, 2 * stats.binom.cdf(k, n_disc, 0.5)))


def posterior_a_better(a_only: int, b_only: int, prior: tuple[float, float] = (1.0, 1.0)) -> float:
    """P(A catches more than B on discordant cases | data), Beta prior."""
    alpha, beta = prior
    return float(1 - stats.beta.cdf(0.5, alpha + a_only, beta + b_only))


def sensitivity_diff_ci_from_table(t: DiscordantTable, alpha: float = 0.05) -> Interval:
    """Wald-type interval for the paired difference in sensitivity (A - B).

    Uses the standard paired-proportion variance; adequate as a sanity
    check against the bootstrap but not preferred for tiny samples.
    """
    n = t.n
    if n == 0:
        return Interval(float("nan"), float("nan"), float("nan"))
    d = (t.a_only - t.b_only) / n
    var = ((t.a_only + t.b_only) / n - d**2) / n
    z = stats.norm.ppf(1 - alpha / 2)
    half = z * np.sqrt(max(var, 0.0))
    return Interval(d, d - half, d + half)


def positives_needed(
    sens_a: float, sens_b: float, discordant_rate: float, power: float = 0.8, alpha: float = 0.05
) -> int:
    """Positives required for a two-sided McNemar test at the given power.

    Normal approximation (Connor 1987). ``discordant_rate`` is the expected
    fraction of positives caught by exactly one policy; it is bounded below
    by |sens_a - sens_b| and above by min(sens_a + sens_b, 2 - sens_a - sens_b).
    """
    d = abs(sens_a - sens_b)
    if d == 0:
        return int(1e9)
    pd_ = discordant_rate
    if pd_ < d:
        raise ValueError("discordant_rate cannot be smaller than |sens_a - sens_b|")
    z_a = stats.norm.ppf(1 - alpha / 2)
    z_b = stats.norm.ppf(power)
    n = (z_a * np.sqrt(pd_) + z_b * np.sqrt(pd_ - d**2)) ** 2 / d**2
    return int(np.ceil(n))


def cluster_bootstrap_diff(
    positive: np.ndarray,
    flag_a: np.ndarray,
    flag_b: np.ndarray,
    cluster: np.ndarray | None,
    n_boot: int = 2000,
    seed: int = 20261010,
    alpha: float = 0.05,
) -> Interval:
    """Percentile interval for sensitivity(A) - sensitivity(B).

    Resamples clusters (prompts) with replacement when ``cluster`` is given,
    otherwise resamples positives. Flags are held fixed, which mirrors a
    design where the queue was already selected and only the label target
    is new; use the paper's re-ranking bootstrap when the queue itself
    should vary with the batch.
    """
    positive = np.asarray(positive, dtype=bool)
    flag_a = np.asarray(flag_a, dtype=bool)
    flag_b = np.asarray(flag_b, dtype=bool)
    rng = np.random.default_rng(seed)

    def diff(idx: np.ndarray) -> float:
        p = positive[idx]
        if p.sum() == 0:
            return np.nan
        return (flag_a[idx] & p).sum() / p.sum() - (flag_b[idx] & p).sum() / p.sum()

    if cluster is None:
        units = [np.array([i]) for i in range(len(positive))]
    else:
        cluster = np.asarray(cluster)
        units = [np.flatnonzero(cluster == c) for c in pd.unique(cluster)]
    units_arr = np.empty(len(units), dtype=object)
    for i, u in enumerate(units):
        units_arr[i] = u

    draws = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.integers(0, len(units_arr), len(units_arr))
        idx = np.concatenate(units_arr[pick].tolist())
        draws[b] = diff(idx)
    finite = draws[np.isfinite(draws)]
    est = diff(np.arange(len(positive)))
    lo, hi = np.percentile(finite, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return Interval(est, lo, hi)


def summarize_counts(n_pos: int, caught_a: int, caught_b: int, both: int | None, name_a: str, name_b: str) -> dict:
    """Report everything derivable from marginal catch counts.

    When the overlap is unknown, iterate over every feasible value so the
    conclusion does not depend on an unobserved quantity.
    """
    out: dict = {
        "n_positive": n_pos,
        name_a: {"caught": caught_a, "sensitivity": wilson_ci(caught_a, n_pos).fmt()},
        name_b: {"caught": caught_b, "sensitivity": wilson_ci(caught_b, n_pos).fmt()},
        "difference_pp": round(100 * (caught_a - caught_b) / n_pos, 1),
    }
    lo_both = max(0, caught_a + caught_b - n_pos)
    hi_both = min(caught_a, caught_b)
    overlaps = [both] if both is not None else list(range(lo_both, hi_both + 1))
    rows = []
    for x in overlaps:
        a_only, b_only = caught_a - x, caught_b - x
        t = DiscordantTable(x, a_only, b_only, n_pos - x - a_only - b_only)
        rows.append(
            {
                "both": x,
                f"{name_a}_only": a_only,
                f"{name_b}_only": b_only,
                "neither": t.neither,
                "mcnemar_exact_p": round(mcnemar_exact(a_only, b_only), 3),
                f"posterior_P({name_a}>{name_b})": round(posterior_a_better(a_only, b_only), 3),
                "wald_diff": sensitivity_diff_ci_from_table(t).fmt(),
            }
        )
    out["by_overlap"] = rows
    sa, sb = caught_a / n_pos, caught_b / n_pos
    d = abs(sa - sb)
    out["replication_positives_for_80pct_power"] = {
        "min_discordance": positives_needed(sa, sb, d),
        "max_discordance": positives_needed(sa, sb, min(sa + sb, 2 - sa - sb)),
    }
    return out


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", help="table with positive, flag columns, optional prompt_id")
    ap.add_argument("--a", default="markers", help="flag column / name for policy A")
    ap.add_argument("--b", default="humt", help="flag column / name for policy B")
    ap.add_argument("--counts", nargs=3, type=int, metavar=("N_POS", "CAUGHT_A", "CAUGHT_B"))
    ap.add_argument("--both", type=int, help="positives caught by both (if known)")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261010)
    args = ap.parse_args(argv)

    if args.counts:
        n_pos, ca, cb = args.counts
        print(json.dumps(summarize_counts(n_pos, ca, cb, args.both, args.a, args.b), indent=2))
        return
    if not args.csv:
        ap.error("provide --csv or --counts")

    df = read_table(args.csv)
    require_columns(df, ["positive", args.a, args.b], args.csv)
    pos = df["positive"].astype(bool).to_numpy()
    fa = df[args.a].astype(bool).to_numpy()
    fb = df[args.b].astype(bool).to_numpy()
    both = int((pos & fa & fb).sum())
    report = summarize_counts(int(pos.sum()), int((pos & fa).sum()), int((pos & fb).sum()), both, args.a, args.b)
    cluster = df["prompt_id"].to_numpy() if "prompt_id" in df.columns else None
    ci = cluster_bootstrap_diff(pos, fa, fb, cluster, n_boot=args.n_boot, seed=args.seed)
    report["bootstrap_diff_pp"] = ci.fmt()
    report["bootstrap_unit"] = "prompt cluster" if cluster is not None else "response"
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
