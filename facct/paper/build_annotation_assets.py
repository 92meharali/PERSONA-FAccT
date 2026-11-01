"""Typeset the supplied assessment follow-up without changing its estimands."""
import csv
import json

from facct.paper.build_overleaf import DEST, ROOT, percentage, sha


SOURCE = ROOT / "facct/independent_annotation/outputs"


def records(name):
    with (SOURCE / name).open() as stream:
        return list(csv.DictReader(stream))


def build(table):
    manifest = json.loads((SOURCE / "manifest.json").read_text())
    for name, digest in manifest["output_hashes"].items():
        assert sha(SOURCE / name) == digest, f"Annotation output changed: {name}"
    metrics = records("policy_metrics.csv")
    intervals = records("bootstrap_intervals.csv")
    agreement = json.loads((SOURCE / "agreement.json").read_text())

    def point(target="resolved_ABC", policy="HumT", budget=.2):
        matches = [r for r in metrics if r["family"] == "original"
                   and r["target"] == target and r["policy"] == policy
                   and float(r["budget"]) == budget]
        assert len(matches) == 1
        row = matches[0]
        assert int(row["unresolved"]) == 0, "Update reporting if unresolved labels appear"
        assert float(row["selected"]) == int(int(row["n"]) * budget)
        return row

    def ci(target, quantity):
        matches = [r for r in intervals if r["target"] == target and r["quantity"] == quantity]
        assert len(matches) == 1
        row = matches[0]
        assert int(row["requested"]) >= 2000
        assert int(row["effective"]) == int(row["requested"]), "Report undefined draws explicitly"
        return "[" + percentage(row["lo"], True) + ", " + percentage(row["hi"], True) + "]"

    def count(value):
        return f"{float(value):g}"

    policies = [("HumT", "HumT"), ("markers_normalized", "Normalized markers"),
                ("length_words", "Word length"), ("random_expected", "Random (expected)")]
    rows = []
    for policy, title in policies:
        r = point(policy=policy)
        rows.append(" & ".join([title, f"{count(r['caught'])}/{r['positives']}",
                                percentage(r["recall"]), percentage(r["precision"]),
                                count(r["missed"])]) + r" \\")
    table("annotation_coverage", "lrrrr", r"Policy & Caught/$P$ & Recall & Precision & Missed", rows,
          r"Exploratory mental-health follow-up: original policies at 132/660 slots against contextual reviewworthiness ($P=19$, 13 supporting prompts), using resolved labels. Recall and precision are percentages. Counts condition on mixed-version judgments; random counts are expectations. Paired hypothetical-batch intervals are reported in the text, not inferred from the ordering.")

    targets = [("A", "R1 alone"), ("B", "R2 alone"), ("resolved_ABC", "Resolved"),
               ("AB_union", "R1/R2 union"), ("AB_intersection", "R1/R2 intersection"),
               ("A_severity3", "R1 rating 3"), ("B_severity3", "R2 rating 3")]
    rows = []
    for target, title in targets:
        h, m = point(target), point(target, "markers_normalized")
        delta = percentage(float(h["recall"]) - float(m["recall"]), True)
        interval = ci(target, "HumT_minus_markers") if target in ("A", "B", "resolved_ABC") else "--"
        rows.append(" & ".join([title, h["positives"], count(h["caught"]), count(m["caught"]),
                                delta, interval]) + r" \\")
    table("annotation_sensitivity", "lrrrrr", r"Target & $P$ & H caught & M caught & $\Delta R$ & 95\% interval", rows,
          r"Assessor and target sensitivity at the same 132 slots. $\Delta R$ is HumT minus normalized-marker recall in percentage points. Pointwise intervals use 2,000 paired prompt-cluster draws with re-ranking. Dashes mean intervals were not estimated, not zero uncertainty. Person and capability-note version are confounded; resolved judgments do not create a third full-corpus rating stream.")

    rows = []
    for budget in (.05, .1, .2, .3):
        h = point(budget=budget)
        rows.append(" & ".join([percentage(budget), count(h["selected"])] +
                               [count(point(policy=p, budget=budget)["caught"]) for p, _ in policies]) + r" \\")
    table("annotation_budgets", "rrrrrr", r"Budget (\%) & Slots & H caught & M caught & L caught & Random", rows,
          r"All four specified budgets under the resolved follow-up target ($P=19$). H, M and L denote HumT, normalized markers and word length. Random values are expected captured counts. The 20\% fraction was already explored, not selected to optimize these new judgments.")

    overlap = records("legacy_overlap.csv")
    labels = {"D>=3": r"$\overline D\geq3$", "F<4": r"$\overline F<4$", "OA<4": r"$\overline{\mathrm{OA}}<4$"}
    rows = []
    for key, label in labels.items():
        def cell(old, new):
            return next(r["n"] for r in overlap if r["legacy"] == key
                        and r["legacy_positive"] == str(old) and r["new_label"] == str(new))
        rows.append(" & ".join([label, cell(True, 1), cell(True, 0), cell(False, 1), cell(False, 0)]) + r" \\")
    table("annotation_overlap", "lrrrr", r"Legacy target & Both & Legacy only & Follow-up only & Neither", rows,
          r"Exact intersections in the 660-response mental-health batch. The new follow-up target is not merely a stricter numerical cutoff of the source ratings. Different criteria, populations and instructions prevent attributing disagreement to any one cause; neither label stream is treated as ground truth for harm.")

    h, m, random = point(), point(policy="markers_normalized"), point(policy="random_expected")
    macros = {
        "IAN": str(agreement["n"]), "IAPositive": h["positives"], "IAClusters": h["positive_clusters"],
        "IASlots": count(h["selected"]), "IAHCaught": count(h["caught"]), "IAMCaught": count(m["caught"]),
        "IAHMissed": count(h["missed"]), "IAMMissed": count(m["missed"]),
        "IAHRecall": percentage(h["recall"]) + r"\%", "IAMRecall": percentage(m["recall"]) + r"\%",
        "IAHDeltaMarkers": percentage(float(h["recall"]) - float(m["recall"]), True),
        "IAHDeltaRandom": percentage(float(h["recall"]) - float(random["recall"]), True),
        "IAHMarkersInterval": ci("resolved_ABC", "HumT_minus_markers"),
        "IAHRandomInterval": ci("resolved_ABC", "HumT_minus_random_expected"),
        "IAAgreement": percentage(agreement["raw_agreement"]) + r"\%",
        "IAKappa": f"{agreement['kappa']:.3f}",
        "IAPositiveAgreement": percentage(agreement["positive_agreement"]) + r"\%",
        "IABothYes": str(agreement["both_yes"]), "IABothNo": str(agreement["both_no"]),
        "IAOnlyFirst": str(agreement["A_yes_B_no"]), "IAOnlySecond": str(agreement["A_no_B_yes"]),
        "IADisputes": str(agreement["A_yes_B_no"] + agreement["A_no_B_yes"]),
        "IAInsideD": next(r["n"] for r in overlap if r["legacy"] == "D>=3"
                          and r["legacy_positive"] == "True" and r["new_label"] == "1"),
        "IAOutsideD": next(r["n"] for r in overlap if r["legacy"] == "D>=3"
                           and r["legacy_positive"] == "False" and r["new_label"] == "1"),
    }
    (DEST / "tables/annotation_numbers.tex").write_text(
        "% Generated from verified annotation outputs; do not edit values manually.\n" +
        "\n".join("\\newcommand{\\" + name + "}{" + value + "}" for name, value in macros.items()) + "\n")
