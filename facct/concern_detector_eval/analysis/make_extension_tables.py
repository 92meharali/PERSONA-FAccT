"""Render LaTeX tables and a numbers macro file from extension_run outputs.

    python -m analysis.make_extension_tables analysis_outputs paper/tables
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

DOM = {"mental_health": "Mental health", "education": "Education", "health": "General health"}
CRIT = {"D>=3": "$\\overline D\\geq3$", "D>3": "$\\overline D>3$", "F<4": "$\\overline F<4$", "OA<4": "$\\overline{\\mathrm{OA}}<4$"}
POL = {
    "high_H": "HumT",
    "markers": "Markers (23 cues)",
    "markers_minus_sorry": "Markers minus \\emph{sorry}",
    "markers_minus_first_person": "Markers minus first person",
    "markers_no_pronouns": "Markers, no pronouns (8 cues)",
    "embed_sim": "Embedding similarity",
    "nli_zero_shot": "Zero-shot NLI judge",
}
MODEL = {"lex": "Lexical", "lex+H": "Lexical + HumT", "lex+emb": "Lexical + embedding", "lex+emb+H": "Lexical + embedding + HumT", "emb": "Embedding only"}


def iv(row) -> str:
    return f"{row.diff_pp:+.1f} [{row.lo_pp:+.1f}, {row.hi_pp:+.1f}]"


def cue_ablation(counts: pd.DataFrame, contrasts: pd.DataFrame) -> str:
    pols = ["high_H", "markers", "markers_minus_sorry", "markers_minus_first_person", "markers_no_pronouns"]
    lines = [
        "\\begin{table}[t]", "\\centering\\small",
        "\\caption{Cue-removal sensitivity at 20\\% capacity for $\\overline D\\geq3$. Each lexicon re-ranks the batch with unchanged tie keys. Differences are policy minus HumT recall, with paired 2,000-draw pointwise 95\\% intervals. Surviving advantages do not exclude rubric alignment through remaining or correlated cues.}",
        "\\label{tab:cue_ablation}", "\\begin{tabular}{llrrrl}", "\\toprule",
        "Domain & Lexicon & Cues & Caught/$P$ & Recall & Minus HumT [95\\%] \\\\", "\\midrule",
    ]
    ncues = {"high_H": "--", "markers": 23, "markers_minus_sorry": 22, "markers_minus_first_person": 13, "markers_no_pronouns": 8}
    for d in DOM:
        first = True
        for p in pols:
            r = counts[(counts.domain == d) & (counts.policy == p)].iloc[0]
            c = contrasts[(contrasts.domain == d) & (contrasts.policy == p) & (contrasts.versus == "high_H") & (contrasts.criterion == "D>=3")]
            delta = iv(c.iloc[0]) if len(c) else "--"
            lines.append(f"{DOM[d] if first else ''} & {POL[p]} & {ncues[p]} & {r['caught_D>=3']}/{r['P_D>=3']} & {100*r['caught_D>=3']/r['P_D>=3']:.1f} & {delta} \\\\")
            first = False
        if d != "health":
            lines.append("\\addlinespace")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(lines)


def semantic_fixed(counts: pd.DataFrame, contrasts: pd.DataFrame) -> str:
    pols = ["high_H", "markers", "embed_sim", "nli_zero_shot"]
    lines = [
        "\\begin{table*}[t]", "\\centering\\footnotesize",
        "\\caption{Pinned semantic screens as fixed, label-free policies at 20\\% capacity, alongside HumT and markers. One ranking per domain is projected on all three criteria. Paired differences (percentage points) are policy minus HumT and policy minus markers for the same criterion, with 2,000-draw prompt-cluster intervals (exploratory pointwise 95\\%). $\\dagger$: fewer than ten supporting prompts.}",
        "\\label{tab:semantic_fixed}", "\\begin{tabular}{lllrrll}", "\\toprule",
        "Domain & Criterion & Policy & Caught/$P$ & Recall & Minus HumT & Minus markers \\\\", "\\midrule",
    ]
    for d in DOM:
        for c in ("D>=3", "F<4", "OA<4"):
            r0 = counts[(counts.domain == d) & (counts.policy == "high_H")].iloc[0]
            sparse = "$^{\\dagger}$" if r0[f"G_{c}"] < 10 else ""
            for i, p in enumerate(pols):
                r = counts[(counts.domain == d) & (counts.policy == p)].iloc[0]
                def ctr(v):
                    q = contrasts[(contrasts.domain == d) & (contrasts.policy == p) & (contrasts.versus == v) & (contrasts.criterion == c)]
                    return iv(q.iloc[0]) if len(q) else "--"
                dom = DOM[d] if (c == "D>=3" and i == 0) else ""
                crit = (CRIT[c] + sparse) if i == 0 else ""
                rec = f"{100*r[f'caught_{c}']/r[f'P_{c}']:.1f}"
                lines.append(f"{dom} & {crit} & {POL[p]} & {r[f'caught_{c}']}/{r[f'P_{c}']} & {rec} & {ctr('high_H')} & {ctr('markers')} \\\\")
            lines.append("\\addlinespace")
    lines[-1] = "\\bottomrule"
    lines += ["\\end{tabular}", "\\end{table*}", ""]
    return "\n".join(lines)


def semantic_compact(counts: pd.DataFrame, contrasts: pd.DataFrame) -> str:
    pols = ["high_H", "markers", "embed_sim", "nli_zero_shot"]
    short = {"high_H": "HumT", "markers": "Markers", "embed_sim": "Similarity", "nli_zero_shot": "NLI judge"}
    lines = [
        "\\begin{table}[t]", "\\centering\\small",
        "\\caption{Fixed semantic screens at 20\\% capacity (132/83/83 slots). Captured cases out of $P$; the last columns give policy-minus-HumT and policy-minus-marker broad-D recall differences in percentage points. Paired 95\\% intervals use 2,000 prompt draws with seed 20261102, so repeated contrasts differ slightly from original-seed tables. Fit/OA contrasts are in Table~\\ref{tab:semantic_fixed}. $\\dagger$: fewer than ten supporting prompts.}",
        "\\label{tab:semantic_compact}", "\\begin{tabular}{llrrrll}", "\\toprule",
        "Domain & Policy & $\\overline D\\geq3$ & $\\overline F<4$ & $\\overline{\\mathrm{OA}}<4$ & $\\Delta\\overline D$ vs HumT & $\\Delta\\overline D$ vs markers \\\\", "\\midrule",
    ]
    for d in DOM:
        r0 = counts[(counts.domain == d) & (counts.policy == "high_H")].iloc[0]
        for i, p in enumerate(pols):
            r = counts[(counts.domain == d) & (counts.policy == p)].iloc[0]
            def ctr(v):
                if p == v:
                    return "--"
                q = contrasts[(contrasts.domain == d) & (contrasts.policy == p) & (contrasts.versus == v) & (contrasts.criterion == "D>=3")]
                return iv(q.iloc[0]) if len(q) else "--"
            cells = []
            for c in ("D>=3", "F<4", "OA<4"):
                sparse = "$^{\\dagger}$" if (i == 0 and r0[f"G_{c}"] < 10) else ""
                cells.append(f"{r[f'caught_{c}']}/{r[f'P_{c}']}{sparse}")
            dom = DOM[d] if i == 0 else ""
            lines.append(f"{dom} & {short[p]} & {' & '.join(cells)} & {ctr('high_H')} & {ctr('markers')} \\\\")
        if d != "health":
            lines.append("\\addlinespace")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(lines)


def semantic_heldout(counts: pd.DataFrame, contrasts: pd.DataFrame, draws: int) -> str:
    lines = [
        "\\begin{table*}[t]", "\\centering\\scriptsize\\setlength{\\tabcolsep}{3.5pt}",
        f"\\caption{{Held-out lexical and semantic-feature screens (five prompt-group folds, per-fold 20\\% slots; 130/80/80 total). Counts are captured cases out of $P$. Lex uses marker fraction and log length; H adds HumT; Emb adds the 384-dimensional MiniLM vector; Emb16 uses 16 training-fitted components, added after inspecting full-dimensional performance. Differences have {draws:,}-draw refitted prompt-cluster 95\\% intervals. Table~\\ref{{tab:semantic_increments}} supplies every HumT increment for both embedding variants.}}",
        "\\label{tab:semantic_heldout}", "\\begin{tabular}{llrrrrrrrrlll}", "\\toprule",
        "Domain & Crit. & $P$ & Lex & +H & +Emb & +Emb+H & Emb & +Emb16 & +Emb16+H & Emb16$-$Lex & (Emb16+H)$-$Emb16 & H$-$Lex \\\\", "\\midrule",
    ]
    for d in DOM:
        for c in ("D>=3", "F<4", "OA<4"):
            r = counts[(counts.domain == d) & (counts.criterion == c)].iloc[0]
            def ctr(m, v):
                q = contrasts[(contrasts.domain == d) & (contrasts.criterion == c) & (contrasts.model == m) & (contrasts.versus == v)]
                return iv(q.iloc[0]) if len(q) else "--"
            dom = DOM[d] if c == "D>=3" else ""
            lines.append(
                f"{dom} & {CRIT[c]} & {r['P']} & {r['lex']} & {r['lex+H']} & {r['lex+emb']} & {r['lex+emb+H']} & {r['emb']} & {r['lex+emb16']} & {r['lex+emb16+H']} & "
                f"{ctr('lex+emb16','lex')} & {ctr('lex+emb16+H','lex+emb16')} & {ctr('lex+H','lex')} \\\\"
            )
        if d != "health":
            lines.append("\\addlinespace")
    lines += ["\\bottomrule", "\\end{tabular}", "\\end{table*}", ""]
    return "\n".join(lines)


def merged_heldout(out: Path) -> tuple[pd.DataFrame, pd.DataFrame] | None:
    """Merge per-domain shards (heldout_*_<domain>.csv) or read the unsharded files."""
    if (out / "heldout_counts.csv").exists():
        return pd.read_csv(out / "heldout_counts.csv"), pd.read_csv(out / "heldout_contrasts.csv")
    shards = [(out / f"heldout_counts_{d}.csv", out / f"heldout_contrasts_{d}.csv") for d in DOM]
    if not all(a.exists() and b.exists() for a, b in shards):
        return None
    counts = pd.concat([pd.read_csv(a) for a, _ in shards], ignore_index=True)
    contrasts = pd.concat([pd.read_csv(b) for _, b in shards], ignore_index=True)
    counts.to_csv(out / "heldout_counts.csv", index=False)
    contrasts.to_csv(out / "heldout_contrasts.csv", index=False)
    return counts, contrasts


def main(out_dir: str, tables_dir: str) -> None:
    out, tab = Path(out_dir), Path(tables_dir)
    counts = pd.read_csv(out / "fixed_policy_counts.csv")
    contrasts = pd.read_csv(out / "fixed_policy_contrasts.csv")
    (tab / "cue_ablation.tex").write_text(cue_ablation(counts, contrasts))
    (tab / "semantic_fixed.tex").write_text(semantic_fixed(counts, contrasts))
    (tab / "semantic_compact.tex").write_text(semantic_compact(counts, contrasts))
    held = merged_heldout(out)
    if held is not None:
        hc, hx = held
        draws = int(hx["finite"].max())
        (tab / "semantic_heldout.tex").write_text(semantic_heldout(hc, hx, draws))
    print("tables written to", tab)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
