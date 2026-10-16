"""Assemble a portable review manuscript without altering frozen analyses."""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "facct/paper/overleaf"
DOMAINS = [("mental_health", "Mental health", "MH"),
           ("education", "Education", "ED"), ("health", "General health", "GH")]
LABELS = {"D_ge3": r"$\overline D\geq3$", "F_lt4": r"$\overline F<4$",
          "OA_lt4": r"$\overline{\mathrm{OA}}<4$"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def percentage(value, signed=False):
    return format(100 * float(value), "+.1f" if signed else ".1f")


def interval(row, field, signed=False):
    return f"[{percentage(row[field + '_lo'], signed)}, {percentage(row[field + '_hi'], signed)}]"


def table(name, spec, header, rows, caption):
    text = [r"\begin{table}[t]", r"\centering\small", r"\caption{" + caption + "}",
            r"\label{tab:" + name + "}", r"\begin{tabular}{" + spec + "}",
            r"\toprule", header + r" \\", r"\midrule", *rows, r"\bottomrule",
            r"\end{tabular}", r"\end{table}", ""]
    (DEST / f"tables/{name}.tex").write_text("\n".join(text))


def build_tables():
    source = ROOT / "facct/outputs/tables/screening.csv"
    with source.open() as stream:
        records = list(csv.DictReader(stream))
    def row(domain, criterion, policy="high_H"):
        matches = [r for r in records if r["domain"] == domain and r["criterion"] == criterion
                   and r["policy"] == policy and float(r["budget"]) == .2]
        assert len(matches) == 1, (domain, criterion, policy)
        return matches[0]
    coverage, baselines, workload, macros = [], [], [], []
    for domain, title, prefix in DOMAINS:
        for j, criterion in enumerate(LABELS):
            r = row(domain, criterion)
            assert int(float(r["selected"])) == int(int(r["n"]) * .2)
            coverage.append(" & ".join([
                title if not j else "", LABELS[criterion],
                f"{int(float(r['selected']))}/{r['n']}",
                f"{int(float(r['caught']))}/{r['concerns']}", percentage(r["precision"]),
                percentage(r["recall"]) + " " + interval(r, "recall"), str(int(float(r["missed"])))]) + r" \\")
        r = row(domain, "D_ge3")
        for suffix, value in {
            "Recall": percentage(r["recall"]) + r"\%",
            "Delta": percentage(r["delta_random"], True),
            "Adjusted": interval(r, "primary_adjusted_delta", True),
            "AP": f"{float(r['ap']):.3f}",
        }.items():
            macros.append("\\newcommand{\\" + prefix + suffix + "}{" + value + "}")
        for j, policy in enumerate(("length", "markers")):
            c = row(domain, "D_ge3", policy)
            baselines.append(" & ".join([
                title if not j else "", policy.capitalize(), f"{int(float(c['caught']))}/{c['concerns']}",
                percentage(c["recall"]), percentage(r["delta_" + policy], True) + " " + interval(r, "delta_" + policy, True)]) + r" \\")
        for j, policy in enumerate(("high_H", "length", "markers", "uniform_random")):
            w = row(domain, "D_ge3", policy)
            workload.append(" & ".join([title if not j else "",
                {"high_H": "HumT", "uniform_random": "Random (expected)"}.get(policy, policy.capitalize()),
                percentage(w["workload_80"]) + " " + interval(w, "workload_80")]) + r" \\")
    table("coverage", "llrrrrr", r"Domain & Criterion & Slots/$n$ & Caught/$P$ & Prec. & Recall [95\% CI] & Missed",
          coverage, r"High-H selection at 20\% capacity. Precision and recall are percentages. $P$ is the number of criterion cases. These are exploratory pointwise intervals, not simultaneous comparisons; education $D$ and general-health OA each have only seven concern-bearing prompts.")
    table("baselines", "llrrr", r"Domain & Comparator & Caught/$P$ & Recall & HumT minus comparator",
          baselines, r"Observable baselines at 20\% capacity for $\overline D\geq3$. Recall is a percentage; paired differences and their exploratory pointwise 95\% intervals are percentage points. Education is sparse.")
    table("workload", "llr", r"Domain & Policy & Batch percentage [95\% CI]",
          workload[:4], r"Mental-health workload for 80\% recall of $\overline D\geq3$. Random workload is an expected order statistic, not a guaranteed stopping point. Intervals are exploratory pointwise 95\%; paired differences are reported in the text.")
    table("workload_transfer", "llr", r"Domain & Policy & Batch percentage [95\% CI]",
          workload[4:], r"Education and general-health retrospective workload for 80\% recall of $\overline D\geq3$. Intervals are exploratory pointwise 95\%; education has only seven concern-bearing prompts.")
    (DEST / "tables/numbers.tex").write_text("% Generated from frozen screening.csv.\n" + "\n".join(macros) + "\n")


def build_revision_tables():
    folder=ROOT/"facct/revision/outputs"
    def records(name):
        with (folder/name).open() as stream:
            return list(csv.DictReader(stream))
    rel=records("source_reliability.csv")
    rows=[]
    for domain,title,_ in DOMAINS:
        for j,dim in enumerate(("D","F","OA","E")):
            r=next(r for r in rel if r["domain"]==domain and r["dimension"]==dim)
            fmt=lambda key:f"{float(r[key]):.3f}"
            rows.append(" & ".join([title if not j else "",dim,r["n_responses"],fmt("icc_ak"),fmt("icc_a1"),fmt("krippendorff_alpha_ordinal")])+r" \\")
    table("reliability","llrrrr",r"Domain & Construct & $n$ & ICC(A,5) & ICC(A,1) & Ordinal $\alpha$",rows,
          r"Source-study agreement estimates for all constructs. ICC point estimates were reconstructed from current ratings; ordinal alpha is reported from the source analysis. Average-rating reliability is not individual-rater agreement or validity of the review criterion.")
    cutoff=records("cutoff_diagnostics.csv")
    rows=[]
    for domain,title,_ in DOMAINS:
        for j,criterion in enumerate(LABELS):
            r=next(r for r in cutoff if r["domain"]==domain and r["criterion"]==criterion)
            rows.append(" & ".join([title if not j else "",LABELS[criterion],r["near_cutoff"],r["exactly_cutoff"],r["split_votes"],r["mean_majority_disagree"]])+r" \\")
    table("cutoffs","llrrrr",r"Domain & Criterion & $\pm0.2$ & At cutoff & Split & Disagree",rows,
          r"Descriptive cutoff diagnostics. Split means 1--4 of five raters individually meet the criterion; disagree means mean-based and majority-vote membership differ. The neighborhood width was specified before this post-review analysis, not chosen for favorable results.")
    comp=records("complementarity.csv")
    pairs=records("paired_comparisons.csv")
    rows=[]
    for domain,title,_ in DOMAINS:
        for j,criterion in enumerate(LABELS):
            r=next(r for r in comp if r["domain"]==domain and r["criterion"]==criterion and float(r["budget"])==.2)
            p=next(p for p in pairs if p["domain"]==domain and p["criterion"]==criterion and p["metric"]=="fusion_minus_markers_recall")
            ci=f"{percentage(p['estimate'],True)} [{percentage(p['lo'],True)}, {percentage(p['hi'],True)}]"
            rows.append(" & ".join([title if not j else "",LABELS[criterion],r["caught_h_only"],r["caught_markers_only"],r["caught_both"],r["caught_fusion"]+"/"+r["concerns"],ci])+r" \\")
    table("complementarity","llrrrrr",r"Domain & Criterion & H only & M only & Both & Fusion/$P$ & $\Delta R$ [95\%]",rows,
          r"Post-review exploratory complementarity at the original 20\% budget. H-only/marker-only/both are concern counts in the two selected sets; their union exceeds the budget and is not a policy. Fusion is an exact-budget equal-weight midrank policy. Differences are recall percentage points with exploratory pointwise 95\% intervals; education $D$ and general-health OA remain sparse.")
    rows=[]
    for domain,title,_ in DOMAINS:
        for j,criterion in enumerate(LABELS):
            r=next(r for r in records("operating_context.csv") if r["domain"]==domain and r["criterion"]==criterion and r["policy"]=="high_H" and float(r["budget"])==.2)
            rows.append(" & ".join([title if not j else "",LABELS[criterion],percentage(r["recall"]),percentage(r["oracle_recall"]),percentage(r["fraction_of_oracle"]),f"{float(r['lift']):.2f}"])+r" \\")
    table("oracle_context","llrrrr",r"Domain & Criterion & Recall & Oracle recall & Fraction of oracle & Lift",rows,
          r"Descriptive capacity context for high-H at 20\%. Recall and oracle quantities are percentages; lift is precision divided by prevalence. Oracle is an unavailable-label upper bound, not an implementable policy.")
    macros=[]
    for domain,_,prefix in DOMAINS:
        for metric,suffix in [("H_minus_random_workload80","WorkRandom"),("H_minus_length_workload80","WorkLength"),("H_minus_markers_workload80","WorkMarkers"),("fusion_minus_markers_recall","FusionDelta")]:
            r=next(r for r in pairs if r["domain"]==domain and r["criterion"]=="D_ge3" and r["metric"]==metric)
            value=f"{percentage(r['estimate'],True)} [{percentage(r['lo'],True)}, {percentage(r['hi'],True)}]"
            macros.append("\\newcommand{\\"+prefix+suffix+"}{"+value+"}")
    with (DEST/"tables/numbers.tex").open("a") as stream:
        stream.write("\n% Post-review exploratory paired estimates, percentage points.\n"+"\n".join(macros)+"\n")


def build_conditional_tables():
    def read(path):
        with (ROOT / path).open() as stream:
            return list(csv.DictReader(stream))

    folder = "facct/conditional/outputs/"
    performance = read(folder + "performance.csv")
    comparisons = read(folder + "conditional_lift.csv")
    splits = read(folder + "split_sensitivity.csv")
    original = read("facct/outputs/tables/screening.csv")
    fusion = read("facct/revision/outputs/complementarity.csv")
    pairs = read("facct/revision/outputs/paired_comparisons.csv")
    names = {"high_H": "HumT", "length": "Length", "markers": "Markers",
             "rank_fusion": "Rank fusion", "reduced_lr": "LR: markers + length",
             "extended_lr": "LR: + HumT", "uniform_random": "Random (expected)"}
    rows, split_rows, macros = [], [], []
    for domain, title, prefix in DOMAINS:
        for j, criterion in enumerate(LABELS):
            r = next(r for r in comparisons if r["domain"] == domain and
                     r["criterion"] == criterion and float(r["budget"]) == .2)
            value = (f"{percentage(r['conditional_lift'], True)} "
                     f"[{percentage(r['lo'], True)}, {percentage(r['hi'], True)}]")
            flag = r"$^{\dagger}$" if r["sparse"] == "True" else ""
            rows.append(" & ".join([title if not j else "", LABELS[criterion] + flag,
                f"{int(float(r['reduced_caught']))}/{r['concerns']}",
                f"{int(float(r['extended_caught']))}/{r['concerns']}", value]) + r" \\")
            suffix = {"D_ge3": "D", "F_lt4": "F", "OA_lt4": "OA"}[criterion]
            macros.append("\\newcommand{\\" + prefix + suffix + "Conditional}{" + value + "}")
            s = [s for s in splits if s["domain"] == domain and s["criterion"] == criterion]
            values = [float(s["conditional_lift"]) for s in s]
            split_rows.append(" & ".join([title if not j else "", LABELS[criterion] + flag,
                str(r["concern_clusters"]), r["valid_replicates"],
                f"[{percentage(min(values), True)}, {percentage(max(values), True)}]"]) + r" \\")

        full_rows, held_rows = [], []
        for criterion in LABELS:
            for j, policy in enumerate(("high_H", "length", "markers", "rank_fusion", "uniform_random")):
                if policy == "rank_fusion":
                    c = next(c for c in fusion if c["domain"] == domain and
                             c["criterion"] == criterion and float(c["budget"]) == .2)
                    p = next(p for p in pairs if p["domain"] == domain and
                             p["criterion"] == criterion and p["metric"] == "fusion_recall")
                    reference = next(r for r in original if r["domain"] == domain and
                        r["criterion"] == criterion and r["policy"] == "high_H" and float(r["budget"]) == .2)
                    caught, concerns = float(c["caught_fusion"]), int(c["concerns"])
                    precision = caught / float(reference["selected"])
                    recall = f"{percentage(p['estimate'])} [{percentage(p['lo'])}, {percentage(p['hi'])}]"
                    missed = concerns - caught
                else:
                    r = next(r for r in original if r["domain"] == domain and
                        r["criterion"] == criterion and r["policy"] == policy and float(r["budget"]) == .2)
                    caught, concerns = float(r["caught"]), int(r["concerns"])
                    precision, missed = float(r["precision"]), float(r["missed"])
                    recall = percentage(r["recall"]) + " " + interval(r, "recall")
                full_rows.append(" & ".join([LABELS[criterion] if not j else "", names[policy],
                    f"{caught:g}/{concerns}", percentage(precision), recall, f"{missed:g}"]) + r" \\")
            for j, policy in enumerate(names):
                r = next(r for r in performance if r["domain"] == domain and
                         r["criterion"] == criterion and r["policy"] == policy and float(r["budget"]) == .2)
                held_rows.append(" & ".join([LABELS[criterion] if not j else "", names[policy],
                    f"{float(r['caught']):.2f}/{r['concerns']}" if policy == "uniform_random" else f"{int(float(r['caught']))}/{r['concerns']}",
                    percentage(r["precision"]), percentage(r["recall"]) + " " + interval(r, "recall"),
                    f"{float(r['missed']):.2f}" if policy == "uniform_random" else str(int(float(r["missed"])))]) + r" \\")
        slots = 132 if domain == "mental_health" else 83
        held_slots = 130 if domain == "mental_health" else 80
        caption = (title + r": all full-batch policies and criteria at 20\% (" + str(slots) +
                   r" slots). Precision and recall are percentages; $P$ denotes cases. Intervals are exploratory pointwise 95\%; random counts are analytical expectations. Fusion is the first post-review addition. Education $D$ and general-health OA are sparse.")
        header = r"Criterion & Policy & Caught/$P$ & Prec. & Recall [95\% CI] & Missed"
        table("full_" + domain, "llrrrr", header, full_rows, caption)
        table("held_" + domain, "llrrrr", header, held_rows,
              title + r": every policy in the same five held-out batches, with " + str(held_slots) +
              r" total slots at the 20\% reference fraction. LR models use training labels; other rules are label-free. Precision and recall are percentages. Intervals are exploratory pointwise 95\% from paired refits, conditional on the fixed partition; sparse cells remain descriptive. Random counts are expectations. Do not compare these directly with the different full-batch capacities.")
    table("conditional", "llrrr", r"Domain & Criterion & Reduced/$P$ & + HumT/$P$ & $\Delta$ recall [95\% CI]", rows,
          r"Conditional lift from adding HumT to logistic regression on markers and log-length. Counts and paired recall differences (percentage points) use common held-out batches: 130/660 mental-health slots, 80/415 in each other domain. All nine intervals include zero. Intervals are exploratory pointwise, not simultaneous; $\dagger$ denotes fewer than ten concern-bearing prompt clusters.")
    table("split_sensitivity", "llrrr", r"Domain & Criterion & Positive prompts & Finite draws & Split range, pp", split_rows,
          r"Conditional-lift sensitivity across ten additional pre-specified prompt partitions. Ranges are descriptive, not confidence intervals or independent replication. Finite draws count defined paired differences in the original-partition 2,000-draw bootstrap; $\dagger$ marks sparse cells. All seed-level results are retained, not just a favorable partition.")
    with (DEST / "tables/numbers.tex").open("a") as stream:
        stream.write("\n% Held-out incremental recall, percentage points.\n" + "\n".join(macros) + "\n")


def validate():
    main = (DEST / "main.tex").read_text()
    tex = "\n".join(p.read_text() for p in [DEST / "main.tex", *sorted((DEST / "tables").glob("*.tex"))])
    bib = (DEST / "references.bib").read_text()
    keys = re.findall(r"@\w+\{([^,]+),", bib)
    assert len(keys) == len(set(keys)), "Duplicate citation keys"
    cited = {key.strip() for group in re.findall(r"\\cite\w*\{([^}]+)\}", tex) for key in group.split(",")}
    assert cited <= set(keys), f"Missing citations: {cited - set(keys)}"
    labels = re.findall(r"\\label\{([^}]+)\}", tex)
    assert len(labels) == len(set(labels)), "Duplicate labels"
    assert set(re.findall(r"\\ref\{([^}]+)\}", tex)) <= set(labels), "Unresolved references"
    for path in re.findall(r"\\input\{([^}]+)\}", main):
        assert (DEST / (path + ".tex")).exists(), path
    for path in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", main):
        assert (DEST / path).is_file(), path
    assert r"\documentclass[manuscript,screen,review,anonymous]{acmart}" in main
    for term in ["/Users/", "92meharali", "Ghaznavi", "Qadir", "TODO", "TBD"]:
        assert term not in tex, f"Private identifier or placeholder: {term}"
    # Check nesting after excluding escaped braces, comments, and verbatim tokens.
    cleaned = re.sub(r"\\verb\|[^|]*\|", "", tex)
    cleaned = re.sub(r"(?<!\\)%[^\n]*", "", cleaned)
    cleaned = re.sub(r"\\[{}]", "", cleaned)
    depth = 0
    for char in cleaned:
        depth += (char == "{") - (char == "}")
        assert depth >= 0, "Unbalanced closing brace"
    assert depth == 0, "Unbalanced opening brace"
    return {"citation_keys": len(keys), "cited_references": len(cited),
            "static_checks": "passed", "compilation": "unverified: no local multi-file TeX compiler",
            "page_count": "unverified; check in Overleaf"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class-source", type=Path, help="Unmodified upstream v2.19 acmart.dtx")
    args = parser.parse_args()
    for name in ("tables", "figures", "template-source"):
        (DEST / name).mkdir(parents=True, exist_ok=True)
    build_tables()
    build_revision_tables()
    build_conditional_tables()
    from facct.paper.build_allocation_assets import build as build_allocation
    build_allocation(table)
    from facct.paper.build_annotation_assets import build as build_annotation
    build_annotation(table)
    from facct.consolidation.audit import main as audit_provenance
    audit_provenance()
    for name in ("provenance_composition.tex", "provenance_truncation.tex"):
        shutil.copyfile(ROOT / "facct/consolidation/outputs" / name, DEST / "tables" / name)
    for name in ("acmart.cls", "ACM-Reference-Format.bst"):
        shutil.copyfile(ROOT / "paper" / name, DEST / name)
    if args.class_source:
        assert "v2.19" in args.class_source.read_text(), "Unexpected upstream source version"
        shutil.copyfile(args.class_source, DEST / "template-source/acmart.dtx")
    assert (DEST / "template-source/acmart.dtx").exists(), "Supply --class-source on first build"
    memo = (ROOT / "facct/submission/overleaf_reference_check.md").read_text()
    additional = re.findall(r"```bibtex\n(.*?)\n```", memo, flags=re.S)[:4]
    assert len(additional) == 4
    revision_memo=(ROOT/"facct/submission/revision_literature_check.md").read_text()
    additional += re.findall(r"```bibtex\n(.*?)\n```", revision_memo, flags=re.S)
    (DEST / "references.bib").write_text((ROOT / "facct/paper/references.bib").read_text() + "\n" + "\n\n".join(additional) + "\n")
    # Retain the original nine-panel asset in the ZIP for source history;
    # the manuscript uses larger panels generated from the same frozen values.
    shutil.copyfile(ROOT / "facct/outputs/figures/recall_budgets.pdf", DEST / "figures/recall_budgets.pdf")
    for name in ("mental_health_budgets.pdf","transfer_budgets.pdf","d_mean_distributions.pdf"):
        shutil.copyfile(ROOT/"facct/revision/outputs"/name,DEST/"figures"/name)
    checks = validate()
    files = sorted(p for p in DEST.rglob("*") if p.is_file() and p.name != "package_manifest.json")
    manifest = {"format_checked": "2026-10-02", "acmart_version": "2.19 (2026-06-27), unmodified repository template",
                "template_source": "https://github.com/borisveytsman/acmart/blob/v2.19/acmart.dtx",
                "author_guide": "https://facctconference.org/2027/authorguide.html", "checks": checks,
                "analysis_manifest_sha256": sha(ROOT / "facct/outputs/manifest.json"),
                "screening_table_sha256": sha(ROOT / "facct/outputs/tables/screening.csv"),
                "revision_manifest_sha256": sha(ROOT/"facct/revision/outputs/manifest.json"),
                "conditional_manifest_sha256": sha(ROOT/"facct/conditional/outputs/manifest.json"),
                "allocation_manifest_sha256": sha(ROOT/"facct/allocation/outputs/manifest.json"),
                "consolidation_manifest_sha256": sha(ROOT/"facct/consolidation/outputs/manifest.json"),
                "annotation_manifest_sha256": sha(ROOT/"facct/independent_annotation/outputs/manifest.json"),
                "files": {str(p.relative_to(DEST)): sha(p) for p in files}}
    (DEST / "package_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    release = ROOT / "facct/releases/PERSONA_FAccT_2027_Overleaf.zip"
    release.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(release, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DEST.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(str(path.relative_to(DEST)), date_time=(2026, 10, 2, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(release) as archive:
        assert archive.testzip() is None
    print(json.dumps({"zip": str(release), "bytes": release.stat().st_size, **checks}, indent=2))


if __name__ == "__main__":
    main()
