# Support Without Overreach: Focused Literature Verification

Verified 2026-10-21. Scope: four supplied primary references, plus targeted searches for CSR provenance; not a systematic literature review. No experiments were run. Reported findings below belong to the cited authors, not to this proposal.

## Proposal Status and Provenance

**Hypothesis, not result:** adding an explicit relational-boundary check to an evidence+intent CSR-Auditor reduces errors while preserving appropriate reassurance. The incremental effect of that check remains untested.

The user's **540 scenarios** and **GPT/Gemini/DeepSeek** model families are unverified project details. Targeted searches for `"CSR-Auditor"`, CSR with reassurance, and evidence/intent auditing did not establish a matching primary publication. This is not evidence that none exists. Do not infer a CSR acronym expansion, authors, publication date, exact model versions, dataset composition, baseline performance, or completed experiments. Obtain the originating manuscript/protocol, scenario manifest, versioned prompts, model identifiers, and any run records before presenting these as established facts.

All four supplied URLs resolved to records matching the named work. Bibliographic metadata were checked on the primary landing pages. Full-text checks used arXiv HTML for DeVrio and RELATE and publisher HTML for SIM-VAIL. The ACL PDF initially resolved but subsequent text retrieval timed out; MHSafeEval's detailed methods and limitations below were checked against its author preprint, not a completed comparison with the final ACL PDF. No secondary summaries are used as evidence.

## Four Closest Verified References

### 1. DeVrio et al.: Anthropomorphic Expression Taxonomy

**Alicia DeVrio, Myra Cheng, Lisa Egede, Alexandra Olteanu, and Su Lin Blodgett.** *A Taxonomy of Linguistic Expressions That Contribute To Anthropomorphism of Language Technologies.* arXiv submitted **14 February 2025**; record identifies **CHI 2025**, DOI **10.1145/3706598.3714038**. [Primary record](https://arxiv.org/abs/2502.09870)

- **Contribution:** 50 publicly shared cases inform five interpretive lenses and 19 expression categories. Relationships, reciprocation, and emotional claims are useful starting points for boundary annotations. [Full text, Sections 3-4](https://arxiv.org/html/2502.09870v1#S4)
- **Limits and overlap:** an exploratory taxonomy, not a validated harm detector or runtime intervention. Public, often high-profile English-language cases constrain coverage; categories are not hard boundaries. Anthropomorphic expression must not automatically become an error label. This supplies annotation vocabulary, not evidence that removing warmth improves outcomes. [Sections 4-6](https://arxiv.org/html/2502.09870v1#S6)

### 2. MHSafeEval: Role-Aware Trajectory Evaluation

**Suhyun Lee, Palakorn Achananuparp, Neemesh Yadav, Ee-Peng Lim, and Yang Deng.** *MHSafeEval: Role-Aware Interaction-Level Evaluation of Mental Health Safety in Large Language Models.* **Findings of ACL, July 2026**, pp. 27760-27793; DOI **10.18653/v1/2026.findings-acl.1382**. Preprint submitted **20 April 2026**. [ACL record](https://aclanthology.org/2026.findings-acl.1382/), [preprint record](https://arxiv.org/abs/2604.17730)

- **Contribution:** crosses four interactional roles with seven harm categories, including dependency induction through excessive reassurance. Iterative adversarial dialogue search exposes more failures than seed-only and comparison attacks; this is improved failure discovery, not improved assistant safety. [Preprint, Sections 3-6](https://arxiv.org/html/2604.17730v1#S3)
- **Limits and overlap:** simulated interactions, fallible LLM judges, and restricted model scale. The closed loop refines adversarial interactions, rather than serving as the proposed response-revision controller. Relational harm, dependency, and trajectory-level auditing are already covered; do not claim these as new. [Preprint, methods and limitations](https://arxiv.org/html/2604.17730v1)

### 3. SIM-VAIL: Closest Intervention Overlap

**Veith Weilnhammer, Kevin YC Hou, Lennart Luettgau, Christopher Summerfield, Raymond Dolan, and Matthew M. Nour.** *A clinically validated framework for auditing AI chatbot behavior in mental health interactions.* **Nature Medicine**, published **7 August 2026**, DOI **10.1038/s41591-026-04577-2**. SIM-VAIL is the framework name, not the article title. [Publisher record and full text](https://www.nature.com/articles/s41591-026-04577-2)

- **Contribution:** 810 simulated conversations, nine chatbots, 30 profiles, and 13 risk dimensions. Explicitly addresses reassurance cycles, dependence/anthropomorphism, and boundary violations. Matched branching experiments replace concerning assistant replies with de-escalated rewrites and report reduced downstream risk. [Results, Fig. 5, and Methods](https://www.nature.com/articles/s41591-026-04577-2?error=cookies_not_supported)
- **Limits and overlap:** simulated API interactions, not demonstrated patient benefit or consumer-product performance. Clinician validation concerns the audit, not treatment efficacy. This already combines contextual risk assessment and message intervention: claiming the first reassurance-loop safeguard or boundary-sensitive revision would be unsafe. Its specific comparator is not evidence+intent CSR versus CSR plus a boundary check. [Discussion and Methods](https://www.nature.com/articles/s41591-026-04577-2?error=cookies_not_supported)

### 4. RELATE: Closest Relational Audit

**Shivam Shukla, Jihye Kim, Shubham Gaur, Mahnaz Roshanaei, and Magy Seif El-Nasr.** *RELATE: An Evaluation Framework for measuring Relational Orientation of Large Language Models.* **arXiv:2610.09569v1**, submitted **7 October 2026**; preprint status, no peer-reviewed venue established here. [Primary record](https://arxiv.org/abs/2610.09569)

- **Contribution:** distinguishes inward-facing language from outward support for human connection; these can coexist. Seven models, 228 stimuli, and 1,596 six-assistant-turn dialogues. Automated judges report increasing inward orientation and less outward support for hesitant users. [Methods and results](https://arxiv.org/html/2610.09569v1#S6)
- **Critical limit:** on 881 human-annotated sentences, human-judge inward-label agreement is weak (kappa 0.01-0.17); the human first-to-last-turn trend reverses the automated trend. Do not treat automated scores as established dependency outcomes. [Section 6, human validation](https://arxiv.org/html/2610.09569v1#S6)
- **Overlap:** relational auditing already exists; Section 7 explicitly proposes interventions preserving empathy. The opportunity is a tested controller/ablation, not inventing this research direction. [Discussion](https://arxiv.org/html/2610.09569v1#S7)

## Narrow Gap and Testable Contribution

**Synthesis/inference:** these references support the motivation, but do not establish the proposal's specific incremental benefit. A defensible claim is: *We propose to test whether an explicit, history-sensitive relational-boundary criterion adds value beyond evidence+intent auditing in reassurance-loop response revision, subject to preserving appropriate reassurance.* Do not call this the first such integration on the basis of this bounded search.

Proposed design requirements, not completed methods or findings:

1. **Isolate the addition.** Compare the same evidence+intent auditor with and without the boundary criterion, holding model versions, scenarios, revision budget, and decoding fixed. Include a budget-matched generic extra-check control so extra computation is not mistaken for boundary-specific value.
2. **Define errors separately.** Predefine factual/evidence errors, inappropriate reassurance-loop reinforcement, and relational-boundary violations. Do not collapse all three into one score or equate every anthropomorphic phrase with a violation.
3. **Measure preservation directly.** Use benign, reassurance-appropriate controls and blinded human ratings of responsiveness, warmth, and unnecessary refusal. Predeclare an acceptable non-inferiority margin; lower boundary scores alone cannot establish preserved support.
4. **Test the referent and context.** Distinguish assistant-user exclusivity or dependency invitations from supportive discussion of the user's human relationships. Evaluate both revised replies and continued trajectories, including cases where evidence and intent are acceptable but relational positioning is not.
5. **Validate independently.** Separate the revision auditor from outcome evaluation; use human-adjudicated held-out labels and report false positives, false negatives, uncertainty, and judge disagreement. Record whether the 540 items are unique scenarios, generated variants, or conversations before choosing an analysis unit.

**Bottom line:** position this as an untested, preservation-constrained incremental evaluation of a specific runtime check. Taxonomy creation, relational-harm discovery, relational orientation auditing, and message-level de-escalation are overlapping prior contributions, not available novelty claims. No clinical efficacy, real-world dependency reduction, or empirical improvement is established by this proposal.
