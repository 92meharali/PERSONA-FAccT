"""Build the computational review draft directly from frozen analysis outputs."""
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DOMAINS = ("mental_health", "education", "health")
NAMES = dict(mental_health="Mental health", education="Education", health="General health")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"] + ["| " + " | ".join(map(str,row)) + " |" for row in rows])


def pct(value):
    return f"{100*value:.1f}%"


def interval(value, lo, hi):
    return f"{pct(value)} [{100*lo:.1f}, {100*hi:.1f}]"


def build(root=ROOT, output=None):
    output = output or root / "facct/paper/generated"
    output.mkdir(parents=True, exist_ok=True)
    sources = root / "facct/outputs/tables"
    names = ("screening.csv", "input_counts.csv", "threshold_sensitivity.csv", "join_sensitivity.csv")
    paths = [sources/n for n in names] + [root/"facct/paper/computational_draft.template.md", root/"facct/outputs/manifest.json", root/"facct/submission/provenance_resolution.md", root/"facct/submission/distinctness_assessment.md"]
    hashes = {str(p.relative_to(root)): sha(p) for p in paths}
    screen, counts, thresholds, joins = [pd.read_csv(sources/n) for n in names]
    base = screen[(screen.budget==.2)&(screen.domain!="pooled")]
    coverage, comparisons, primary, stronger, workload = [], [], [], [], []
    for domain in DOMAINS:
        for criterion in ("D_ge3", "F_lt4", "OA_lt4"):
            r = base[(base.domain==domain)&(base.criterion==criterion)&(base.policy=="high_H")].iloc[0]
            coverage.append([NAMES[domain],criterion,f"{int(r.selected)}/{int(r.n)}",f"{int(r.caught)}/{int(r.concerns)}",pct(r.precision),interval(r.recall,r.recall_lo,r.recall_hi),int(r.missed)])
        g = base[(base.domain==domain)&(base.criterion=="D_ge3")].set_index("policy")
        r = g.loc["high_H"]
        primary.append(f"- {NAMES[domain]}: HumT minus random recall {100*r.delta_random:+.1f} percentage points; adjusted interval [{100*r.primary_adjusted_delta_lo:+.1f}, {100*r.primary_adjusted_delta_hi:+.1f}]. Supporting concern-bearing prompts: {int(r.concern_clusters)}.")
        for p,field in (("length","delta_length"),("markers","delta_markers")):
            b=g.loc[p]
            comparisons.append([NAMES[domain],p,f"{int(b.caught)}/{int(b.concerns)}",pct(b.recall),f"{100*r[field]:+.1f} [{100*r[field+'_lo']:+.1f}, {100*r[field+'_hi']:+.1f}]"])
        t=thresholds[(thresholds.domain==domain)&(thresholds.criterion=="D>=4")&(thresholds.policy=="high_H")].iloc[0]
        j=joins[(joins.domain==domain)&(joins.criterion=="D_ge3")&(joins.policy=="high_H")].iloc[0]
        stronger.append(f"- {NAMES[domain]}: at mean D >= 4, high-H selection captures {int(t.caught)}/{int(t.concerns)} cases from {int(t.concern_clusters)} concern-bearing prompts. For the full-text/embedded-only D >= 3 sensitivity, {int(j.excluded)} rows are excluded and {int(j.caught)}/{int(j.concerns)} cases are selected.")
        for p in ("high_H","length","markers","uniform_random"):
            r=g.loc[p]
            workload.append([NAMES[domain],p,interval(r.workload_80,r.workload_80_lo,r.workload_80_hi)])
    blocks = {
        "CORPUS": f"The released corpus contains {counts.responses.sum():,} responses in {counts.prompts.sum():,} domain-scoped prompt clusters.\n\n" + table(["Domain","Responses","Prompt clusters"],[[NAMES[r.domain],r.responses,r.prompts] for r in counts.itertuples()]),
        "COVERAGE":table(["Domain","Criterion","Review slots / batch","Cases selected / concern cases","Precision","Recall (95% CI)","Unreviewed concerns"],coverage),
        "PRIMARY":"For the specified D >= 3 primary comparison family, the adjusted 98.3333% intervals are:\n\n"+"\n".join(primary)+"\n\nThe general-health adjusted lower endpoint is very close to zero; the percentile interval and its finite Monte Carlo resolution should not be presented as a decisive threshold-independent finding.",
        "BASELINES":table(["Domain","Comparator","Cases selected / D cases","Comparator recall","HumT minus comparator recall, pp (95% CI)"],comparisons),
        "SENSITIVITY":"\n".join(stronger),
        "WORKLOAD":table(["Domain","Policy","Batch fraction needed for 80% D-case recall (95% CI)"],workload),
    }
    text=(root/"facct/paper/computational_draft.template.md").read_text()
    for name,block in blocks.items():
        assert text.count("{{"+name+"}}") == 1
        text=text.replace("{{"+name+"}}",block)
    assert not re.search(r"\{\{[A-Z_]+\}\}",text)
    (output/"computational_review_draft.md").write_text(text)
    for name in ("CORPUS","COVERAGE","BASELINES","WORKLOAD"):
        (output/f"{name.lower()}.md").write_text(blocks[name]+"\n")
    assert hashes == {str(p.relative_to(root)):sha(p) for p in paths}
    manifest={"status":"internal computational review draft; not submission-ready", "source_hashes":hashes,"generator_sha256":sha(Path(__file__)),"output_hashes":{p.name:sha(p) for p in sorted(output.glob("*.md"))}}
    (output/"review_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest


if __name__=="__main__":
    result=build()
    print(f"Built {len(result['output_hashes'])} documents from verified outputs; sources unchanged.")
