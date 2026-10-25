# PERSONA: Tone-Score Review Allocation

## Current paper: 26 October 2026

**When Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization**

- [Active manuscript](paper/overleaf/main.tex)
- [Latest Overleaf ZIP](releases/PERSONA_FAccT_Overleaf_2026-10-26_professor.zip)
- [Professor response and verified results](submission/professor_response_2026-10-26.md)
- [Source checks](submission/professor_primary_sources_2026-10-26.md)
- [Current scope](submission/current_scope.md), [readiness](submission/readiness.md), and [claim ledger](paper/claims_ledger.md)
- [Layout audit](paper/qa/2026-10-26/layout_report.json): 14 content pages, one endmatter,
  two references and 14 appendix pages; 31 total, 24 cited references.

The four questions concern enrichment, comparative allocation, incremental value,
and distribution of coverage. The paper evaluates a proposed fixed-capacity review
queue, not demonstrated reviewer effectiveness or harm reduction.

## Evidence

The corpus contains 1,490 responses: mental health 660, education 415 and general
health 415. At 132 mental-health review slots, HumT captures 42/165 broad-D cases,
full-text markers 63 and 300-character markers 68. Under mean D > 3, the counts
are 13, 26 and 22 of 57; the paired HumT-minus-prefix interval reaches zero.
The assessment follow-up has 19 resolved concerns: HumT captures six and full
markers twelve, with wide paired intervals crossing zero. All nine trained
incremental-recall intervals include zero; this is not evidence of equivalence.

- [Original screening, sensitivity and workload](outputs/reports/results.md)
- [Original input audit](outputs/reports/input_audit.md)
- [Cutoffs, fusion and representation sensitivity](revision/outputs/findings.md)
- [Trained conditional lift](conditional/outputs/findings.md)
- [Common-queue category coverage](allocation/outputs/findings.md)
- [Independent assessment follow-up](independent_annotation/README.md)
- [Latest matched-window and strict-threshold checks](professor_revision/README.md)
- [Provenance consolidation](consolidation/outputs/findings.md)
- [LLM-judge status and limitations](llm_judge/README.md)

All 61 exclusive cases have an AI-assisted descriptive coding draft for author
verification. Its semantic frequencies are not manuscript findings. Original
ratings, original outputs and protocols are preserved, including unfavorable
results and exploratory-analysis disclosures.

## Reproduce and verify

From the repository root, use Python 3.12 and pinned dependencies:

```bash
python -m pip install -r facct/requirements.txt
python -m facct.analysis.verify_outputs
python -m pytest facct -q
```

Stage-specific commands:

```bash
python -m facct.analysis.run
python -m facct.revision.run
python -m facct.conditional.run
python -m facct.allocation.run
python -m facct.professor_revision.run
python -m facct.professor_revision.build_assets
```

The latest sensitivity run takes about 16 seconds locally with 2,000 paired
prompt-cluster draws per domain. The trained stage previously took about 178
seconds. The full original computational verification is
`python -m facct.consolidation.verify --fresh-env` (previously about eight minutes).
Follow-up reconstruction and the latest sensitivity runner require the authorized
external assessor ID map documented in their manifests; private returns and consent
records are not distributed. The supplied companion PDF is also an external input.
Do not describe those stages as independently reproducible from this repository alone.

Original figures/CSVs and amended outputs remain separate. Do not run a historical
manuscript generator over the edited active source. To package the current source:

```bash
python -m facct.paper.package_text_revision --release-name PERSONA_FAccT_Overleaf_2026-10-26_professor --revision-date 2026-10-26 --revision-scope "Professor feedback: review-setting pitch, self-contained corpus, paired 300-character and strict-cutoff sensitivity; original evidence preserved" --additional-assets-manifest facct/professor_revision/outputs/asset_manifest.json --layout-report facct/paper/qa/2026-10-26/layout_report.json
```

The layout report must match the source, bibliography and class. Any later source
revision needs recompilation and a new layout audit before packaging.

## Retained supporting material

Protocols, manifests, evidence checks and dated response records are provenance,
not alternative current drafts. Capability-study and practitioner-study materials
remain explicitly prospective, not new results or authorized recruitment.
Source annotation data and inherited companion materials remain unchanged because
current checks depend on their hashes. Superseded FAccT manuscript copies and
release ZIPs have been removed from the current tree and remain in Git history.
See the [cleanup record](submission/repository_cleanup_2026-10-26.md).

The paper is ready for the requested internal review, not certified for submission.
Author verification of the semantic coding and the requested reviews by Dr. Ibrahim
and Dr. Wafa remain outstanding. No email or submission has been sent.
