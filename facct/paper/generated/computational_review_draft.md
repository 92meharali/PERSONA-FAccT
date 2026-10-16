# From Tone Scores to Review Decisions: Auditing HumT-Based Screening of Anthropomorphic AI Responses

**Internal computational-study draft, not submission-ready.** No new human study or AI-agent evaluation was conducted. All numerical tables and result sentences marked by the generation process come from the frozen computational outputs. This draft does not establish concurrent-submission eligibility. Read the author checks at the end before sharing externally.

## Abstract

Automated human-like-tone scores describe linguistic style, but their usefulness for allocating limited manual review depends on the review criterion. We evaluate a proposed screening procedure on PERSONA's existing multi-domain response corpus. Policies prioritize high HumT, response length or a fixed pronoun/conversational-marker score, alongside matched-capacity random controls. Evaluation covers exact review budgets, separately defined anthropomorphic-implication, domain-fit and holistic-appropriateness criteria, and prompt-cluster uncertainty. Results show criterion-specific enrichment rather than uniform utility: HumT can improve over random selection while remaining weaker than a simple marker baseline. Stricter concern definitions yield substantially different coverage and sparse supporting cases. The study contributes an explicit allocation evaluation and reporting proposal, not evidence of experienced harm or successful organizational adoption. All data and human ratings are reused from related CHI work; independent scholarly distinctness and submission eligibility require assessment.

## 1. Introduction and research questions

A reviewer with capacity to inspect only part of an AI-response batch must choose which responses enter the queue. A linguistic measure may be useful for this decision without measuring the review target directly. Conversely, a score's relationship with human judgments does not establish that ranking by it is the best use of a constrained review budget. The relevant question concerns opportunities to inspect criterion-defined cases, not whether tone itself is desirable or undesirable.

We study a proposed offline workflow: rank a fixed batch, select an exact number of responses and assess which existing rubric-defined concerns appear in that selection. A qualified reviewer would subsequently examine the original prompt and response, but that downstream action is not observed here. Non-selection means unreviewed, not cleared. We have not established organizational deployment of HumT screening.

- **RQ1:** At fixed review capacities, how does high-H selection compare with uniform random selection and transparent observable baselines for each concern criterion within each domain?
- **RQ2:** How do coverage and residual unreviewed concerns change under alternative rubric anchors, rater-consensus rules and contexts?
- **RQ3:** What workload and reporting implications follow from the observed allocation tradeoffs, without assuming that non-selection establishes safety?

RQ3 concerns computed workload and an explicitly unevaluated reporting proposal, not practitioner acceptance. The related CHI manuscript asks about H's sufficiency for OA prediction and the contributions of E/D/F using regression, grouped cross-validation and ablation. This draft uses the same corpus and ratings but changes the decision estimand to constrained review allocation. That distinction is substantive enough to investigate, not automatic proof of publication novelty.

## 2. Related work and scope of inference

HumT DumT develops measurement and control of human-like language; it does not establish that its score is a calibrated harm probability or a validated organizational review policy. Our use is a proposed downstream allocation procedure, not a correction to an alleged safety-calibration claim by its authors. [Cheng, Yu and Jurafsky, 2025](https://aclanthology.org/2025.acl-long.1261/)

DeVrio and colleagues' taxonomy distinguishes linguistic expressions contributing to anthropomorphism. It supplies descriptive conceptual resources, not validated equivalences between taxonomy categories and PERSONA's numerical ratings. Dehumanizing Machines already recognizes contextual tradeoffs in changing anthropomorphic expressions; merely observing that context matters is therefore not our new contribution. [DeVrio et al., 2025](https://doi.org/10.1145/3706598.3714038), [Cheng et al., 2025](https://aclanthology.org/2025.acl-long.1259/)

Measurement and Fairness motivates explicit links between constructs and operationalizations; Evaluation Gaps distinguishes evaluation oriented toward model performance from evaluation grounded in applications. We apply these distinctions to a specified selection decision while treating the human criteria themselves as contestable judgments. [Jacobs and Wallach, 2021](https://doi.org/10.1145/3442188.3445901), [Hutchinson et al., 2022](https://facctconference.org/static/pdfs_2022/facct22-3533233.pdf)

Internal auditing and assurance-audit frameworks involve scoping, normative criteria, verification and reporting beyond one offline calculation. Our simulation is a component-level investigation, not a demonstrated end-to-end audit program. [Raji et al., 2020](https://arxiv.org/abs/2001.00973), [Lam et al., 2024](https://doi.org/10.1145/3630106.3658957)

The primary-source memo records the search scope, closest related anthropomorphism studies and limits of each citation. We do not claim the first study of context-sensitive evaluation or infer novelty from the absence of our exact experiment in a targeted literature review.

## 3. Existing resource and concern criteria

The released corpus contains 1,490 responses in 499 domain-scoped prompt clusters.

| Domain | Responses | Prompt clusters |
| --- | --- | --- |
| Education | 415 | 139 |
| General health | 415 | 140 |
| Mental health | 660 | 220 |

These are final analytical counts, not a reconstruction of the original collection size. Every stored E/D/F/OA mean reconstructs from five released ratings. The processed files are byte-identical to the repository's submission-supplement snapshot, and checked CHI headline figures are numerically consistent. These checks cannot authenticate which files were uploaded to the conference portal.

The source study documents 20 raters in non-overlapping pools: three domain-specific five-person Group A pools supplied OA, and a separate five-person Group B supplied E/D/F across domains. Group B included authors and research interns familiar with the framework. The final protocol application note explicitly explains that phase labels distinguish instruments rather than shared personnel, and that the same-rater fallback was not used. Its ethics record reports informed consent, voluntary withdrawal rights and compensation through existing grant-supported research roles rather than a separate per-response payment scheme. Voluntary participation and compensation are compatible. This account follows the final documented design; the present reuse analysis is not an independent identity, consent or payroll audit. We describe documented domain-relevant training rather than infer unverified clinical licenses.

H is the recorded automated HumT score. Higher D denotes greater anthropomorphic-implication concern; higher F and OA denote better fit and holistic appropriateness. The primary candidate trigger is mean D >= 3, whose rubric anchor includes simulated affect or understanding, including ordinary sympathy. This is a broad review trigger, not proof of deceptive intent or experienced deception. Secondary criteria F < 4 and OA < 4 identify responses below strong fit and mostly appropriate, respectively. Applying ordinal anchors to a mean is an operational choice; the three thresholds do not establish equivalent severity.

Education and general-health prompt identifiers are reconstructed from prompt text and model attribution comes from HumT source files; mental-health metadata are native. Some HumT joins use prefixes or fuzzy matching. Main results retain all released rows; a separate full-text/embedded-only sensitivity changes the analyzed batch rather than quietly removing difficult cases.

## 4. Methods

The review unit is a response. Primary analyses use separate domain batches; pooled results are secondary because mixtures can alter performance. Capacity is floor(n*b), for budgets of 5%, 10%, 20% and 30%. The 20% reference was already explored, not optimized in this analysis. High-H ranks descending recorded H. Length ranks descending regex word count. Markers ranks by the proportion of tokens in a fixed first/second-person and conversational-marker dictionary. The dictionary is transparent but not a separately validated anthropomorphism metric. No human outcome rating enters these policies, and no model is fitted.

Uniform random selection is evaluated analytically at exactly the same capacity, not using one fortunate or unfortunate draw. Pooled stratified random selection allocates slots proportionally by domain with largest-remainder rounding. SHA256-based seeded ordering resolves score ties without exceeding capacity; a 100-seed analysis checks sensitivity. Average precision and ROC-AUC retain tied-score groups and were checked against scikit-learn. A positive-class-free sample has undefined recall and AP; ROC-AUC needs both classes.

Outcomes include selected concern counts, recall, precision, missed concern counts, prevalence among unreviewed responses, ranking summaries and workload to reach target recall. Workload is a retrospective ranking prefix, not a calibrated deployment stopping rule. Equal response capacity is not equal review time. Time and error-cost scenarios are stated assumptions rather than empirically estimated preferences.

We use 2,000 paired prompt-cluster bootstrap draws, re-ranking each resampled batch. All responses to a sampled prompt remain together; pooled draws are stratified by domain. Repeated cluster copies receive distinct occurrence keys for tie handling. Intervals estimate a resampled-batch procedure, not performance of a fixed learned threshold. Undefined draws remain undefined and finite counts are reported. Bootstrap intervals condition on released ratings; rater uncertainty is explored separately.

The specified primary family comprises three domain-specific high-H minus expected-random recall differences for D >= 3 at 20%, with Bonferroni 98.3333% percentile intervals. Other intervals are exploratory pointwise 95%, not simultaneous comparisons. Fewer than ten concern-bearing or nonconcern-bearing prompts triggers a sparse-evidence flag. The full corpus and earlier cutoffs were already inspected; the specification is prospective for this computation but is not a preregistration on unseen data.

## 5. Results

### 5.1 Fixed-budget coverage

| Domain | Criterion | Review slots / batch | Cases selected / concern cases | Precision | Recall (95% CI) | Unreviewed concerns |
| --- | --- | --- | --- | --- | --- | --- |
| Mental health | D_ge3 | 132/660 | 42/165 | 31.8% | 25.5% [19.2, 32.1] | 123 |
| Mental health | F_lt4 | 132/660 | 18/95 | 13.6% | 18.9% [12.2, 27.6] | 77 |
| Mental health | OA_lt4 | 132/660 | 31/133 | 23.5% | 23.3% [17.6, 30.6] | 102 |
| Education | D_ge3 | 83/415 | 7/12 | 8.4% | 58.3% [16.7, 90.9] | 5 |
| Education | F_lt4 | 83/415 | 10/25 | 12.0% | 40.0% [18.8, 60.0] | 15 |
| Education | OA_lt4 | 83/415 | 9/18 | 10.8% | 50.0% [23.5, 73.7] | 9 |
| General health | D_ge3 | 83/415 | 10/23 | 12.0% | 43.5% [24.0, 65.2] | 13 |
| General health | F_lt4 | 83/415 | 25/120 | 30.1% | 20.8% [13.6, 27.2] | 95 |
| General health | OA_lt4 | 83/415 | 3/9 | 3.6% | 33.3% [0.0, 70.1] | 6 |

Intervals are pointwise 95%. Uniform-random expected recall is 20% at these exact reference capacities. Expected random counts may be fractional; each real allocation selects an integer number of responses. Sparse education D and general-health OA cells each have only seven concern-bearing prompts.

For the specified D >= 3 primary comparison family, the adjusted 98.3333% intervals are:

- Mental health: HumT minus random recall +5.5 percentage points; adjusted interval [-2.0, +13.8]. Supporting concern-bearing prompts: 99.
- Education: HumT minus random recall +38.3 percentage points; adjusted interval [-19.8, +80.1]. Supporting concern-bearing prompts: 7.
- General health: HumT minus random recall +23.5 percentage points; adjusted interval [+0.1, +50.5]. Supporting concern-bearing prompts: 15.

The general-health adjusted lower endpoint is very close to zero; the percentile interval and its finite Monte Carlo resolution should not be presented as a decisive threshold-independent finding.

This provides bounded evidence of enrichment in some settings, not consistent superiority across criteria. In particular, selecting anthropomorphic tone does not necessarily recover responses judged to lack domain fit. Do not interpret a label outside one criterion as evidence that a response is safe under another criterion.

### 5.2 Simple alternatives

| Domain | Comparator | Cases selected / D cases | Comparator recall | HumT minus comparator recall, pp (95% CI) |
| --- | --- | --- | --- | --- |
| Mental health | length | 54/165 | 32.7% | -7.3 [-14.8, +1.8] |
| Mental health | markers | 63/165 | 38.2% | -12.7 [-21.9, -4.3] |
| Education | length | 3/12 | 25.0% | +33.3 [-11.1, +75.0] |
| Education | markers | 9/12 | 75.0% | -16.7 [-50.0, +16.7] |
| General health | length | 5/23 | 21.7% | +21.7 [+0.0, +47.1] |
| General health | markers | 21/23 | 91.3% | -47.8 [-63.2, -25.9] |

Paired differences, rather than overlapping marginal intervals, support the comparisons. The marker score partly shares linguistic cues with the D rubric. Its stronger D coverage is evidence about matching this criterion, not an independently validated capacity to detect user harm. Its performance does not justify suppressing those expressions by default.

### 5.3 Criterion and provenance sensitivity

- Mental health: at mean D >= 4, high-H selection captures 0/5 cases from 4 concern-bearing prompts. For the full-text/embedded-only D >= 3 sensitivity, 0 rows are excluded and 42/165 cases are selected.
- Education: at mean D >= 4, high-H selection captures 3/8 cases from 5 concern-bearing prompts. For the full-text/embedded-only D >= 3 sensitivity, 56 rows are excluded and 6/12 cases are selected.
- General health: at mean D >= 4, high-H selection captures 2/8 cases from 6 concern-bearing prompts. For the full-text/embedded-only D >= 3 sensitivity, 3 rows are excluded and 10/23 cases are selected.

All stronger-D cells are sparse. Threshold sensitivity is therefore informative about this corpus, not a stable estimate of deployment performance for severe cases. Majority and unanimous rater rules, individual-rater results, exact criterion intersections and continuous relationships are separately reported. Low overlap can arise from prevalence and cut points; it does not itself prove normative disagreement.

Model comparisons use complete three-model prompt sets, with incomplete clusters reported separately. Some apparent rate-order reversals have intervals crossing zero; neither those reversals nor the three endpoints support universal model-family rankings. Condition and scenario analyses are descriptive: natural and adversarial sets are unmatched, while domain, prompt source and rater population vary together.

### 5.4 Workload

| Domain | Policy | Batch fraction needed for 80% D-case recall (95% CI) |
| --- | --- | --- |
| Mental health | high_H | 70.8% [64.1, 77.3] |
| Mental health | length | 66.1% [58.6, 73.8] |
| Mental health | markers | 63.3% [52.9, 71.1] |
| Mental health | uniform_random | 79.6% [79.6, 80.1] |
| Education | high_H | 37.6% [9.2, 83.7] |
| Education | length | 67.7% [29.0, 96.4] |
| Education | markers | 23.9% [9.9, 38.1] |
| Education | uniform_random | 77.1% [66.8, 80.2] |
| General health | high_H | 46.3% [28.5, 61.4] |
| General health | length | 83.4% [70.5, 93.0] |
| General health | markers | 15.2% [9.8, 32.9] |
| General health | uniform_random | 79.4% [75.2, 80.2] |

These workload fractions use the known criterion labels retrospectively. Uniform-random workload is an expected order statistic; a particular random draw need not achieve that target at the expected workload. Observed and equal-domain mixtures and time/cost ratios remain hypothetical deployment scenarios. They are not estimates of actual institutional demand or cost.

## 6. Reporting proposal and discussion

The proposed audit-use card names the decision owner, criterion version, review capacity, tie rule, counts, uncertainty and unsupported inferences. It preserves a route to challenge the criterion, a selected case or a non-selection and proposes retaining disagreements and versioned amendments. Neither usability nor the effectiveness of that process has been evaluated. An affected user should not need a high tone score to raise a concern, but the practical implementation and evaluation of such a process are outside the present evidence.

The contribution is an auditable account of allocation consequences: a score can enrich one broad trigger while offering little advantage for a different criterion, and a transparent low-cost comparator can materially change the interpretation. Low linear predictive R2 does not determine exact-budget recall for thresholded judgments, so these operating-point comparisons are not available directly from CHI's reported prediction tables. Nevertheless, the submitted CHI discussion already connects PERSONA to governance and model auditing. The governance motivation, all empirical responses and judgments, and much of the context-sensitive argument are shared. Workload is a derived view of the same rankings, not an independent experiment. We therefore present this as a computational extension candidate; sufficient independent scholarly value and concurrent-submission eligibility are not established by different metrics or a new title.

## 7. Limitations and ethics

This is observational reuse of a bounded single-turn text corpus. It measures neither experienced deception, longer-term relationships, clinical or educational outcomes, nor actual successful review. The existing dimensions carry rubric and rater-population assumptions, including framework familiarity in Group B. Sparse events, ceiling/floor concentrations, reconstructed metadata and text-based joins constrain generalization. Simple lexical baselines overlap with target cues, and equal item counts ignore potentially different reading times. Bootstrap uncertainty does not validate normative criteria or resolve source-history ambiguities.

No new interviews, practitioner judgments or LLM-judge outputs are included. Prepared external-study materials and suggested agent experiments are deferred. Available research-team experts may inform internal development but cannot be reported as independent validators. The prior annotation study is documented as a sub-study under parent-project institutional approval; scope and reporting must be verified against the actual records rather than inferred from this draft. No new ethics exemption is claimed. Source rights, sensitive-text handling and anonymous release remain author checks.

AI assisted code and document preparation. It did not create participant responses, independent human coding or replacement source ratings. Authors remain responsible for checking code, numerical claims, citations and the final disclosure of actual AI use.

## 8. Conclusion

The completed simulation supports criterion-specific assessment of proposed review allocation rather than a blanket endorsement or rejection of human-like tone. HumT sometimes enriches a review queue, while simple alternatives and stricter criteria change the result. The defensible conclusion concerns opportunities for review under explicit assumptions. Practical effectiveness, independent external validation and publication distinctness remain unestablished.

## Author checks before submission

- Confirm the exact uploaded CHI supplement version if making an authenticated release-history claim. Current analyzed files match every entry in the repository ZIP; the author's recollection of the upload is tentative. The final repository's explicit annotation-design and compensation account is the reporting basis, not an independently audited personnel/payment record.
- Assess the computational-only contribution against the submitted CHI paper, without promising deferred evidence.
- The author will handle chair contact and any confidential disclosure of the shared corpus and judgments; the assistant will not send an inquiry. Record applicable guidance rather than assume permission.
- Resolve rights/anonymity and recheck current venue policy and submission status.
- Typeset and inspect the eventual complete manuscript only after the scope and factual wording are settled. This Markdown review draft has no verified conference page count or compiled PDF.

## Supporting materials

Full numerical outputs and the verified bibliography remain in the computational package. Tables in this document are generated by build_review_tables.py; edit this template, not the generated draft. The new review manifest records source/output hashes and can be checked independently of the unchanged analysis manifest.
