"""Render the alignment-diagnostic forest plot from values reported in the paper.

Every number below is copied from the manuscript's tables (baselines,
prefix_threshold, annotation_coverage, Appendix D fit/OA contrasts). The
figure adds no evidence; it arranges paired HumT-minus-marker differences
across criteria and rater populations, not a causal scale of independence.

    python -m analysis.make_alignment_figure paper/figures/alignment_diagnostic.pdf
"""

from __future__ import annotations

import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# (label, estimate, lower, upper, supporting prompts, note)
# lower/upper None => paired interval reported in text as including zero but
# endpoints not tabulated in the package.
GROUPS = [
    (
        "Broad $\\overline{D}\\geq3$ — dimension raters",
        [
            ("Mental health", -12.7, -21.9, -4.3, 99, ""),
            ("Education", -16.7, -50.0, 16.7, 7, "sparse"),
            ("General health", -47.8, -63.2, -25.9, 15, ""),
        ],
    ),
    (
        "(i) Stricter $\\overline{D}>3$ — vs. 300-character markers",
        [
            ("Mental health", -15.8, -31.4, 0.0, 42, ""),
            ("Education", -37.5, -100.0, 36.1, 5, "sparse"),
            ("General health", -45.0, -66.7, -13.6, 13, ""),
        ],
    ),
    (
        "Overall appropriateness — separate rubric-blind raters",
        [
            ("Mental health", -1.5, -9.2, 8.4, 111, "later seed"),
            ("Education", 33.3, -7.7, 71.4, 10, ""),
            ("General health", -66.7, -100.0, -28.5, 7, "sparse"),
        ],
    ),
    (
        "(iv) Contextual reviewworthiness — external assessors",
        [
            ("Mental health", -31.6, -66.7, 4.3, 13, ""),
        ],
    ),
    (
        "Domain fit $\\overline{F}<4$ — dimension raters, for reference",
        [
            ("Mental health", -4.2, -14.6, 6.8, 77, "later seed"),
            ("Education", 36.0, 15.4, 58.6, 17, ""),
            ("General health", -5.8, -13.6, 2.9, 69, ""),
        ],
    ),
]


def main(out: str) -> None:
    rows = []
    for gi, (gname, items) in enumerate(GROUPS):
        rows.append(("__group__", gname))
        for it in items:
            rows.append(("__item__", it))
    n = len(rows)

    fig, ax = plt.subplots(figsize=(7.2, 0.27 * n + 0.8))
    y = n
    yticks, ylabels = [], []
    for kind, payload in rows:
        y -= 1
        if kind == "__group__":
            ax.text(-118, y - 0.1, payload, fontsize=8.3, fontweight="bold", va="center", ha="left")
            continue
        label, est, lo, hi, g, note = payload
        sparse = note == "sparse"
        color = "#444444"
        if lo is not None:
            ax.plot([lo, hi], [y, y], color=color, lw=1.2, solid_capstyle="butt")
        ax.plot(
            est, y, marker="o", ms=5.5, mfc="white" if (sparse or lo is None) else color,
            mec=color, mew=1.2, ls="none",
        )
        txt = f"{est:+.1f}"
        if lo is not None:
            txt += f"  [{lo:+.1f}, {hi:+.1f}]"
        else:
            txt += "  (interval includes 0)"
        txt += f"   G={g}"
        ax.text(104, y, txt, fontsize=7.5, va="center", ha="left", family="monospace")
        yticks.append(y)
        ylabels.append(label)

    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=8)
    ax.set_xlim(-120, 180)
    ax.set_ylim(-0.6, n - 0.4)
    ax.set_xticks([-100, -75, -50, -25, 0, 25, 50, 75, 100])
    ax.set_xlabel("HumT minus markers, recall at 20% capacity (percentage points)", fontsize=8.5)
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.text(-100, n - 0.5, "favors markers  \u2190", fontsize=7.5, ha="left", va="bottom", color="#555555")
    ax.text(100, n - 0.5, "\u2192  favors HumT", fontsize=7.5, ha="right", va="bottom", color="#555555")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "paper/figures/alignment_diagnostic.pdf")
