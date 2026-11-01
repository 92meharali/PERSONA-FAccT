# Cross-criterion review-screen transfer: bounded primary-source check

Checked: 2026-10-28. Scope: six selected primary research sources, plus current official FAccT 2027 submission guidance. This is a targeted literature check, not a systematic review or a priority search. Interpretations and proposed reporting choices below are distinguished from the sources' results. No new analysis results are asserted.

## Bottom line

Position the proposed study as an **exploratory comparison of training-target choice in review allocation**, not a new algorithm or proof of construct validity. The closest empirical precedent is **Obermeyer et al. (2019), Table 2**. [Primary paper](https://www.ftc.gov/system/files/documents/public_events/1548288/privacycon-2020-ziad_obermeyer.pdf).

The useful contribution here would be the concrete evidence about which PERSONA concern judgments receive scarce review slots when the same lexical logistic-regression pipeline is trained against different criteria, including evaluation against a separately assessed mental-health reviewworthiness endpoint. Whether that evidence is informative depends on the completed estimates, uncertainty, and residual-case patterns, not on naming the matrix.

## Local context and terminology

Read-only context: [current manuscript](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/facct/paper/overleaf/main.tex) and [bibliography](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/facct/paper/overleaf/references.bib). These are working files being revised separately; this note does not certify the eventual manuscript or implemented analysis.

- The manuscript defines broad anthropomorphic-implication concern as mean D >= 3, domain-fit concern as mean F < 4, and overall-appropriateness concern as mean OA < 4. Prefer these operational names to an unqualified "D risk" or "harm" label.
- Its lexical LR uses marker fraction and log(1 + length), with training-only standardization and fixed regularization. Its existing incremental comparison adds recorded HumT. Keep feature addition distinct from the proposed training-target comparison.
- OA comes from a different rater group and measures a different construct. The later contextual-reviewworthiness assessment concerns existing MH responses, not a fresh external corpus. The manuscript reports 19 resolved positives and cautions that neither endpoint is validated harm ground truth.
- Use "cross-criterion transfer" to mean transfer of a learned ranking's usefulness across evaluation criteria. Unless training actually moves between domains, this is not cross-domain transfer learning, domain adaptation, or deployment validation.

## Six closest sources

### 1. Obermeyer, Powers, Vogeli, and Mullainathan (2019): closest empirical design

**Dissecting racial bias in an algorithm used to manage the health of populations.** Science 366(6464), 447-453. [Publisher/DOI](https://doi.org/10.1126/science.aax2342); [readable primary paper](https://www.ftc.gov/system/files/documents/public_events/1548288/privacycon-2020-ziad_obermeyer.pdf).

**Supported result:** In "Experiments on label choice" and Table 2, three models trained using the same procedure target total cost, avoidable cost, and active chronic conditions. Held-out evaluation crosses training labels with all three outcomes, measuring outcome concentration above the 97th risk percentile and racial composition of that group. Predictive usefulness against a convenient label does not settle allocation suitability.

**Interpretation for PERSONA:** This directly precedes the proposed train-target-by-evaluation-target comparison at matched selection size. PERSONA's distinction is binary concern recovery in chatbot review queues, with an additional contextual judgment endpoint, rather than clinical outcome concentration and racial allocation. Do not claim discovery of cross-target allocation auditing or infer analogous racial harm from PERSONA's categories. Table 2 is on printed page 452 (PDF page 6).

**Bibliography status:** Not present in the inspected bibliography.

### 2. Jacobs and Wallach (2021): construct validity, not label accuracy alone

**Measurement and Fairness.** FAccT 2021, 375-385. [Publisher/DOI](https://doi.org/10.1145/3442188.3445901); [author manuscript](https://arxiv.org/pdf/1912.05511).

**Supported argument:** Section 3 separates reliability from validity and distinguishes content, convergent, discriminant, predictive, hypothesis, and consequential validity. Convergent validity concerns measures of the same construct; consequential validity considers consequences of using measurements.

**Interpretation for PERSONA:** Cross-criterion screening performance can interrogate an intended use, but does not itself validate D, F, OA, or reviewworthiness. Those are not established interchangeable measures of one construct. Low off-diagonal recall is not automatically a failed validity test, and strong recall against separately collected judgments is not demonstrated consequential validity. Reviewer actions and experienced outcomes remain unobserved. Describe the experiment as evidence relevant to a use-validity argument, not a new validity coefficient or completed validation.

**Bibliography status:** Already present as `jacobs2021measurement`.

### 3. Passi and Barocas (2019): target choice is a substantive decision

**Problem Formulation and Fairness.** FAT* 2019. [Publisher/DOI](https://doi.org/10.1145/3287560.3287567); [author manuscript](https://arxiv.org/pdf/1901.02547).

**Supported argument:** Drawing on six months of ethnographic fieldwork with a corporate data-science team, the paper examines how objectives become prediction problems and how target variables and proxies are negotiated. Normative questions enter before model fitting, through problem formulation.

**Interpretation for PERSONA:** Choosing broad D, poor fit, or OA concern is not merely changing an interchangeable supervision column. Each specifies what the queue rewards. Holding the pipeline fixed makes that choice inspectable, but cannot determine which criterion an organization or affected community ought to prioritize. Present this as a computational examination informed by problem-formulation scholarship, not a substitute for stakeholder justification or an observed organizational study.

**Bibliography status:** Not present in the inspected bibliography.

### 4. Okati, De, and Gomez-Rodriguez (2021): budgeted triage is established

**Differentiable Learning Under Triage.** NeurIPS 34, 9140-9151. [Official proceedings](https://proceedings.neurips.cc/paper/2021/hash/4c4c937b67cc8d785cea1e42ccea185c-Abstract.html); [paper](https://proceedings.neurips.cc/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf).

**Supported result:** The paper studies joint prediction and triage under limited human involvement. Its optimal triage characterization depends on differences between model and human errors; models optimized for full automation can be suboptimal under triage.

**Interpretation for PERSONA:** Neither limited-capacity allocation nor the distinction between ordinary prediction and triage is new. However, ranking probable concern cases is not the same objective as routing cases where human intervention reduces error most. Without downstream reviewer performance, the proposed study measures selection coverage, not optimal human-machine collaboration or error reduction. Use this work to delimit the endpoint, not to borrow its optimality guarantees.

**Bibliography status:** Already present as `okati2021triage`. The paper PDF identifies the third author as Manuel Gomez-Rodriguez; the proceedings landing page shortens that name.

### 5. Mozannar and Sontag (2020): distinguish screening from learning to defer

**Consistent Estimators for Learning to Defer to an Expert.** ICML, PMLR 119, 7076-7087. [Official proceedings](https://proceedings.mlr.press/v119/mozannar20b.html); [paper](https://proceedings.mlr.press/v119/mozannar20b/mozannar20b.pdf).

**Supported result:** Sections 3-4 formulate a combined model-expert decision system and give a consistent surrogate using expert decisions, learning both a classifier and a rejector.

**Interpretation for PERSONA:** Follow-up reviewworthiness labels are evaluation targets, not observations of what a downstream reviewer would decide after allocation. A top-k concern queue therefore should not be called an evaluated learning-to-defer system. In particular, non-selection does not mean the machine has made a correct negative decision, and selected cases are not assumed to be resolved perfectly. This distinction is essential to avoid turning recall-at-budget into a claim about joint-system accuracy.

**Bibliography status:** Already present as `mozannar2020defer`.

### 6. Alves et al. (2025): concrete alert review and batch-capacity precedent

**A benchmarking framework and dataset for learning to defer in human-AI decision-making.** Scientific Data 12, 506. [Publisher/DOI](https://doi.org/10.1038/s41597-025-04664-y); [publisher PDF](https://www.nature.com/articles/s41597-025-04664-y.pdf).

**Supported contribution:** OpenL2D generates synthetic expert decisions and capacity-limited training/testing scenarios. FiFAR instantiates financial-fraud alert review; the framework explicitly represents batches and expert capacity constraints (Methods; Figure 1). It evaluates deferral systems using decision costs, not simply alert recall.

**Interpretation for PERSONA:** Batch-based capacity constraints and an alert-review framing have direct precedent. The proposed work changes the concern criterion rather than modeling expert allocation and decision costs. Cite this as adjacent infrastructure and evaluation design, not evidence that PERSONA measures actual reviewer workload. FiFAR's generated expert predictions must not be described as a new field study of real reviewers.

**Bibliography status:** Already present as `alves2025openl2d`. The publisher HTML redirected to an inaccessible authentication endpoint during this check; the publisher's full PDF was accessible and inspected.

## What the proposed analysis should make identifiable

These are recommendations for the parent analysis, not claims that the cited papers implement this exact protocol or that the new results already exist.

1. **Separate the two experimental axes.** Within each domain, fit three lexical LR screens with identical features, folds, preprocessing, regularization, and training eligibility, changing only the training target (D, F, OA). If HumT-augmented variants are included, show that as a separate feature-addition comparison, not an unmarked change of model across rows.
2. **Freeze each row's selections before evaluating columns.** Rank each held-out batch once per trained screen and choose exactly the same k for every screen. Evaluate that unchanged selection against D, F, OA, and, in MH only, contextual reviewworthiness. A row's selected responses must not change when the evaluation column changes. The MH endpoint should be evaluation-only in this design, not used for hyperparameter or training-target selection.
3. **Match the actual budget, not just its nominal percentage.** Keep prompt clusters together; use identical test batches and tie rules. The inspected manuscript's five-fold analysis floors quotas to 130 MH slots, whereas its full-domain 20% queue uses 132. Recompute fixed baselines and reviewworthiness coverage under the new batches; do not transplant full-queue counts into a held-out table. Do not pool probabilities from different fold-specific fits into one queue without a separately justified design.
4. **Compare rows within an evaluation column.** Report caught/total positives, recall, precision, remaining positives, and supporting prompt counts. A useful contrast is recall on target t for the screen trained on s minus recall on t for the screen trained on t, at equal capacity. This need not be negative: a target-matched fitted model is a comparator, not an oracle or upper bound. The MH evaluation-only column has no trained-on-MH diagonal comparator.
5. **Retain the random reference and feasibility ceiling.** For batch b with n_b cases and P_bt positives for target t, expected random catches are k_b P_bt / n_b. Sum catches and denominators before pooled recall. The capacity ceiling is sum_b min(k_b, P_bt) / sum_b P_bt. Unequal prevalence and thresholds make unqualified comparisons of recall levels across columns misleading; zero-positive recall remains undefined.
6. **Carry the dependence through uncertainty.** Pair screens on the same prompt-cluster resamples and refit their scalers/models if estimating uncertainty for the training procedure. Document single-class training fallback and sparse/undefined replicates. Fold sensitivity is not independent replication. Any widened family of contrasts remains exploratory unless a justified multiplicity plan is specified; a zero-crossing interval does not establish equivalence.
7. **Keep the inferential scope narrow.** Fixed features control one modeling choice, not label prevalence, annotation noise, rubric overlap, threshold severity, or model misspecification. A changed ranking can establish sensitivity to target choice in this pipeline, not a causal explanation of stakeholder judgments or intrinsic construct separability. Equal review slots also do not equal equal annotation cost or reviewer minutes.

For the separately assessed MH endpoint, report its overlap with each original criterion and preserve assessor/disagreement provenance. "Separate assessment" is safer than "independent validation": existing responses, study framing, and researcher involvement still matter. Do not use the extra column as an authoritative resolution of which original target is correct.

## Cautious positioning language

Proposed framing, conditional on implementing and reporting the complete comparison:

> Building on research on measurement, problem formulation, and selective human involvement, we conduct an exploratory audit of criterion transfer in budgeted chatbot review. We hold the lexical logistic-regression pipeline and held-out review capacity fixed, vary the concern label used for training, and evaluate each resulting queue against all original criteria and a separately assessed mental-health reviewworthiness endpoint. The contribution is evidence about the suitability and limits of reusing a screen for a different review purpose in this corpus, rather than a new learning algorithm or validated harm detector.

This framing draws on the six sources above; the experimental specification and scope restriction are this note's synthesis. Preserve the original analysis chronology rather than retrospectively calling the extension preregistered.

Avoid claims that this is the first cross-criterion allocation study; that D, F, OA, and contextual reviewworthiness are equivalent gold standards; that failure to transfer proves a construct invalid; or that the most successful column identifies the ethically correct criterion. Do not assume a reversal or a useful transfer effect before seeing the estimates. A plausible null finding is that this feature-restricted screen yields uncertain differences.

## Official FAccT 2027 guidance checked today

Primary policy sources: [2027 Author Guide](https://facctconference.org/2027/authorguide.html), marked updated August 2026; [2027 Call for Papers](https://facctconference.org/2027/cfp.html). These are 2027 pages, not inherited 2026 guidance.

- **Format:** Single-column anonymous review. The guide specifies `\documentclass[manuscript,screen,review,anonymous]{acmart}`. The inspected `main.tex` already uses that declaration; this is not a compiled-layout audit. [Formatting instructions](https://facctconference.org/2027/authorguide.html).
- **Length:** Initial content limit is 14 pages including figures/tables, with unlimited references; one additional page is reserved for endmatter, not extra results. Revision-stage and accepted papers receive one additional content page. [CFP](https://facctconference.org/2027/cfp.html).
- **Endmatter/anonymity:** A Generative AI Usage Statement is required at submission, including non-use or tool/task disclosure. Omit identifying contribution, acknowledgement, competing-interest, and positionality sections. Method limitations belong in the body. [Author guide](https://facctconference.org/2027/authorguide.html).
- **Appendices/references:** Appendices belong at the end of the same PDF; the main paper must stand alone and appendix review is optional. Archival submissions use ACM reference format. Do not hide essential transfer evidence in appendices. [Author guide](https://facctconference.org/2027/authorguide.html).
- **Dates:** Abstract October 27, 2026; paper November 3, 2026; both 23:59 Anywhere on Earth. Registration status was not checked. [CFP](https://facctconference.org/2027/cfp.html).

## Scope of this handoff

Only this Markdown note was authored. No manuscript, bibliography, analysis, or source-data changes were made for this task. No inference about acceptance, exhaustive novelty, completed criterion-transfer results, or submission readiness follows from this check.
