"""Generate manuscript tables directly from the verified transfer outputs."""
import json
from pathlib import Path

import pandas as pd

from facct.analysis.validate_inputs import sha
from .run import HERE, ROOT, TRAIN, MODELS

DEST = ROOT / "facct/paper/overleaf"
DOMAIN_NAMES = {"mental_health": "Mental health", "education": "Education", "health": "General health"}
NAMES = {"D_ge3": "$D$", "F_lt4": "$F$", "OA_lt4": "OA", "contextual_reviewworthiness": "Reviewworthiness"}


def table(name, columns, header, rows, caption, label):
    text = "\n".join([r"\begin{table}[htbp]", r"\centering\small", r"\caption{"+caption+"}",
        r"\label{"+label+"}", r"\begin{tabular}{"+columns+"}", r"\toprule",
        " & ".join(header)+r" \\", r"\midrule", *[" & ".join(row)+r" \\" for row in rows],
        r"\bottomrule", r"\end{tabular}", r"\end{table}", ""])
    (DEST/"tables"/name).write_text(text)


def build():
    out = HERE/"outputs"
    manifest = json.loads((out/"manifest.json").read_text())
    assert manifest["status"] == "final" and manifest["config"]["replicates"] >= 2000
    for name, digest in manifest["outputs"].items():
        assert sha(out/name) == digest, name
    p = pd.read_csv(out/"performance.csv")
    c = pd.read_csv(out/"contrasts.csv")
    p, c = p[p.budget==.2], c[c.budget==.2]
    rows = []
    for domain, title in DOMAIN_NAMES.items():
        for t in TRAIN:
            d = p[(p.domain==domain)&(p.model==MODELS[0])&(p.train_target==t)].set_index("evaluation_target")
            cells = [f"{int(d.loc[e,'caught'])}/{int(d.loc[e,'concerns'])}" if e in d.index else "--"
                     for e in (*TRAIN, "contextual_reviewworthiness")]
            rows.append([title if t==TRAIN[0] else "", NAMES[t], *cells])
    table("criterion_transfer_counts.tex", "llrrrr",
        ["Domain", "Train target", "$D$ cases", "$F$ cases", "OA cases", "Reviewworthy"], rows,
        "Changing the training target with learner, lexical features and held-out batches fixed. Cells are captured/total assessment cases, not predictive $R^2$. All queues use 130 mental-health or 80 transfer-domain slots at the 20\\% reference fraction. Reviewworthiness is an evaluation-only mental-health target. These exploratory counts do not establish an optimal target; paired uncertainty is reported in the text and Appendix~\\ref{app:criteriontransfer}.", "tab:criteriontransfer")
    files = ["tables/criterion_transfer_counts.tex"]
    for domain, title in DOMAIN_NAMES.items():
        rows = []
        for model in MODELS:
            d = p[(p.domain==domain)&(p.model==model)]
            for endpoint in dict.fromkeys(d.evaluation_target):
                cells=[]
                for t in TRAIN:
                    r=d[(d.train_target==t)&(d.evaluation_target==endpoint)].iloc[0]
                    cells.append(f"{100*r.recall:.1f} [{100*r.recall_lo:.1f}, {100*r.recall_hi:.1f}]")
                rows.append(["Lexical" if model==MODELS[0] else "Lexical+$H$", NAMES[endpoint], *cells])
        name=f"criterion_transfer_{domain}.tex"
        table(name, "llrrr", ["Features", "Assess against", "Train $D$", "Train $F$", "Train OA"], rows,
            title+": all training-target by assessment-target recall percentages and exploratory pointwise 95\\% refitted prompt-bootstrap intervals at the 20\\% reference fraction. Feature sets share the same learner and folds. Each column is a different learned queue, not a different assessment of one queue. Sparse target support and finite-replicate counts are described in the appendix.", "tab:transfer"+domain.replace("_", ""))
        files.append("tables/"+name)
    rows=[]
    for r in c[(c.left_target=="F_lt4")&(c.right_target=="OA_lt4")].itertuples():
        rows.append([DOMAIN_NAMES[r.domain], "Lexical" if r.model==MODELS[0] else "+$H$", NAMES[r.evaluation_target],
            f"{100*r.recall_difference:+.1f} [{100*r.lo:+.1f}, {100*r.hi:+.1f}]", str(r.valid_replicates)])
    table("criterion_transfer_contrasts.tex", "lllrr", ["Domain", "Features", "Assess against", "$F$ minus OA (pp)", "Draws"], rows,
        "All fit-trained minus OA-trained recall contrasts at 20\\%. Positive values favor the fit-trained queue. These pointwise paired 95\\% intervals are exploratory, not a multiplicity-adjusted primary family. All other training-target pairs remain in the machine-readable analysis record.", "tab:transfercontrasts")
    files.append("tables/criterion_transfer_contrasts.tex")
    legacy = pd.read_csv(ROOT/"analysis/outputs/tables/incremental_validity.csv")
    rows=[]
    for domain, title in DOMAIN_NAMES.items():
        r=legacy[(legacy.domain==domain)&(legacy.comparison=="H+E+D+F vs F_only")].iloc[0]
        rows.append([title, f"{r.cv_r2_baseline:.3f}", f"{r.cv_r2_model:.3f}",
            f"{r.delta_cv_r2:+.3f} [{r.delta_ci_low:+.3f}, {r.delta_ci_high:+.3f}]"])
    table("measurement_bridge.tex", "lrrr", ["Domain", "$F$ only $R^2$", "Full profile $R^2$", "Increment [95\\%]"], rows,
        "Earlier OA-prediction diagnostic, reproduced from recorded outputs rather than refitted here. Predictors include already-acquired human ratings; this is not a cheap deployable review screen. OLS uses five prompt-group folds over 20 repeats, with 1,000 prompt-bootstrap draws over averaged held-out predictions, not bootstrap model refits. The full profile uses $H,E,D,F$. Small increments do not establish construct equivalence or independent framework validation.", "tab:measurementbridge")
    files.append("tables/measurement_bridge.tex")
    baseline = pd.read_csv(out/"baselines.csv")
    baseline = baseline[(baseline.budget==.2)&(baseline.evaluation_target=="contextual_reviewworthiness")]
    rows=[]
    for r in baseline.itertuples():
        rows.append([{"high_H":"HumT", "length":"Length", "markers":"Markers", "uniform_random":"Random (expected)"}[r.policy],
            f"{r.caught:.2f}" if r.policy=="uniform_random" else str(int(r.caught)),
            f"{100*r.recall:.1f}", f"{100*r.precision:.1f}"])
    table("criterion_transfer_baselines.tex", "lrrr", ["Policy", "Caught / 19", "Recall (\\%)", "Precision (\\%)"], rows,
        "Fixed baselines assessed against contextual reviewworthiness in exactly the same held-out mental-health batches (130 slots) as criterion transfer. Counts are descriptive; other fixed-policy interval families using 132 slots must not be attached to these values. Original-target held-out baselines already appear in Tables~\\ref{tab:held_mental_health}--\\ref{tab:held_health}.", "tab:transferbaselines")
    files.append("tables/criterion_transfer_baselines.tex")
    result = dict(analysis_manifest_sha256=sha(out/"manifest.json"),
        legacy_incremental_sha256=sha(ROOT/"analysis/outputs/tables/incremental_validity.csv"),
        files={name:sha(DEST/name) for name in files})
    (out/"paper_assets.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    build()
