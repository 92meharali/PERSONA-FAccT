"""Reconstruct existing provenance sensitivity without changing any old output."""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

from analysis.build_dataset import humt_file
from facct.analysis.screening import capacity, features, labels, tie_keys
from facct.analysis.validate_inputs import sha, source_hashes
from facct.revision.run import POLICIES, policy_orders

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "facct/consolidation/outputs"


def protected_hashes(root=ROOT):
    result = source_hashes(root)
    for directory in ("facct/analysis", "facct/tests", "facct/protocol", "facct/outputs",
                      "facct/revision", "facct/conditional", "facct/allocation"):
        for path in (root / directory).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                result[str(path.relative_to(root))] = sha(path)
    return result


def equality_mask(frame, provenance):
    """Require one provenance row per item; never equate tier with text equality."""
    if provenance.id.duplicated().any():
        raise ValueError("Duplicate provenance ID")
    joined = frame[["id"]].merge(provenance, on="id", how="left", validate="one_to_one")
    if joined.comparison.isna().any():
        raise ValueError("Missing provenance item")
    return joined.comparison.eq("raw_equal").to_numpy()


def composition(frame, config):
    rows = []
    for domain, domain_frame in frame.groupby("domain", sort=True):
        for batch_name in ("full", "byte_identical", "different_text", "embedded_only"):
            if batch_name == "full":
                batch = domain_frame
            else:
                batch = domain_frame[domain_frame.text_status == batch_name]
            if batch.empty:
                continue
            partitions = [("all", "all", batch)]
            for category in ("condition", "model", "scenario_type"):
                partitions.extend((category, str(value), group)
                                  for value, group in batch.groupby(category, sort=True))
            for category, value, group in partitions:
                Y = labels(group, config)
                for j, criterion in enumerate(config["criteria"]):
                    positive = Y[:, j]
                    rows.append(dict(domain=domain, batch=batch_name, category=category,
                        value=value, criterion=criterion, n=len(group),
                        prompts=group.cluster.nunique(), concerns=int(positive.sum()),
                        concern_prompts=group.loc[positive, "cluster"].nunique(),
                        prevalence=float(positive.mean())))
    return pd.DataFrame(rows)


def subset_points(frame, config):
    rows = []
    for domain in ("education", "health"):
        full = frame[frame.domain == domain]
        batch = full[full.text_status == "byte_identical"]
        X, Y = features(batch), labels(batch, config)
        orders, _ = policy_orders(X, tie_keys(batch.id, config["seed"]))
        for mode, k in (("same_capacity", capacity(len(full), .2)),
                        ("same_fraction", capacity(len(batch), .2))):
            for j, criterion in enumerate(config["criteria"]):
                p = int(Y[:, j].sum())
                for i, policy in enumerate(POLICIES):
                    caught = int(Y[orders[i][:k], j].sum())
                    rows.append(dict(domain=domain, mode=mode, criterion=criterion,
                        policy=policy, n=len(batch), selected=k, concerns=p, caught=caught,
                        missed=p-caught, recall=caught/p if p else np.nan,
                        random_expected_caught=k*p/len(batch),
                        interpretation="descriptive subset; no causal join-error estimate"))
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before = protected_hashes()
    baseline = OUT / "protected_before.json"
    if baseline.exists():
        if json.loads(baseline.read_text()) != before:
            raise RuntimeError("Protected inputs changed since consolidation began")
    else:
        baseline.write_text(json.dumps(before, indent=2) + "\n")
    config = json.loads((ROOT / "facct/protocol/criteria.yaml").read_text())
    frame = pd.read_csv(ROOT / "analysis/processed/persona_all.csv")
    frame["id"] = frame.domain + ":" + frame.annotation_item_id
    frame["cluster"] = frame.domain + ":" + frame.prompt_id
    prov = pd.read_csv(ROOT / "facct/revision/outputs/text_provenance.csv")
    mask = equality_mask(frame, prov)
    frame["text_status"] = np.where(mask, "byte_identical", "different_text")
    frame.loc[frame.domain == "mental_health", "text_status"] = "embedded_only"
    checks = []
    for domain in ("education", "health"):
        source = pd.read_csv(humt_file(domain), encoding="utf-8-sig")
        subset = frame[frame.domain == domain]
        p = prov.set_index("id").loc[subset.id]
        exported = source.loc[p.export_row.astype(int), "text"].to_numpy()
        recorded_trunc = source.loc[p.export_row.astype(int), "text_trunc"].to_numpy()
        export_prefix = np.asarray([text[:300] for text in exported])
        rated_prefix = np.asarray([text[:300] for text in subset.response])
        equality = subset.response.to_numpy() == exported
        assert np.array_equal(equality, subset.text_status.eq("byte_identical"))
        assert np.array_equal(equality, subset.humt_join_tier.eq("full"))
        for a, b, row in zip(subset.response, exported, p.itertuples()):
            assert hashlib.sha256(a.encode()).hexdigest() == row.rated_sha256
            assert hashlib.sha256(b.encode()).hexdigest() == row.export_sha256
        checks.append(dict(domain=domain, n=len(subset), byte_identical=int(equality.sum()),
            different=int((~equality).sum()), full_tier_equals_byte_identical=True,
            export_trunc_equals_export_first300=int((recorded_trunc == export_prefix).sum()),
            export_trunc_equals_rated_first300=int((recorded_trunc == rated_prefix).sum()),
            differing_pairs_with_same_recorded_prefix=int(((~equality) & (recorded_trunc == rated_prefix)).sum()),
            scorer_invocation_authenticated=False))
    pd.DataFrame(checks).to_csv(OUT / "provenance_checks.csv", index=False)
    comp = composition(frame, config)
    comp.to_csv(OUT / "subset_composition.csv", index=False)
    points = subset_points(frame, config)
    old = pd.read_csv(ROOT / "facct/revision/outputs/text_representation_sensitivity.csv")
    for row in points.itertuples():
        old_row = old[(old.domain == row.domain) & (old.criterion == row.criterion) &
                      (old.policy == row.policy) &
                      (old.sensitivity == "full_join_" + row.mode)]
        assert len(old_row) == 1
        for name in ("n", "selected", "concerns", "caught"):
            assert old_row.iloc[0][name] == getattr(row, name)
    points.to_csv(OUT / "verified_subset_operating_points.csv", index=False)
    text = ["# Provenance consolidation", "", "No new screening experiment or score correction.",
        "All 48 existing byte-identical-subset operating points reproduce from an explicit equality mask.",
        "The stored full-join tier coincides with byte equality in these files; this was tested, not assumed.",
        "No historical scorer invocation is authenticated by this check.", "",
        "| Domain | Batch | Responses | D cases | F cases | OA cases |",
        "|---|---|---:|---:|---:|---:|"]
    summary = comp[comp.category == "all"]
    for (domain, batch), group in summary.groupby(["domain", "batch"], sort=True):
        values = group.set_index("criterion")
        text.append(f"| {domain} | {batch} | {group.n.iloc[0]} | " +
                    " | ".join(str(values.loc[c, "concerns"]) for c in config["criteria"]) + " |")
    text += ["", "Complete condition/model/scenario composition is in subset_composition.csv.",
        "Subset comparisons alter the batch and sometimes its quota; they do not isolate join error.",
        "Missing invocation records cannot be repaired with a fresh score or deterministic join.",
        "Mental health retains embedded scores but has no independent scorer-input string."]
    text += ["", "## Recorded truncated strings", "",
        "The available scorer implementation truncates text to its first 300 characters.",
        "The export also records text_trunc. Checking that field is additional provenance evidence,",
        "not proof that this implementation/version generated the historical score."]
    for check in checks:
        text.append(f"- {check['domain']}: {check['export_trunc_equals_export_first300']}/{check['n']} "
                    f"recorded truncations equal the export's first 300 characters; "
                    f"{check['export_trunc_equals_rated_first300']}/{check['n']} equal the rated text's first 300. "
                    f"Of the differing full-text pairs, {check['differing_pairs_with_same_recorded_prefix']} "
                    "have matching recorded/rated prefixes.")
    (OUT / "findings.md").write_text("\n".join(text) + "\n")
    rows = []
    for domain, title in (("education", "Education"), ("health", "General health")):
        for status, label in (("byte_identical", "Identical"), ("different_text", "Different")):
            g = summary[(summary.domain == domain) & (summary.batch == status)].set_index("criterion")
            rows.append(" & ".join([title, label, str(g.n.iloc[0])] +
                        [str(g.loc[c, "concerns"]) for c in config["criteria"]]) + r" \\")
    tex = [r"\begin{table}[t]", r"\centering\small",
        r"\caption{Available export/rated-text composition. Counts are criterion cases, not harms. Identical strings do not authenticate historical scorer calls; excluded rows change the evaluation population.}",
        r"\label{tab:provenance_composition}", r"\begin{tabular}{llrrrr}", r"\toprule",
        r"Domain & Text pair & $n$ & $D$ cases & $F$ cases & OA cases \\", r"\midrule",
        *rows, r"\bottomrule", r"\end{tabular}", r"\end{table}", ""]
    (OUT / "provenance_composition.tex").write_text("\n".join(tex))
    edu, health = checks
    total = sum(check["n"] for check in checks)
    matching_trunc = sum(check["export_trunc_equals_export_first300"] for check in checks)
    differing = sum(check["different"] for check in checks)
    preserved_prefix = sum(check["differing_pairs_with_same_recorded_prefix"] for check in checks)
    note = (f"The available scorer code truncates its input to 300 characters. {matching_trunc}/{total} recorded "
            r"\texttt{text\_trunc} fields match their export's first 300 characters, but only "
            f"{edu['export_trunc_equals_rated_first300']}/415 education and "
            f"{health['export_trunc_equals_rated_first300']}/415 general-health fields match the "
            f"rated text's first 300 characters. Thus {preserved_prefix} of the {differing} differing full-text pairs "
            f"retain the same recorded prefix and {differing-preserved_prefix} do not. This is evidence about available "
            "export preprocessing, not authentication that the available code/version produced "
            "the historical score. No score is replaced.\n")
    (OUT / "provenance_truncation.tex").write_text(note)
    assert before == protected_hashes(), "Protected input changed"
    (OUT / "manifest.json").write_text(json.dumps(dict(
        scope="reporting verification, not new validation", protected_files=len(before),
        protected_unchanged=True, subset_points_reconstructed=len(points),
        additional_evidence_hashes={str(p.relative_to(ROOT)): sha(p) for p in
            (ROOT / "compute_humt_sociot_colab.py", humt_file("education"), humt_file("health"))},
        code_and_spec={str(p.relative_to(ROOT)): sha(p) for p in
                       sorted(Path(__file__).parent.iterdir()) if p.is_file()},
        outputs={p.name: sha(p) for p in sorted(OUT.iterdir())
                 if p.is_file() and p.name not in ("manifest.json", "protected_before.json", "artifact_check.json")}), indent=2) + "\n")
    print((OUT / "findings.md").read_text())


if __name__ == "__main__":
    main()
