# Computational Scope: Literature and Policy Check

Verified **2 October 2026**. Targeted primary-source check, not an exhaustive novelty review or submission clearance. Existing literature memos and `facct/paper/overleaf/references.bib` supplied leads. Local scope documents describe the proposed contribution; their numerical results, annotation provenance and private CHI submission status were not independently audited here. Only this memo was written; no bibliography, data, manuscript or other file was changed, and nobody was contacted.

## Assessment

The defensible contribution is **corpus-specific evidence about a proposed review-allocation use of HumT**, not a new tone metric, general theory of contextual validity, or novel capacity-constrained routing method. The checked literature already supplies those foundations. None of the checked sources establishes organizational adoption of HumT screening. The authors' [repository README](https://raw.githubusercontent.com/myracheng/humtdumt/main/README.md) documents scoring and fine-tuning, not an operational review program. This is a bounded finding, not proof of universal non-use.

## Verified Primary Records and Claim Boundaries

| Work and verified identity | Already established | What remains specific to PERSONA |
| --- | --- | --- |
| **Cheng, Yu and Jurafsky (2025), HumT DumT: Measuring and controlling human-like language in LLMs.** ACL long **1261**, pp. 25983-26008, DOI 10.18653/v1/2025.acl-long.1261. [ACL record](https://aclanthology.org/2025.acl-long.1261/); [published paper](https://aclanthology.org/2025.acl-long.1261.pdf). | Sections 3-5 introduce relative-LM-probability tone/social-perception measures, human-annotation validation, preference analyses, social-dimension associations, and DumT steering. Risk mitigation is explicitly part of the authors' motivation and interpretation; do not portray them as making no safety-related argument. | The paper does not establish calibrated harm probabilities or the effectiveness of a HumT-prioritized review queue. Testing this downstream use need not invalidate HumT's tone-measurement evidence, nor show that lowering tone causes harm reduction. |
| **Cheng, Blodgett, DeVrio, Egede and Olteanu (2025), Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems.** ACL long **1259**, pp. 25923-25948, DOI 10.18653/v1/2025.acl-long.1259. [ACL record](https://aclanthology.org/2025.acl-long.1259/); [published paper, especially Section 4](https://aclanthology.org/2025.acl-long.1259.pdf). | Literature and crowdsourced rewriting inform an intervention inventory and conceptual framework. Context-dependent effectiveness, apparently contradictory edits, and potentially worsened outcomes are explicitly discussed. | Neither context dependence nor the possibility that removing human-like expressions is inappropriate is new here. PERSONA instead evaluates which existing criterion-labeled responses particular rankings expose to review. This source does not validate PERSONA's thresholds. |
| **Okati, De and Gomez-Rodriguez (2021), Differentiable Learning Under Triage.** NeurIPS 34, pp. 9140-9151. Local key: `okati2021triage` (lowercase). [Proceedings](https://proceedings.neurips.cc/paper/2021/hash/4c4c937b67cc8d785cea1e42ccea185c-Abstract.html); [published paper](https://proceedings.neurips.cc/paper_files/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf). | Section 2, equations (1)-(2), optimizes combined prediction loss with an expected human-assignment upper bound. The optimal routing result depends on model-versus-human losses, not simply a high model score. | PERSONA measures criterion coverage under exact batch quotas, not human-machine prediction accuracy. Their theory does not prove high-HumT optimality. The expectation-level constraint differs from PERSONA's quota, but this distinction alone is not novelty. |
| **Mozannar and Sontag (2020), Consistent Estimators for Learning to Defer to an Expert.** ICML, PMLR 119, pp. 7076-7087. Local key: `mozannar2020defer` (lowercase). [Publisher record and BibTeX](https://proceedings.mlr.press/v119/mozannar20b.html); [published paper](https://proceedings.mlr.press/v119/mozannar20b/mozannar20b.pdf). | Learns a classifier and rejector using sampled expert decisions; supplies a consistent cost-sensitive surrogate and experimental evaluation. Routing must be evaluated against the combined decision objective. | In their setting, non-deferred cases receive model predictions. In PERSONA, non-selected cases remain unreviewed, not cleared. A trained concern screen still does not model subsequent reviewer correctness or implement this estimator. |
| **Alves et al. (2025), A benchmarking framework and dataset for learning to defer in human-AI decision-making.** Scientific Data **12, 506**, DOI 10.1038/s41597-025-04664-y. [Publisher full text](https://www.nature.com/articles/s41597-025-04664-y). | OpenL2D/FiFAR models synthetic experts, integer per-expert capacities over batches, deferral rates and variable availability. Method rankings change with expert composition. The authors explicitly limit synthetic experts to benchmarking rather than replacing real expert evidence. | A particularly close capacity-aware precedent: bounded review, batch constraints and sensitivity to allocation conditions are not new mechanisms. PERSONA's distinction is the HumT/concern-criterion application and its observed allocation patterns, without simulated expert decisions or a combined error-cost objective. |
| **Jacobs and Wallach (2021), Measurement and Fairness.** FAccT, pp. 375-385, DOI 10.1145/3442188.3445901. [Publisher record](https://doi.org/10.1145/3442188.3445901); [author manuscript, Section 3.2.7](https://arxiv.org/pdf/1912.05511). | Measurement modeling distinguishes constructs from operationalizations and examines their assumptions. Consequential validity includes consequences of using measurements; it is part of their account of construct validity, not wholly outside it. | Score-to-use justification is an application of established measurement reasoning. PERSONA's human labels also require justification; they are not unquestionable ground truth. Offline coverage alone does not establish consequential validity. |
| **Hutchinson, Rostamzadeh, Greer, Heller and Prabhakaran (2022), Evaluation Gaps in Machine Learning Practice.** FAccT, DOI 10.1145/3531146.3533233. [Conference paper](https://facctconference.org/static/pdfs_2022/facct22-3533233.pdf); [author manuscript v1, Sections 2-5](https://arxiv.org/html/2205.05256v1). | Examines 200 NLP/CV papers, distinguishes learner-centric from application-centric evaluation, and discusses why threshold-averaged metrics can obscure operating-point consequences. | Reporting capacity-specific coverage, residual cases and alternatives supplies an instance of application-oriented evidence, not discovery that aggregate predictive metrics are insufficient. Neither this paper nor PERSONA's curves establish an effective organizational workflow. |

**Metadata caveat:** The [NeurIPS BibTeX export](https://proceedings.neurips.cc/paper_files/paper/12322-/bibtex) uses `Rodriguez, Manuel`; the published PDF byline is `Manuel Gomez-Rodriguez`. The existing local full-name form follows the PDF, rather than reproducing the export verbatim. The two requested triage/defer entries identify real publications with matching titles, years and pagination; no bibliography edit was made. OpenL2D is an additional verified lead, not a claim that it is already cited locally.

## Corpus-Specific Evidence, Not General Novelty

Based on the [current scope](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/submission/current_scope.md) and [review response](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/submission/review_response_v3.md), the contribution can be stated narrowly:

> On the reused PERSONA corpus, we examine the opportunities for review produced by specified screening policies at equal item capacities: which separately defined concern labels are captured or missed, how the comparison depends on criterion and context, and whether adding recorded HumT improves the specified held-out screens. We do not evaluate reviewer actions, realized harm reduction, or an established organizational HumT deployment.

- **Candidate new evidence:** policy-specific capture/miss counts and paired contrasts; criterion/rater-rule sensitivity; held-out incremental HumT comparisons; and the distribution of selection within a common domain-wide queue. These are corpus-conditioned empirical results, subject to the implementation/provenance checks being conducted separately. Shared-corpus reuse is not independent replication.
- **Not a new method or independent study:** recall/precision at capacity, exact quotas, workload curves derived from the same rankings, or a reporting card. A worked card remains an unevaluated proposal. Common-queue subgroup analysis is descriptively different from subgroup reranking, but does not by itself establish demographic fairness or causal exclusion.
- **Important scope correction:** the older targeted memo's blanket claim of no task-specific model fitting no longer describes the consolidated scope. Fixed HumT/length/marker rankings are unfitted; the later criterion-specific logistic screens are fitted on other prompt groups. Neither component estimates reviewer behavior. Avoid calling the whole study model-free or a learning-to-defer implementation. [Earlier memo](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/submission/revision_literature_check.md); [current scope](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/submission/current_scope.md).
- **Interpretation checks:** marker overlap with rubric cues can explain criterion matching without proving harm detection. Intervals including zero do not demonstrate equivalence or universal HumT redundancy. Equal response counts are not equal review time. Changing evaluation thresholds need not change a fixed policy's selected queue. These are analytical boundaries, not new computations by this check.

**Assessment, not a venue verdict:** This is plausibly a bounded computational extension, not an established first-of-its-kind contribution. Its value must come from informative effect sizes, residual cases and transparent assumptions, rather than reframing alone. The complete CHI/FAccT claim overlap and sufficient independent scholarly significance remain unresolved here.

## Current Official Submission Guidance

### Dates and Format

| Venue | Verified dates and format |
| --- | --- |
| **FAccT 2027 CFP** | Abstract **27 October 2026**; full paper **3 November**; initial decisions **22 December**; revision/rebuttal **28 January 2027**; final decisions **23 March**. Deadlines: 23:59 AoE. Initial submission: **14 content pages**, plus one endmatter-only page; references excluded. Revision/accepted content limit: 15 pages. [Official CFP](https://facctconference.org/2027/cfp.html). |
| **FAccT Author Guide** | Anonymous single-column `\documentclass[manuscript,screen,review,anonymous]{acmart}`. Figures/tables count; references and appendices are unlimited. Appendices belong in the same PDF and need not be reviewed; main text must stand alone. Include AI-use/non-use disclosure and an ethics statement; methodological limitations belong in main text. Representative abstract registration is mandatory; author list and archival choice freeze then. [Official guide](https://facctconference.org/2027/authorguide.html). |
| **CHI 2027 Papers** | Submission **10 September 2026**; reviews **5 November**; resubmission **3 December**; final notification **17 December**, AoE. No separate abstract deadline. Anonymous single-column review; 5,000-8,000 words encouraged, over 12,000 needs strong justification; abstract at most 150 words. [Official Papers page](https://chi2027.acm.org/authors/papers/). |

### Overlap and Uncertainty

- **FAccT prohibits identical or substantially similar work** under review, accepted or published elsewhere; there is no numerical overlap safe harbor. Its evaluations focus area is relevant, but insufficient social engagement or purely hypothetical concerns are out of scope. Computational-only status is not itself disqualifying or sufficient. [CFP](https://facctconference.org/2027/cfp.html).
- **CHI requires originality and anonymous concurrent-paper disclosure** for related work sharing a study, artifact or dataset; omission can cause desk rejection. The same-corpus pair therefore requires disclosure if concurrent, but disclosure does not authorize duplication. The Papers page does not specify a post-deadline route for adding a newly arising related submission. [CHI Papers](https://chi2027.acm.org/authors/papers/).
- **Timing inference:** ordinary CHI reviews arrive after FAccT's full deadline, so waiting for them cannot resolve concurrency in time. An actual earlier rejection/effective withdrawal can change status; expected rejection cannot. Reused data alone neither proves nor disproves substantial similarity. These are policy implications, not private-status verification. [FAccT dates/rule](https://facctconference.org/2027/cfp.html); [CHI dates](https://chi2027.acm.org/authors/papers/).
- **FAQ mismatch:** FAccT's abstract-registration example assumes notification between its deadlines, unlike CHI's ordinary schedule; it requires withdrawal if the other paper is accepted or remains under review beyond the full deadline. Its non-archival journal exception is not a concurrent-CHI workaround. Abstract registration is not full-paper clearance. [Author Guide](https://facctconference.org/2027/authorguide.html).
- **Conflicting guidance:** CFP requires all authors to sign up to review; Author Guide encourages at least one. Plan for the stricter requirement pending clarification. CHI's review-process page says early notifications around **October 25**; its process announcement says **October 26** in the opening schedule and **October 25** later. None is a guaranteed outcome date. [FAccT CFP](https://facctconference.org/2027/cfp.html); [Author Guide](https://facctconference.org/2027/authorguide.html); [CHI review process](https://chi2027.acm.org/authors/papers/papers-review-process/); [CHI announcement](https://chi2027.acm.org/2026/08/17/how-the-chi-2027-papers-review-process-will-work/).
- **Unverified routes/limits:** FAccT's guide does not identify a dedicated related-manuscript upload field. The linked [ACM simultaneous-submissions policy](https://www.acm.org/publications/policies/simultaneous-submissions) was not retrievable, so no unseen ACM exception is asserted. Author-handled chair guidance and accurate confidential disclosure remain necessary unresolved steps, not actions taken here. Neither silence nor this memo establishes permission. Recheck live policies and actual submission status before proceeding.

## Verification Limits

Searches were targeted to the named works, measurement-use foundations, capacity-constrained human review, and HumT screening; irrelevant acronym matches and secondary summaries were not used as evidence. Some browser PDF/HTML follow-up requests timed out. NeurIPS was read at its canonical `paper_files` PDF; Hutchinson's detailed support was checked in the explicitly identified author manuscript; Nature and CHI process text were additionally retrieved directly from their official sites. No exhaustive novelty claim, organizational adoption claim, empirical rerun, manuscript eligibility certification or full-project formatting/page-count verification is supplied.

## Addendum: Publisher-Verified OpenL2D/FiFAR Citation

Reverified **2 October 2026** directly against the [Scientific Data publisher record](https://www.nature.com/articles/s41597-025-04664-y): its `citation_author`, `citation_title`, `citation_volume`, `citation_issue`, `citation_online_date` and `citation_doi` metadata, structured author list, and displayed citation. Publication date: **23 April 2025**; volume **12**, article **506**. The browser encountered a redirect error, but direct retrieval of the publisher HTML succeeded.

The following is BibTeX formatted from that primary metadata, not a claimed verbatim publisher BibTeX export. It includes all eight authors in publisher order and preserves their full published name forms; middle initials are not speculatively expanded. Accents use ASCII LaTeX escapes. `articleno` records the article identifier, not a page range; `alves2025openl2d` is a proposed local citation key.

```bibtex
@article{alves2025openl2d,
  author = {Alves, Jean V. and
            Leit{\~a}o, Diogo and
            Jesus, S{\'e}rgio and
            Sampaio, Marco O. P. and
            Li{\'e}bana, Javier and
            Saleiro, Pedro and
            Figueiredo, M{\'a}rio A. T. and
            Bizarro, Pedro},
  title = {A benchmarking framework and dataset for learning to defer in human-{AI} decision-making},
  journal = {Scientific Data},
  year = {2025},
  volume = {12},
  number = {1},
  articleno = {506},
  doi = {10.1038/s41597-025-04664-y},
  url = {https://www.nature.com/articles/s41597-025-04664-y}
}
```

**Exact comparison sentence** (cite `alves2025openl2d` after the first clause):

> Whereas OpenL2D/FiFAR benchmarks learning-to-defer methods with synthetic experts and per-batch capacity constraints, PERSONA evaluates HumT-based and alternative rankings against existing concern labels at fixed review budgets without modeling reviewer decisions.

The first clause is supported by the publisher's Methods and L2D Benchmarking sections; the PERSONA clause describes the local computational scope, not a claim made by Alves et al. [Publisher full text](https://www.nature.com/articles/s41597-025-04664-y).
