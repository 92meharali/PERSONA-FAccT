# Capability Study Readiness

As of 23 October 2026: documentation specimen only. **Not ready for recruitment, assessment, confirmatory evaluation, or claims of completed research.** No actual ratings or held-out outcomes have been collected for this proposed study in these documents. Existing PERSONA approvals, assessors, labels, or capability notes are not assumed to authorize or validate it.

## Preparation Versus Study Completion

The adjacent scaffold and preparation directory now exist. The recorded preparation is a deterministic, label-blind sample of 60 existing mental-health responses, one per prompt, with a manifest. It is separate from the proposed purposive 60-base diagnostic pilot and supplies neither capability evidence nor new labels. The evaluator consumes externally supplied assessments and scores; it does not run an LLM or collect human judgments.

Verification on 23 October: 11 capability-scaffold unit tests and 27 package/existing-screening tests passed (38 total); the saved manuscript compiled successfully. An independent check also verified 144 existing ranked operating points and unchanged source hashes. These concern implementation and typesetting, not ethics coverage, empirical validation, recruitment, completed screening, or study completion. No actual LLM screening runs or human annotations are reported for the proposed study.

## Document Set

- `protocol.md`: scope, fixed-text design, sampling, assignment, budgets, paired analysis, and limitations.
- `assessor_guide.md`: independent interpretation, support, reviewworthiness, uncertainty, and packet-issue reporting.
- `evidence_dossier_template.md`: factual provenance and separation of capability, permission, access, and performed action.
- `screening_prompts.md`: shared-judge specimens, metadata ablations, failure handling, and explicit-claim comparator specification.
- `readiness.md`: gates and outstanding decisions; this checklist is not an ethics determination or study registration.

## Blocking Gates

| Gate | Current status | Required before proceeding |
| --- | --- | --- |
| Ethics coverage of this proposed study | UNCONFIRMED | Written institutional approval/amendment or documented applicable determination covering fixed-text variants, new assessors, sensitive material, data handling, and automated screening |
| Consent and participant information | PENDING | Approved consent, withdrawal limits, use of judgments, confidentiality, breaks/skips, and contact procedures |
| Recruitment and qualifications | PENDING | Eligibility, independence/conflicts, qualifications appropriate to the review remit, recruitment method, and balanced assignment feasibility |
| Staffing | PENDING | At least six eligible independent assessors for two variants with three judgments each; no assessor sees twins or related scenario variants |
| Compensation and power relationships | PENDING | Payment, workload, skip/withdrawal protections, and safeguards against supervisory pressure |
| Distress and safeguarding process | PENDING | Approved handling of sensitive content, breaks, reporting, and escalation contacts; no clinical-care promises |
| Data rights and privacy | PENDING | Provenance, reuse permission, redaction, storage/access/retention, and permission for any external model-provider processing |
| Operational configurations | UNVERIFIED | Scoped memory-present and memory-absent evidence, permission/access documentation, tests and limitations for both arms |
| Follow-up capability family | OPTIONAL / UNFROZEN | Separate secondary sample and evidence plan; authorized sandbox scheduling and action/delivery distinctions |
| Existing-text relevance sample | PREPARED, UNASSESSED | Keep the deterministic 60-response mental-health sample and manifest separate from the diagnostic pilot; verify reuse rights and exposure before use |
| Diagnostic pilot inventory | PENDING | Frozen text, scenario grouping, ordinary functional and invariant controls, selection/exclusion log without selecting on flips |
| Assignment schedule | NOT CREATED | Randomized balanced incomplete assignment, no twins/near-duplicates per assessor, common guide and packet version |
| Screening implementation | PROMPTS SPECIFIED; NO JUDGE RUNS | Same pinned judge across conditions, outcome-blind evidence projections, caching, failures and simple rule comparator; API integration remains separate |
| Analysis implementation | SCAFFOLD PRESENT; NO STUDY RESULTS | Confirm final conformance for exact floor budgets, 2,000 paired scenario replicates, undefined-replicate disclosure, U bounds, ties, rater sensitivity and costs |
| Final-study sample size | UNDECIDED | Pilot-informed useful-effect and precision/power justification; no treating 60 bases as a powered final study |

Scaffold presence is not end-to-end study readiness. No runnable study-input set, judge API integration, capability harness, or staffing availability is implied by these documents. The bootstrap computes percentiles of finite replicates and reports undefined counts and interval status: any resulting conditional interval must be disclosed as such under the protocol, not presented as an unconditional 95% interval when undefined replicates occur.

## Freeze Checklist: Before Pilot Collection

- [ ] All ethics, consent, participant protection, data-use, and recruitment gates cleared with references and accountable owner.
- [ ] Primary memory scope and secondary follow-up boundary agreed.
- [ ] Purposive 60-base diagnostic inventory selected without label or score inspection; enrichment disclosed; distinct from the prepared 60-response relevance sample.
- [ ] 20 development / 40 exploratory held-out base split fixed by scenario cluster; no twins/paraphrases cross splits.
- [ ] Evidence schema and operational verification completed; unknown not substituted for absent.
- [ ] All assessor packet identifiers opaque; guide/version uniform within phase.
- [ ] At least six eligible assessors confirmed; three independent judgments per instance; balanced configuration exposure and no within-assessor scenario duplicates.
- [ ] Initial vote aggregation and unresolved/skip handling frozen.
- [ ] Pilot explicitly described as exploratory, not powered confirmation.

## Freeze Checklist: Before Held-Out Screening

- [ ] Shared judge instruction, pinned model, decoding, score scale, token limits, projections, failure convention, and tie order frozen.
- [ ] Development-only edits complete; no evaluator tuning on held-out ratings.
- [ ] Capability-summary, full-evidence, missing, irrelevant, and prompt-response inputs checked for leakage.
- [ ] Exact simple-rule vocabulary, negation, temporal scope, and extraction behavior frozen and inspectable.
- [ ] Primary budget floor(0.20 * n); secondary floor(0.05 * n), floor(0.10 * n), floor(0.30 * n).
- [ ] One primary descriptive paired contrast: `semantic_full_evidence` minus `semantic_text` recall at 20% in the mixed memory diagnostic queue; within-configuration and other comparisons secondary exploratory; intervals pointwise.
- [ ] U labels remain in queues; definite-label metrics and identification bounds disclosed; `primary` and `label_conditional` output fields not represented as confirmatory status.
- [ ] Scenario bootstrap details, seed, 2,000 final replicates, percentile convention, undefined cases, and rater sensitivity frozen.
- [ ] Evidence preparation, screening, and assessor time/cost collection specified.
- [ ] Entire evaluation queue retained, including unresolved human labels and screening failures; no outcome-dependent omissions.

For a future confirmatory phase, additionally freeze a new untouched sample, size justification, useful effect, stopping rule, and deviation handling before collection. No confirmatory sample has been selected or collected here. Any formal minimum-context claim also needs prespecified noninferiority/error margins and adequate precision; these are not currently set.

## Decision and Deviation Record Template

Date: [pending]

Phase and specification version: [pending]

Decision or deviation: [pending]

Reason and affected scenarios/conditions: [pending]

Were held-out labels or results already visible? [yes/no; describe]

Authorized owner and ethics implications: [pending]

Disposition: [prospective amendment / restart affected ratings / exploratory-only / stop]

## Stop or Narrow the Claim

Stop collection if ethics, permission, packet validity, or participant protections are unresolved. Stop calling an analysis confirmatory if held-out outcomes influenced its specification. Do not force label flips or recruit replacement judgments to improve agreement.

If gains reduce to explicit factual contradictions, describe a conformance test. If metadata does not improve useful allocation, or harms invariant-control performance, report that result. Sparse positives and wide intervals do not demonstrate equivalence. Any eventual result is offline review allocation, not evidence that review, remediation, or deployment safety improved.

## Change Boundary

These five study documents accompany the manuscript integration, candidate preparation and tested offline scaffold. They do not certify actual capability evidence or human judgments. No publication, recruitment, commit or push was performed in this revision. See the implementation record for the complete change scope.
