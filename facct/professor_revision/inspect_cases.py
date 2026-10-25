"""Validate and format assistant-authored case drafts for author review only."""
import json
import pandas as pd
from facct.professor_revision.run import ROOT


def main():
    private = ROOT / "private/professor_revision_2026-10-26"
    packet = pd.read_csv(private / "cases_blinded.csv").set_index("case_id")
    draft = json.loads((private / "coding_draft.json").read_text())
    d = pd.DataFrame(draft["entries"], columns=["case_id", "draft_code", "evidence_span", "draft_note"])
    assert d.case_id.is_unique and set(d.case_id) == set(packet.index)
    assert d.draft_code.isin(["support_validation", "therapeutic_role", "quoted_role_demonstration", "other"]).all()
    for row in d.itertuples():
        assert row.evidence_span in packet.loc[row.case_id, "response"], row.case_id
    d["draft_producer"] = draft["coder"]
    d["review_status"] = "author_verification_pending"
    for name in ("author_code", "author_reason", "reviewer_id"):
        d[name] = ""
    d.to_csv(private / "coding_draft.csv", index=False)
    key = pd.read_csv(private / "case_key.csv")
    summary = d.merge(key[["case_id", "policy_only"]], on="case_id", validate="one_to_one")
    summary.groupby(["policy_only", "draft_code"]).size().rename("n").to_csv(private / "draft_summary.csv")
    print(f"Verified all {len(d)} case IDs and exact evidence spans; author review remains pending.")
    print(summary.groupby(["policy_only", "draft_code"]).size().to_string())


if __name__ == "__main__":
    main()
