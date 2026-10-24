# PERSONA: proposed tone-score review allocation

## Current scope: completed audit, 24 October 2026

The author has chosen **no new experiments for this deadline**. This supersedes
the October 23 audit-plus-capability-protocol direction. The restored paper is
*When Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization*:
RQ1 comparative allocation, RQ2 incremental benefit, and RQ3 coverage in a shared
queue. Its evidence is the completed audit and supplied mental-health assessment
follow-up; existing estimates, ratings, and analysis scope are preserved.

Capability study documents, code, and the unassessed relevance sample are retained
as future work only. They are not new empirical findings, active submission RQs,
or experiments promised before this deadline. The prospective RQ sections/appendix
have been removed from the active source. The [October 23 prospective source](capability/archive/main_capability_prospective_2026-10-23.tex)
is archived separately.

No actual capability-conditioned judgments or semantic-judge runs are reported.
Assessor qualifications, recruitment/pay, supporting ethics documentation, and
CHI overlap/disclosure/eligibility remain author gates. Completed analyses do not
mean complete reporting or a submission-ready manuscript. The restored active
source compiled with the native compiler and isolated pdfLaTeX; the
[October 24 layout audit](paper/qa/2026-10-24/layout_report.json) records 14 main-content,
one endmatter, one references, and 12 appendix pages (28 total), within the
main-content and endmatter limits.

## Historical direction: 23 October 2026 (superseded)

The following paragraph records the October 23 state, not the current scope.
Its unchecked-layout status is superseded by the October 24 audit above.

The 23 October author-approved direction asks what verified system information is
needed to review anthropomorphic implications. See the [study implementation](capability/README.md)
and [change record](submission/capability_implementation_2026-10-23.md). The
[archived manuscript](capability/archive/main_capability_prospective_2026-10-23.tex) separates completed audit results (A1-A3)
from new prospective questions (RQ1-RQ3). No new capability-conditioned judgments
or semantic-evaluator results exist yet. Earlier status notes below are historical
and do not override this prospective scope. The source manuscript compiled
successfully in the desktop editor; page-count compliance remains unchecked.

**Manuscript status: computational audit plus a new mental-health assessment follow-up; internal review.** The [integration record](submission/annotation_integration.md) documents the 10 October update. The manuscript now includes the [verified follow-up](independent_annotation/README.md), with 19 resolved positives, original-queue HumT coverage of 6 versus markers' 12, and wide paired intervals crossing zero. The CHI response corpus and results remain unchanged. Practitioner evaluation remains deferred; assessor qualifications, recruitment/compensation and the supporting ethics reference still need completion.

**Current author decision:** integrate the supplied human assessment records and retain all important methodological caveats. The author confirms separation from the original author/rater team and prior consent/ethics coverage; this is an attestation, not independently inspected documentation. The author has deferred supplying the remaining details. Practitioner sessions and additional AI-agent experiments remain deferred. The [scope record](submission/current_scope.md) distinguishes the current amendment from its earlier computational-only scope.

Historical October 23 title: *From Tone Scores to Capability Evidence: Auditing Review Allocation for Anthropomorphic AI*. The October 24 title and RQ mapping above supersede it.

## Start here

- [Final consolidation and changes](submission/computational_consolidation_response.md), [contribution brief](submission/contribution_brief.md), and [provenance assessment](submission/provenance_consolidation.md)
- [Fresh-environment full verification](consolidation/verification/verification.json) and [targeted primary-source check](submission/computational_scope_literature_check.md)
- [Current LaTeX manuscript](paper/overleaf/main.tex) and [Overleaf package](releases/PERSONA_FAccT_Overleaf_2026-10-24_chat_audit.zip)
- [Conditional-lift findings](conditional/outputs/findings.md) and [four-comment implementation response](submission/conditional_response.md)
- [Common-queue findings](allocation/outputs/findings.md) and [latest review response](submission/review_response_v3.md)
- [Earlier computational Markdown draft](paper/generated/computational_review_draft.md) (historical predecessor)
- [Professor-review brief](submission/professor_review_brief.md)
- [Issue-resolution tracker](submission/resolution_tracker.md), [GitHub provenance findings](submission/provenance_resolution.md), and [substantive CHI comparison](submission/distinctness_assessment.md)

- [Results and decision gates](outputs/reports/results.md)
- [Sensitivity and workload findings](outputs/reports/sensitivity_findings.md)
- [Input audit](outputs/reports/input_audit.md) and [submitted PDF checks](outputs/reports/submitted_pdf_checks.md)
- [Primary-source literature and venue policy review](outputs/reports/literature_and_policy.md)
- [Frozen analysis specification](protocol/analysis_plan.md), [criteria](protocol/criteria.yaml), [prior exploration](protocol/explored_data_register.md), [decisions](protocol/decisions.md)
- [Current CHI overlap matrix](submission/current_overlap_matrix.md) and [frozen original comparison](protocol/overlap_matrix.md)
- [Audit-use card](outputs/reports/audit_use_card.md)
- [External study protocol](study/protocol.md) and [paper outline](paper/outline.md)
- [60-minute session plan](study/session_plan.md), [launch checklist](study/launch_checklist.md), and [prepared session packets](study/materials/README.md)
- [Claim ledger](paper/claims_ledger.md) and [readiness](submission/readiness.md)
- [Change record](CHANGELOG.md) and [independent verification](outputs/verification.json)

## Reproduce

Use Python 3.12 in an isolated environment. Install the pinned dependencies with `python -m pip install -r facct/requirements.txt`. From the repository root, the original-stage command is:

```bash
python -m facct.analysis.run
```

The final run uses 2,000 paired prompt-cluster bootstrap replicates per domain and for the secondary pooled batch. Allow approximately 1-3 minutes on a modern laptop; exact measured runtime is recorded in [manifest.json](outputs/manifest.json). The supplied submitted PDF is read from the documented Downloads path if available; use `--pdf /absolute/path/to/submitted.pdf` elsewhere. Missing PDF access is explicitly recorded, not treated as verification.

```bash
python -m pytest facct/tests -q
```

Independently check generated point estimates against scikit-learn and verify source/code/output hashes:

```bash
python -m facct.analysis.verify_outputs
```

For an independent full rerun, use `python -m facct.analysis.run --output facct/reproduction_outputs`, then `python -m facct.analysis.verify_outputs --compare facct/reproduction_outputs`. The comparison requires byte-identical CSVs and figures, not just rounded agreement; runtime-dependent report text is excluded from that equality check.

Pilot runs must use a separate output directory and are labeled pilot:

```bash
python -m facct.analysis.run --replicates 25 --output facct/pilot_outputs
```

The `.yaml` criteria file uses JSON syntax, a valid YAML subset, so no additional YAML dependency is required. No network API or model call is used by the computational pipeline. Sources are hashed before and after execution. The pipeline only writes below `facct/`; never rerun the older CHI pipeline as part of this command.

## Outputs and interpretation

`screening.csv` contains exact integer budgets for ranked policies and analytical expectations for random policies. Thus random caught/missed counts can be fractional. Each metric has pointwise interval and finite-replicate count fields; AP and ROC-AUC are undefined where their class requirements fail. Workload fields are fractions of the batch needed to reach specified recall, not minutes. Uniform-random workload is the expected order-statistic workload; stratified-random workload is undefined because it is only specified at discrete allocations.

Primary multiplicity-adjusted intervals apply **only** to high_H minus uniform_random recall, D >= 3, 20%, within three domains. Other stored adjusted fields are not additional primary tests. All other comparisons are exploratory. Sparse cells are flagged; no empirical deployment prevalence, human-harm probability, or model-family ranking is inferred.

The case sample is deliberately criterion/status-stratified, not prevalence-representative. Blank human-coding templates do not constitute coded data. Store participant/consent records elsewhere. Do not share raw response examples publicly until source-license and anonymity checks are completed.

## Change scope

All new work is under `facct/` and originated on `research/facct-review-allocation`, based on Git revision `7605174`. Original CHI data, manuscripts, bibliography, analyses and original working-tree changes are preserved. No PR, chair email, recruitment, or submission was made. The current internal-review manuscript incorporates supplied human records without certifying their provenance; see readiness for remaining author gates.

Regenerate the review draft and its tables with `python -m facct.paper.build_review_tables`. Edit `paper/computational_draft.template.md`, not the generated draft. This command reads existing outputs and writes only `facct/paper/generated/`. The review manifest records its inputs separately without changing the frozen computational manifest. Run all package tests with `python -m pytest facct/tests facct/study/test_materials.py facct/paper/test_review_build.py -q`.

## Overleaf manuscript

The active source is [paper/overleaf/main.tex](paper/overleaf/main.tex), restored to the October 24 completed-audit scope. Use the [October 24 package](releases/PERSONA_FAccT_Overleaf_2026-10-24_chat_audit.zip). The October 23 ZIP is historical. The generated Markdown draft is a predecessor, not the authoritative manuscript.

The restored source compiled successfully with the native compiler and isolated pdfLaTeX. The [October 24 layout report](paper/qa/2026-10-24/layout_report.json) records 14 main-content pages, one endmatter page, one references page, and 12 appendix pages (28 total); visual inspection found no visible clipping or overlap. The [official author guide and FAQ](https://facctconference.org/2027/authorguide.html) allow 14 main-content pages plus one endmatter-only page, with unlimited references and appendices excluded from that limit and appendices in the same PDF. Anonymous single-column format, AI-use disclosure, and ethics reporting are required. The measured page counts meet the main-content and endmatter limits; author provenance, accurate disclosures, source rights, anonymity, final package contents, and publication eligibility remain separate checks.

## Post-review analyses

Run `python -m facct.revision.run` to regenerate the [first exploratory revision outputs](revision/outputs/findings.md), approximately 20 seconds locally with 2,000 paired cluster draws per domain. The [first amendment](revision/plan.md) predates those added runs but follows inspection of the original results. It preserves the original primary family and frozen outputs. Additions include fixed rank fusion and complementary cases, paired workload differences, oracle/lift context, reliability and cutoff diagnostics, and text-representation/fixed-capacity provenance checks. That historical amendment did not include training. The later trained analysis below supersedes that scope statement without rewriting its outputs or history. No LLM judge was added.

## Conditional-lift amendment

Reproduce the complete added analysis with:

```bash
python -m facct.conditional.run
```

The final run took **178 seconds** locally. It uses five prompt-group-held-out batches, separate logistic screens for every domain and D/F/OA criterion, training-only scaling, and 2,000 paired **refitted** cluster bootstrap draws per domain. Reduced features are markers and log-length; the extended model adds HumT. No tuning, new annotation, or external API is used. Ten additional fixed partitions assess split sensitivity. See the [prospective post-review amendment](conditional/plan.md) and [configuration](conditional/config.json); this is not preregistration of unseen data.

All nine incremental-recall intervals include zero at the reference fraction. This is not proof of equivalence or universal HumT redundancy. The [performance table](conditional/outputs/performance.csv) retains all 252 domain/criterion/policy/budget cells. The manuscript shows all 45 original/fusion and 63 held-out reference cells, including unfavorable fit/OA results. Held-out capacities are 130/660, 80/415, and 80/415, distinct from the original full-batch capacities; all policies are matched within each evaluation family. Training uses historical human labels, with acquisition requirements explicitly reported rather than equated with label-free rules.

Fold assignments, out-of-fold scores, fitted coefficients, training counts, bootstrap differences, split results, and input/output hashes are retained under `conditional/outputs/`. The original `outputs/` and `revision/` trees remain unchanged. Rebuild the typesetting ZIP with `python -m facct.paper.build_overleaf` after running the analyses.

Run all checks with `python -m pytest facct/tests facct/study/test_materials.py facct/paper/test_review_build.py facct/paper/test_overleaf.py facct/revision/test_revision.py facct/conditional/test_conditional.py -q`.

## Common-queue audit and presentation revision

```bash
python -m facct.allocation.run
```

The new analysis takes approximately **18 seconds** locally with 2,000 paired whole-prompt draws per domain. Its [post-review specification](allocation/plan.md) distinguishes projection of a domain-wide queue from the earlier subgroup-specific ranking procedure. It reports all 525 condition/model/scenario-by-criterion-by-policy cells and exact selection identities, without raw response text. Subgroups receive no independent quota. Zero-concern recall remains undefined; intervals are pointwise exploratory and sparse/complement support is explicit.

The condition view shows that aggregate performance can hide coverage differences. General-health markers catch 32 fit cases overall versus HumT's 25, but four versus eight among natural prompts. That natural-prompt policy difference is uncertain (+5.4 pp for HumT, 95% interval -1.3 to +13.0), not proven superiority. All condition/criterion cells are reported together. No causal unfairness, demographic disparity, or stakeholder-validated allocation is claimed.

The manuscript now leads with accountability for review allocation, clarifies criterion versus queue changes, explains the transparent model choice and separate OA raters, and retains denominators in the abstract. New generated figures show all nine paired baseline contrasts, all nine trained increments, and workload at all four original recall targets. No new citations, source ratings, thresholds, equivalence margins, external participants, or semantic judges were introduced.

Rebuild the full Overleaf package with `python -m facct.paper.build_overleaf`. Run the complete suite with `python -m pytest facct/tests facct/study/test_materials.py facct/paper/test_review_build.py facct/paper/test_overleaf.py facct/revision/test_revision.py facct/conditional/test_conditional.py facct/allocation/test_allocation.py -q`.

The anonymous reproducibility supplement remains a separate release task: the Overleaf ZIP contains typesetting sources and aggregates, not full analysis inputs/code. See [artifact release checklist](submission/artifact_release_checklist.md) before asserting reviewer reproducibility or distributing source material.

## Final computational-only consolidation

The active manuscript now has three empirical questions: comparative allocation,
incremental benefit, and distribution of coverage within a common queue. The worked
card is supporting reporting, not an evaluated contribution. Scope is restricted to
transparent policies and the specified trained model, not semantic-judge competitiveness.

One command reruns **all four** completed stages in an isolated copy, installs pinned
dependencies in a fresh environment, and compares every numerical CSV and figure:

```bash
python -m facct.consolidation.verify --fresh-env
```

The verified run took **466 seconds (about eight minutes)** including setup. All 59
CSV/figure outputs were byte-identical and 270 protected files remained unchanged.
This requires the complete authorized checkout and network access for installation;
it is computational reproducibility, not independent scientific validation.

`python -m facct.consolidation.audit` reconstructs the 48 existing identical-text
subset points and writes condition/model/scenario composition without altering old
outputs. Export equality does not authenticate historical scorer inputs.

`python -m facct.consolidation.build_artifact` builds and extraction-tests a **local
code/aggregate review candidate**, excluding raw response text and private records.
It supports hash/arithmetic checks, not full statistical reruns without the omitted
inputs. Rights and anonymity approval are pending; do not upload it as a certified
full reproducibility supplement. See its README and the release checklist.

Run the complete test suite with:

```bash
python -m pytest facct/tests facct/study/test_materials.py facct/paper/test_review_build.py facct/paper/test_overleaf.py facct/revision/test_revision.py facct/conditional/test_conditional.py facct/allocation/test_allocation.py facct/consolidation/test_consolidation.py -q
```
