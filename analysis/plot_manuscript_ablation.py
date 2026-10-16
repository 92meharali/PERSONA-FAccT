"""Render the manuscript's six-family grouped-CV comparison."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "analysis" / "outputs" / "tables" / "cv_performance.csv"
OUTPUT = ROOT / "paper" / "figures" / "fig_cv_model_comparison.png"

ORDER = ["H_only", "E_only", "D_only", "F_only", "E+D+F", "H+E+D+F"]
LABELS = ["H", "E", "D", "F", "E+D+F", "Full"]
DOMAINS = [
    ("mental_health", "Mental health"),
    ("education", "Education"),
    ("health", "General health"),
    ("pooled", "Pooled (all models include domain)"),
]
COLORS = ["#7A8BA8", "#76A5AF", "#D98880", "#7FB069", "#B39DDB", "#4C78A8"]


def main() -> None:
    data = pd.read_csv(INPUT).set_index(["domain", "specification"])
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 7.2), sharey=True)

    for ax, (domain, title) in zip(axes.flat, DOMAINS):
        block = data.loc[domain].reindex(ORDER)
        values = block["cv_r2_mean"].to_numpy()
        lows = block["cv_r2_boot_ci_low"].to_numpy()
        highs = block["cv_r2_boot_ci_high"].to_numpy()
        x = np.arange(len(ORDER))

        ax.bar(
            x,
            values,
            color=COLORS,
            edgecolor="#333333",
            linewidth=0.5,
            yerr=np.vstack([values - lows, highs - values]),
            capsize=3,
            error_kw={"elinewidth": 1, "capthick": 1},
        )
        ax.axhline(0, color="#444444", linewidth=0.8)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xticks(x, LABELS)
        ax.set_ylim(-0.16, 0.82)
        ax.grid(axis="y", alpha=0.22)
        ax.tick_params(axis="both", labelsize=9)

    axes[0, 0].set_ylabel("Prompt-grouped cross-validated $R^2$")
    axes[1, 0].set_ylabel("Prompt-grouped cross-validated $R^2$")
    fig.suptitle("Cross-validated performance by model family", fontsize=13)
    fig.tight_layout()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
