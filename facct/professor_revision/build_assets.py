"""Generate the new manuscript tables directly from immutable revision outputs."""
import json

import pandas as pd

from facct.analysis.validate_inputs import sha
from facct.professor_revision.run import OUT, ROOT


def main():
    manifest = json.loads((OUT / "manifest.json").read_text())
    for name, digest in manifest["output_hashes"].items():
        assert sha(OUT / name) == digest, f"Changed output: {name}"
    p = pd.read_csv(OUT / "performance.csv")
    c = pd.read_csv(OUT / "paired_contrasts.csv")
    labels = {"D_ge3": r"$\overline D\geq3$", "D_gt3": r"$\overline D>3$",
              "D_ge4": r"$\overline D\geq4$", "F_lt4": r"$\overline F<4$",
              "OA_lt4": r"$\overline{\mathrm{OA}}<4$", "followup": "Follow-up"}
    domains = {"mental_health": "Mental health", "education": "Education", "health": "General health"}
    rows = [r"\begin{table}[t]", r"\centering\small",
            r"\caption{Input-window and threshold sensitivity at 20\% capacity. Counts are selected concerns; $P/G$ are concerns/supporting prompts. Full and 300-character markers use the same dictionary and token normalization. Last column: HumT minus 300-character-marker recall in percentage points with paired exploratory 95\% intervals. Sparse cells and zero-positive draws are retained in the computational record.}",
            r"\label{tab:prefix_threshold}", r"\begin{tabular}{llrrrrl}", r"\toprule",
            r"Domain & Target & $P/G$ & HumT & Full M & 300 M & $\Delta R$ [95\%] \\", r"\midrule"]
    for (domain, target), g in p[p.budget == .2].groupby(["domain", "criterion"], sort=False):
        lookup = g.set_index("policy")
        contrast = c[(c.domain == domain) & (c.criterion == target) & (c.budget == .2)
                     & (c.policy_a == "HumT") & (c.policy_b == "markers_300")].iloc[0]
        base = g.iloc[0]
        vals = [domains[domain], labels[target], f"{base.concerns}/{base.concern_clusters}"]
        vals += [str(int(lookup.loc[v, "caught"])) for v in ("HumT", "markers_full", "markers_300")]
        vals += [f"{100*contrast.recall_difference:+.1f} [{100*contrast.lo:+.1f}, {100*contrast.hi:+.1f}]"]
        rows.append(" & ".join(vals) + r" \\")
    rows += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    destination = ROOT / "facct/paper/overleaf/tables"
    (destination / "prefix_threshold.tex").write_text("\n".join(rows) + "\n")
    cases = pd.read_csv(OUT / "exclusive_case_summary.csv").set_index("policy_only")
    rows = [r"\begin{table}[t]", r"\centering\small",
            r"\caption{All broad-$D$ cases unique to one original mental-health queue at 132 slots. Counts reuse source judgments and follow-up labels; they are not a new semantic adjudication. The 22 cases selected by both queues are excluded from this descriptive contrast.}",
            r"\label{tab:exclusive_profiles}", r"\begin{tabular}{lrr}", r"\toprule",
            r"Characteristic & HumT only ($n=20$) & Markers only ($n=41$) \\", r"\midrule"]
    for field, label in [("D_eq3", r"Mean $D=3$"), ("D_gt3", r"Mean $D>3$"),
                         ("D_ge4", r"Mean $D\geq4$"), ("F_lt4", r"Mean $F<4$"),
                         ("OA_lt4", r"Mean OA $<4$"), ("followup", "Follow-up concern"),
                         ("natural", "Natural-prompt cases"), ("clusters", "Supporting prompts")]:
        rows.append(label + " & " + " & ".join(str(int(cases.loc[v, field])) for v in ("HumT", "markers_full")) + r" \\")
    rows += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    (destination / "exclusive_profiles.tex").write_text("\n".join(rows) + "\n")
    asset_hashes = {name: sha(destination / name) for name in ("prefix_threshold.tex", "exclusive_profiles.tex")}
    (OUT / "asset_manifest.json").write_text(json.dumps({"analysis_manifest_sha256": sha(OUT / "manifest.json"), "files": asset_hashes}, indent=2) + "\n")


if __name__ == "__main__":
    main()
