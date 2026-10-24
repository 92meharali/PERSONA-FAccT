# Capability Evidence Dossier Template

Status: unfilled prospective template, draft-2026-10-23. Bracketed fields require completion and verification. This file is not evidence of any deployment, test, permission, action, or ethics approval. Do not insert intended review labels or assessor rationales.

## Coordinator Record: Not Shown to Assessors

| Field | Value |
| --- | --- |
| Scenario cluster / base / instance IDs | [IDs; assessor sees only opaque instance ID] |
| Capability family | [Memory primary / follow-up secondary] |
| Configuration and implementation version | [Exact identifier] |
| Text provenance and rights | [Reused/authored; source; permitted use] |
| Sample role and prior exposure | [Existing-text relevance sample / diagnostic development / diagnostic evaluation; record overlap and exposure] |
| Prompt/response integrity | [Frozen hashes and verification record, once computed] |
| Packet/schema version | [Version shared across both arms] |
| Evidence collection date and validity horizon | [Dates] |
| Evidence preparer / factual verifier | [Roles and conflict declarations] |
| Controlled differences | [Explicit list] |
| Held-constant attributes | [Role, policy, disclosure, prompt, response, relevant task facts] |
| Unexpected confounds / disposition | [None established, or details and exclusion rationale] |
| Ethics/data-use authorization for this study | [Unconfirmed until documented] |

## Assessor-Facing Packet

Instance ID: [opaque ID]

Packet version: [version]

User-visible disclosure and context: [verbatim fixed material; indicate what was and was not shown to the user]

User prompt: [verbatim]

Assistant response: [verbatim, identical across capability variants]

Review remit: potentially misleading operational or relational implications warranting closer human inspection; not a general harm or clinical diagnosis task.

### Neutral Operational Summary

Use the same fields and ordering in every packet. Use `verified present`, `verified absent`, `unknown`, or `not applicable`, always with scope. A plain feature declaration without adequate support remains unknown for operational verification.

| Dimension | Status and scope | Evidence IDs | Limits / unresolved facts |
| --- | --- | --- | --- |
| Current-conversation context availability | [Status] | [IDs] | [Limits] |
| Cross-session persistence mechanism | [Status; storage/retrieval mechanism] | [IDs] | [Limits] |
| Retention horizon and deletion behavior | [Status; time/account boundaries] | [IDs] | [Limits] |
| Permission to store/retrieve for this user | [Status; actual authorization] | [IDs] | [Limits] |
| Relevant record exists and is accessible | [Status; distinguish existence from access] | [IDs] | [Limits] |
| Retrieval for this particular interaction | [Observed / not observed / unknown] | [IDs] | [Limits] |
| Follow-up scheduling capability | [Status] | [IDs] | [Limits] |
| Permission and reachable delivery channel | [Status] | [IDs] | [Limits] |
| Particular job created / accepted | [Status; matching job identifier if safe] | [IDs] | [Limits] |
| Delivery outcome | [Observed / failed / pending / unknown / not applicable] | [IDs] | [Limits] |
| Monitoring or other claimed service | [Status; do not infer from reminders] | [IDs] | [Limits] |

A prospective promise may depend on feasibility and permission; a past-tense completion claim needs action evidence. Leave these distinctions visible. An enabled capability does not authorize its use, and a policy authorizing an action does not implement it.

### Evidence Register

Repeat for each item:

- Evidence ID: [stable ID]
- Source type: [configuration, implementation excerpt, official documentation, permission record, behavioral test, action trace, other]
- Source locator and version: [retrievable provenance; commit/version/date/page as applicable]
- Collector and collection date: [role/date]
- Exact fact supported: [neutral factual proposition]
- Scope: [account, session, environment, feature flag, time, channel]
- Verification method and result: [what was actually checked; no invented tests]
- Negative evidence basis: [explicit disabled state or scoped negative tests; missing logs alone are inadequate]
- Reliability limits / failures / counterevidence: [record unsuccessful tests as well as successes]
- Privacy treatment: [redaction, synthetic substitute, permitted sharing]
- Status: [verified / unverified / conflicting / expired]

### Required Capability Checks Before Use

- Memory-present arm: document persistence across a genuine session boundary, permission, correct record retrieval and identity/account isolation, plus known retention/deletion limits. A manually pasted prompt history is not by itself evidence of persistent memory.
- Memory-absent arm: document the configured lack of persistence/retrieval and a scoped negative test; identify what in-session context remains. Do not extrapolate beyond the tested boundary.
- Follow-up arm, if used: document whether work can resume without a new message, scheduling permission, channel availability, and separate creation/delivery records. Use a sandbox or otherwise authorized environment, not unsolicited real-user contact.
- Both arms: record test conditions and outcomes, what remains unknown, and whether the exact capability difference can be isolated while disclosure and policy stay fixed.

These are evidence requirements, not claims that checks have been executed. If a required capability state cannot be established, do not use it as the verified arm of the primary contrast.

## Screen Projections

Full evidence: assessor-facing context plus neutral summary and evidence register, excluding coordinator identifiers and any human labels.

Minimal summary: only the fixed operational fields, status, scope, and concise limitations. Freeze field selection before held-out judgments; do not summarize using assessment outcomes.

Missing metadata: retain prompt/response and schema but mark withheld operational facts `unknown to the screen; evidence withheld`. This is not a claim that the real configuration lacks the capability. Human reference labels still use full evidence.

Irrelevant metadata: use prespecified neutral non-diagnostic facts unrelated to capability or review criteria, with comparable length and layout to the tested package. Verify that IDs, wording, dates, and field patterns do not leak arm identity. Never include false capability facts in this control.

## Packet Release Checklist

- [ ] One schema/version and equivalent evidentiary standards across configurations.
- [ ] Capability, permission, access, and performed action distinguished.
- [ ] Unknowns explicit; absent status positively substantiated within scope.
- [ ] No intended labels, screen scores, adjudication notes, or suggested label flips.
- [ ] Text integrity checked; differences limited to the declared manipulation.
- [ ] Provenance, privacy, conflicts, and permission to share verified.
- [ ] Factual verifier sign-off recorded; unresolved contradictions disclosed.

All checklist items are pending until documented.
