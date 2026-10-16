# Evidence-bounded manuscript outline

## Current consolidated outline (2 October 2026)

The authoritative draft is [overleaf/main.tex](overleaf/main.tex), titled **When
Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization**.
The earlier design below is retained as history, not an active study commitment.

1. Introduction: proposed evaluator-managed batch review and three empirical questions.
2. Related work: existing tone measures, measurement/use reasoning, capacity-aware
   triage and documentation. Do not claim these methods or principles are new.
3. Corpus and criteria: complete CHI resource reuse, source rater account, broad D
   meaning, fit/OA endpoints, and available-text provenance limitations.
4. Methods: exact quotas, fixed rules, grouped trained comparison, paired uncertainty
   and explicit post-exploration amendment history.
5. Results: comparative allocation; incremental benefit; common-queue distribution.
6. Decision accounting: retrospective workload and a concrete supporting report,
   not independent evaluation or a proven governance intervention.
7. Discussion, limitations and conclusion: bounded empirical lesson, no semantic-
   evaluator competitiveness or harm-outcome claims.
8. Ethics/AI/reproducibility endmatter; complete tables and diagnostics in appendices.

No participant study is part of this draft. Its scholarly value and submission
eligibility are author decisions, not consequences of successful code tests.

## Historical design (superseded)

Working title: **From Tone Scores to Review Decisions: Auditing HumT-Based Screening of Anthropomorphic AI Responses**

Status: methods-study candidate, not a submission-ready manuscript. An outline is intentional: the computational evidence is available, but workflow plausibility, external evaluation and substantial-overlap clearance remain unresolved. Do not turn pending sections into past-tense results. No full-paper compilation is claimed.

Current reporting scope: the author has deferred external participation and agent experiments. The [computational review draft](generated/computational_review_draft.md) supersedes the conditional external-study section below for current writing; retain this outline as the earlier design record. No additional human evidence is promised.

## Candidate contribution

A reproducible offline evaluation of a specified review-allocation procedure, with exact budgets, feasible baselines, criterion sensitivity and workload reporting. The proposed audit-use card makes assumptions and unresolved criteria visible. Independent practical value beyond CHI is still to be demonstrated, not presumed.

## 1. Problem and decision (about 1 page)

Define the evaluator, batch, response-level review slot, review action and meaning of non-selection. Describe HumT screening as a proposed simulation. Motivate the cost of incomplete review without claiming organizations already use HumT this way. Central question: what criterion-specific opportunities for detection do different allocations provide at matched capacity?

Distinguish tone measurement, judged appropriateness, review allocation, achieved detection and downstream harm. Human-likeness is not inherently wrong; a valid tone measure need not be a sufficient review policy. New work must go beyond merely repeating that observation.

## 2. Measurement-use validity and related work (about 1.5 pages)

Use verified references only; metadata and support limits are in the literature memo. HumT/DumT provides the score, DeVrio's taxonomy provides descriptive linguistic distinctions, and Dehumanizing Machines already recognizes contextual intervention tradeoffs. Jacobs/Wallach and Hutchinson et al. ground operationalization/use distinctions; Raji et al. and Lam et al. delimit what constitutes a broader audit. Related FAccT work distinguishes output cues from observed reliance or longer-term parasociality.

Do not describe D/F/OA as validated harm instruments, claim a first-ever gap from a targeted review, or attribute safety-calibration claims to HumT's authors.

## 3. Existing corpus and criteria (about 1.5 pages)

Disclose complete reuse of the CHI resource: 1,490 responses, 499 prompt clusters, three domains and three endpoints. Group A supplies OA, Group B E/D/F. Group B includes authors/interns; separation of streams does not establish external independence. Rater identifiers are anonymous and domain-scoped. The final supplement's explicit separate-pool and compensation account is now the reporting basis; see [provenance resolution](../submission/provenance_resolution.md). It is not an independent identity/payroll audit.

Specify D >= 3 as a broad review trigger, with ordinary sympathy in its anchor. F < 4 and OA < 4 are different constructs/thresholds, not equivalent harms. Show criterion counts and supporting prompt counts; mark education D and health OA sparsity. Explain inferred prompt/model metadata and full/prefix/fuzzy HumT joins, plus sensitivity rather than quiet exclusions.

## 4. Allocation procedure (about 2 pages)

Fixed capacity floor(n*b), budgets 5/10/20/30%, deterministic score ties, high-H/length/marker baselines, analytical exact-budget uniform and proportional domain-stratified random. No labels are inputs to deployable policies. No model tuning or learned weights. AP/AUC are tied-score metrics, not operating-point guarantees.

2,000 paired prompt-cluster resamples; re-rank fresh resampled batches. State finite/undefined counts, pointwise intervals, limited primary comparison family and sparse-cell rules. Include workload targets and cost assumptions. Explain that old corpus exploration prevents confirmatory preregistration claims.

## 5. Results and sensitivity (about 2.5 pages)

Generate every number from `screening.csv` and associated sensitivity tables. Lead with both useful enrichment and limitations, including simple alternatives that outperform HumT. Avoid pooled-only conclusions.

- Figure 1: recall versus exact review capacity, by criterion/domain; counts and HumT intervals. Caption must say other policy intervals are in tables.
- Figure 2: selected versus unreviewed concern counts at the reference budget, not "safe versus harmful".
- Table 1: counts, prevalence, concern clusters, caught/missed, precision/recall and matched-random differences.
- Table 2: paired differences versus length/markers; distinguish shared lexical cues in D's rubric from independently established harm detection.
- Table 3 or appendix: thresholds/consensus, tie and join sensitivity, AP/AUC, workload, model pairings on complete prompts.

Low criterion overlap alone is not normative disagreement; include exact joint counts and continuous relationships. Natural/adversarial comparisons are observational, and source/rater/domain distributions are confounded. Three endpoints do not support model-family rankings.

## 6. External evidence (conditional, about 1.5 pages)

**Not conducted.** If completed with approval, report actual participants, protocol, disagreements, comprehension errors, negative cases and limitations. Do not present a formative-then-informed critique as independent confirmatory validation. If unavailable, omit completed-study language and narrow the paper to a simulation/methods contribution. Whether that is sufficient for FAccT is unresolved.

## 7. Audit-use card, discussion and boundaries (about 2 pages)

Show the proposed artifact, criterion owner, what reviewers inspect, contestation/escalation path and residual uncertainties. Claim proposal, not proven accountability improvement. Discuss time-cost differences, target-cue overlap for marker baselines, normative criteria, Group B expectations, text joins, fixed corpus mixture and absent user outcomes.

## Endmatter and submission

Current official guide specifies single-column anonymous acmart, 14 content pages plus one endmatter-only page, references excluded and appendices in the same PDF. Recheck before typesetting. Include accurate ethics and generative-AI-use statements. AI assisted preparation/code/document drafting; it did not supply participant responses, independent human coding or modified ratings. Authors must review the actual contribution disclosure and verify all citations.

Use the confidential venue procedure for related CHI work; a public identifying repository link is not anonymous disclosure. Do not copy the CHI predictive/ablation tables as this paper's main result. No manuscript should claim eligibility or external validation on the basis of this outline.
