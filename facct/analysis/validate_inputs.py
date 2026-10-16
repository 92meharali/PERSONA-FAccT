"""Read-only validation of the released analysis corpus and submission snapshot."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from pypdf import PdfReader


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_hashes(root):
    paths = set()
    for directory in ("data", "analysis/processed", "analysis/outputs", "submission/chi2027_supplement"):
        paths.update(p for p in (root / directory).rglob("*") if p.is_file() and "__pycache__" not in str(p))
    paths.update((root / "paper").glob("*.tex"))
    paths.add(root / "paper/ref.bib")
    return {str(p.relative_to(root)): sha(p) for p in sorted(paths)}


def validate(root, out, pdf=None):
    d = pd.read_csv(root / "analysis/processed/persona_all.csv")
    r = pd.read_csv(root / "analysis/processed/persona_ratings_long.csv")
    keys = ["domain", "annotation_item_id"]
    if d.duplicated(keys).any() or r.duplicated(keys + ["rater_group", "annotator_id"]).any():
        raise ValueError("Duplicate response or rater keys")
    needed = keys + ["prompt_id", "model", "condition", "scenario_type", "prompt", "response", "H", "E", "D", "F", "OA"]
    if d[needed].isna().any().any() or not np.isfinite(d[["H", "E", "D", "F", "OA"]]).all().all():
        raise ValueError("Incomplete source inputs")
    if not d[["E", "D", "F", "OA"]].apply(lambda x: x.between(1, 5)).all().all():
        raise ValueError("Invalid mean rating range")
    if not d.condition.isin(["natural", "adversarial"]).all():
        raise ValueError("Unknown condition")
    if d.duplicated(["domain", "prompt_id", "model"]).any():
        raise ValueError("Duplicate model within prompt")
    if not np.allclose(d.H, d.humt, rtol=0, atol=1e-12):
        raise ValueError("H and stored HumT differ")
    metadata = r.merge(d[keys+["prompt_id","model","condition"]],on=keys,how="left",validate="many_to_one",suffixes=("_rating","_response"))
    for col in ("prompt_id","model","condition"):
        if not (metadata[col+"_rating"] == metadata[col+"_response"]).all():
            raise ValueError(f"Long/response metadata mismatch: {col}")
    d["id"] = d.domain + ":" + d.annotation_item_id
    d["cluster"] = d.domain + ":" + d.prompt_id
    audit = []
    for col in ("OA", "E", "D", "F"):
        values = r[col + "_score"].dropna()
        if not values.between(1, 5).all() or not (values == values.round()).all():
            raise ValueError("Noninteger/out-of-range source ratings")
        means = r.groupby(keys)[col + "_score"].agg(["mean", "count"])
        joined = d.set_index(keys).join(means)
        delta = float((joined[col] - joined["mean"]).abs().max())
        if not (joined["count"] == 5).all() or delta > 1e-10:
            raise ValueError(f"Rating reconstruction failed: {col}, {delta}")
        audit.append({"check": f"{col}_mean_reconstruction", "value": delta, "status": "pass"})
    if not r.loc[r.rater_group == "Group A", ["E_score", "D_score", "F_score"]].isna().all().all():
        raise ValueError("Group A contains dimension scores")
    if not r.loc[r.rater_group == "Group B", "OA_score"].isna().all():
        raise ValueError("Group B contains OA scores")
    if len(r) != len(d) * 10 or set(r.rater_group) != {"Group A", "Group B"}:
        raise ValueError("Unexpected rater design")
    for fname in ("persona_all.csv", "persona_ratings_long.csv"):
        a = root / "analysis/processed" / fname
        b = root / "submission/chi2027_supplement/analysis/processed" / fname
        same = b.exists() and sha(a) == sha(b)
        audit.append({"check": f"submission_snapshot_hash:{fname}", "value": same, "status": "pass" if same else "investigate"})
    counts = d.groupby("domain").agg(responses=("id", "size"), prompts=("cluster", "nunique"))
    counts.to_csv(out / "tables/input_counts.csv")
    d.groupby(["domain", "prompt_id_source", "model_source", "humt_join_tier"]).size().rename("n").to_csv(out / "tables/metadata_provenance.csv")
    d.groupby(["domain", "condition", "scenario_type", "model"]).size().rename("n").to_csv(out / "tables/context_counts.csv")
    cluster = d.groupby(["domain", "cluster"]).agg(responses=("id", "size"), models=("model", "nunique"), prompt_texts=("prompt", "nunique"))
    cluster.to_csv(out / "tables/prompt_audit.csv")
    d.isna().sum().rename("missing").to_csv(out / "tables/missingness.csv")
    d.groupby("domain")[["H", "E", "D", "F", "OA"]].agg(["min", "max", "mean", "std"]).to_csv(out / "tables/ranges.csv")
    # Anonymous IDs document released structure, not verified real-world identities.
    r.groupby(["domain", "rater_group", "annotator_id"]).size().rename("ratings").to_csv(out / "tables/rater_counts.csv")
    pd.DataFrame(audit).to_csv(out / "tables/input_checks.csv", index=False)
    cv = pd.read_csv(root / "analysis/outputs/tables/cv_performance.csv")
    headline = []
    for domain, submitted in (("mental_health", .659), ("education", .562), ("health", .256)):
        row = cv[(cv.domain == domain) & (cv.specification == "H+E+D+F")].iloc[0]
        headline.append(dict(claim=f"{domain} full-profile CV R2", pdf_reported=submitted,
                             released_output=float(row.cv_r2_mean), matches_at_reported_precision=round(row.cv_r2_mean,3)==submitted,
                             evidence="existing CHI output; not newly fitted"))
    ceiling = (d.loc[d.domain=="health", "OA"]==5).mean()*100
    headline.append(dict(claim="health OA ceiling percent", pdf_reported=63.86, released_output=ceiling,
                         matches_at_reported_precision=round(ceiling,2)==63.86, evidence="recomputed from current inputs"))
    pd.DataFrame(headline).to_csv(out / "tables/chi_headline_crosscheck.csv",index=False)
    pdf_info = {"available": False, "release_linkage": "unverified"}
    if pdf and Path(pdf).is_file():
        reader = PdfReader(pdf)
        text = "\n".join(p.extract_text() for p in reader.pages)
        terms = ["1,490", "660", "415", "499", ".659", ".562", ".256", "63.86%"]
        pdf_info = {"available": True, "sha256": sha(pdf), "pages": len(reader.pages), "claim_tokens_found": {t: t in text for t in terms}, "release_linkage": "counts and headline numerical claims consistent; byte-identical supplement data; actual submitted supplement identity requires author confirmation"}
        snippets = []
        for i, page in enumerate(reader.pages):
            lines = page.extract_text().splitlines()
            for j, line in enumerate(lines):
                if any(t in line for t in ("compensation", "1,490", ".659", "63.86%")):
                    snippets.append(f"Page {i+1}: " + " ".join(lines[max(0,j-1):j+3]))
        (out / "reports/submitted_pdf_checks.md").write_text("# Submitted PDF checks\n\nLocal supplied PDF only; not a verified portal download.\n\n" + "\n\n".join(snippets))
    (out / "reports/input_audit.md").write_text("# Input audit\n\n" + counts.to_string() + "\n\nFive ratings per construct reconstruct every stored mean exactly (numerical tolerance 1e-10). Source columns distinguish inferred from native metadata; see metadata_provenance.csv. All H values are finite; final-corpus availability is not proof of join correctness or original collection completeness.\n\nThe submitted PDF's counts and numerical claim tokens are checked, and released processed files are compared with the repository's submission snapshot. This supports numerical consistency, not an authenticated historical chain of custody. Authors must confirm this supplement was actually submitted. See decisions.md for payment and collection-history questions. Anonymous IDs cannot independently establish distinct real-world people.\n\n" + json.dumps(pdf_info, indent=2))
    if not all(x["matches_at_reported_precision"] for x in headline):
        raise ValueError("CHI headline mismatch: stop claims linking this release to the submission")
    return d, r, pdf_info
