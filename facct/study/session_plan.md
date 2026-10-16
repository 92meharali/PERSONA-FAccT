# External-evaluator session plan v1.1

Status: prepared, not approved, recruited or conducted. The user confirmed that 2-3 independent practitioners per domain are feasible. Plan six participants initially (two per domain), with a third per domain if available within the agreed collection window. Decide the collection end date before recruitment; do not extend or stop based on favorable feedback. Do not claim saturation or representative coverage.

This dated operational addendum follows protocol v1.0; it does not replace the frozen computational specification. The case-subset and presentation rules here were chosen after computational results were known and are exploratory. No participant outcomes were available. If timing/content changes after a rehearsal or interview, retain the original packet and record the amendment and exposure history.

## Who to recruit

| Domain | Relevant experience to screen for | Target |
|---|---|---:|
| Mental health | Psychology/mental-health practice, supervision, or evaluation of support content; verify the role without inferring a clinical license | 2-3 |
| General health | Medical/health practice or review of health information and advice; record the actual role and review responsibilities | 2-3 |
| Education | Teaching, tutoring, curriculum or educational-content evaluation; record actual responsibilities | 2-3 |

Prior AI auditing is not a requirement. Record firsthand AI-review experience separately from domain expertise; an imagined workflow is not evidence of adoption. No original authors, rubric developers, annotators or involved research interns qualify as external participants. Record prior exposure, collaboration, supervisory relationships and conflicts privately. Prefer people without a dependent relationship to the recruiting researcher; any exception requires institutional review and explicit reporting.

## What the study can establish

- Whether these practitioners recognize a plausible review task and its constraints.
- Which criteria they would dispute and the reasons for that dispute.
- How they interpret counts, uncertainty and non-selection on the proposed card.
- What they would need to challenge or escalate a decision.

It cannot establish reduced harm, representative acceptance, calibrated risk, measured operational effectiveness or generalizable differences between policies. The same people provide formative input and later artifact critique; call this informed usability/criterion feedback, not independent confirmatory validation of the revised artifact.

## Sixty-minute running order

| Minutes | Activity | What is visible | Record |
|---|---|---|---|
| 0-5 | Confirm approved consent, recording choice, sensitive-content warning and right to skip/stop | Consent and purpose only | Private consent record; session code |
| 5-13 | Actual work, constraints and review concerns; ask open questions before construct definitions | No study performance, thresholds or policy names | Firsthand versus hypothetical use, stakeholder/cost account |
| 13-21 | Two label-blind orientation cases; then discuss construct definitions without numeric anchors | Part 1 only | Unprompted criteria, disagreements, missing context |
| 21-22 | Lock initial notes with timestamp; do not retrospectively rewrite them | No results | Formative-note lock |
| 22-38 | Six diagnostic cases, one at a time; ask for review decision, reason and uncertainty | Part 2 only; no scores, model metadata or selection status | Per-case explanation; skipped/incomplete items |
| 38-39 | Lock blind-case notes | No results | Blind-note lock |
| 39-52 | Reveal the matched-budget evidence panels in the assigned order; teach-back before explanation | Part 3 only now | Initial answers, prompts and later corrections kept separate |
| 52-57 | Challenge/appeal scenario, missing perspectives and reasons not to use the workflow | Proposed contestation process | Feasibility objections and negative cases |
| 57-60 | Debrief, optional corrections and withdrawal procedure | Explain proposed workflow and limits | Corrections, with time and stage |

Eight cases is a preparation target, not a speed test. At minute 38 stop the blind-case block and record cases not reached; do not rush or fill missing answers. Rotate case order as specified in the packet guide. Pilot timing internally using researcher rehearsal only, not invented participant feedback. If an external pilot is conducted, it needs the same ethics/consent protections and is reported separately from later sessions where the protocol changed.

## Case and presentation rules

Two orientation cases are sampled by a frozen seeded hash from the complete domain corpus without accessing ratings, H, or policy status. They are not selected to be benign or representative; provide the content warning and preserve the draw. Six diagnostic cases come from the existing systematic sample, maximizing coverage of its predeclared criterion/status and policy/status cells with deterministic tie-breaking. The coordinator register records cells not covered by six cases. No claim is made that every cell is shown or that this sample estimates prevalence.

Orientation/diagnostic overlap is possible because the orientation draw is label-independent. Keep a repeated case at its assigned slot, mark it as previously seen for analysis and do not treat it as an independent first exposure. Do not silently replace it based on scores. Participant-visible text is preserved verbatim; only external metadata are withheld. The coordinator flags model-related strings for human blinding review; removal of metadata cannot guarantee that identity is absent from the text itself.

Generate packets with `python -m facct.study.prepare_materials`. Each domain has separate orientation, blind-case and evidence files to prevent accidental early reveal. The facilitator answer key is not a participant response file. Planned slots are not enrolled people. Actual consent/identity/session records stay outside the repository.

Evidence panels show all three criteria, all three deterministic policies, and the uniform-random expectation at the same 20% capacity. Do not show only HumT's best comparison. Policy order rotates across three sequences; criterion order rotates independently by planned domain/slot. This is partial order balancing, not a powered experiment or full carryover counterbalance. No inference about causal policy preference follows from the order schedule.

## Data and coding decisions

Use private pseudonymous session codes; never commit filled session notes. Capture exact statements when feasible, with notes versus recording clearly distinguished. A comprehension task is coded as accurate, partially accurate, inaccurate, uncertain, or not answered; this is a descriptive categorization, not a validated psychometric score. Criterion disagreement is not a comprehension error. Preserve initial answers before any explanation and label prompted corrections.

Two humans independently code all externally conducted pilot transcripts and at least ceil(25% of remaining transcripts), with at least two remaining transcripts when available. If this subset omits a represented domain, add one transcript from that domain. Select within domain by enrollment order before inspecting content. Preserve independent codes, disagreements and later consensus. AI cannot substitute for either coder or provide participant responses.

Before any claims, report planned/enrolled/completed/withdrawn counts, protocol versions, role descriptions, missing cases, prompted versus initial responses and dissent. Quote only with approved consent and de-identification. Report costs as participant accounts or assumptions, not measured workload unless timing was actually collected and its limitations described.

## Launch gates

Use launch_checklist.md. No recruitment or external session starts until ethics scope, consent fields, data storage, compensation, named responsible humans and author authorization are complete. Venue eligibility is a separate unresolved gate; this protocol is not publication clearance.
