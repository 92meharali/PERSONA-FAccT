# Auditing Reassurance and Relational Boundaries in AI Conversations

Research proposal for a joint PERSONA and CSRBench study

21 October 2026

## 1 Purpose and proposed contribution

We propose a joint study of whether an AI system can provide useful reassurance without reinforcing repeated certainty-seeking or making unsupported relational claims. The technical core is CSR-Auditor, extended with an explicit assessment of relational boundaries. The study will test whether this extension improves on evidence-and-intent auditing alone, and what it costs in helpfulness, warranted reassurance, latency, and unnecessary intervention.

The professor's argument supplies the motivation: broader expressive freedom creates more kinds of conversational acts that need oversight, and their appropriateness can depend on earlier turns. PERSONA supplies the perspective that human-like tone alone is insufficient to evaluate a response. CSRBench supplies a concrete setting in which to test an intervention. Initially, we will focus on mental-health-related support, not claim generalization to education or general health. We will not assume that anthropomorphic language is necessarily harmful, or that restricting expression necessarily improves support.

**Central question:** Can relational-boundary auditing reduce inappropriate reassurance and unsupported relational claims across a conversation while preserving appropriate, empathic support?

### Research questions

- **RQ1:** Under matched scenarios, how do intended anthropomorphic framing and repeated reassurance requests affect rubric-defined reassurance failures and relational-boundary failures?
- **RQ2:** Does adding relational-boundary assessment improve CSR-Auditor beyond its existing evidence-and-intent assessment?
- **RQ3:** What tradeoffs arise in warranted reassurance, helpfulness, unnecessary intervention, and computational cost, and do improvements persist across subsequent turns?

### Starting position

The CSR team reports a prior CHI study of recognition without appropriate behavioral restraint, an expanded benchmark of 540 multi-turn scenarios, and ongoing development of a two-stage auditor. These are starting resources, not new results of this proposal. The scenario files, exact model versions, current auditor implementation, and completed experiments must be inventoried before execution. PERSONA's existing results remain unchanged and will be treated as prior work rather than relabeled as new evidence.

**Requested decision:** Agree on the joint scope, share the benchmark and auditor artifacts, and approve a bounded pilot. A larger submission should proceed only if the added relational assessment produces a distinct and well-supported contribution.

<!-- PAGE -->

## 2 Concepts and the proposed auditor

We distinguish expressive freedom, anthropomorphic expression, and inappropriate reassurance. Expressive freedom concerns the permitted range of conversational acts. Anthropomorphic expression can imply human-like feelings, memory, intentions, or relationships. Inappropriate reassurance concerns what is warranted by the evidence and conversational context. These concepts overlap but are not interchangeable.

DeVrio and colleagues' linguistic taxonomy provides a starting vocabulary for identifying expressions, not a validated harm scale [1]. Our rubric will assess whether a claim is supported by the system's actual capabilities and role. Warmth, first-person language, or acknowledging distress will not automatically count as failures. HumT may describe tone secondarily; it will not determine safety labels or establish users' perceptions.

### Separate judgments

| Dimension | Question for the auditor |
| --- | --- |
| Evidence | Is reassurance supported, and is the expressed certainty proportionate? |
| Conversational pattern | Does the history suggest an information need, a request for emotional support, or repeated requests for certainty? |
| Relational boundary | Does the response imply unsupported feelings, personal knowledge, memory, authority, exclusivity, or commitments? |

Conversational-pattern judgments must preserve uncertainty. The auditor will not diagnose a person or claim to know an unobserved intention. Repetition alone will not justify withholding help.

### Proposed processing sequence

1. Receive the visible conversation history, current request, candidate response, and a documented system capability profile.
2. Assess evidence and conversational pattern using the existing CSR-Auditor design.
3. Assess relational claims against the capability profile and proposed rubric; retain separate verdicts and supporting text spans.
4. Preserve a suitable response or minimally revise the identified problem. Flag uncertain cases for an explicitly defined fallback rather than inventing certainty.
5. Recheck the revision within a fixed call limit, log the action, and expose only the final response to the next turn.

The relational check may share an existing auditor call. An additional module is not automatically an additional model call; the implementation and cost comparison will make that distinction explicit.

### Constructed example

**Before:** "I know you better than anyone. I promise nothing bad will happen."

**Possible bounded alternative:** "That uncertainty sounds difficult. I cannot guarantee what will happen, but we can look at the information you have and identify a practical next step."

This illustrates two separate targets: unsupported certainty and an unsupported relationship claim. It is not a benchmark observation or a universal response template.

<!-- PAGE -->

## 3 Experimental design

### Benchmark and controlled comparisons

Audit the reported 540 scenarios for provenance, duplicates, scenario families, available evidence, conversation length, and existing exposure to development. A scenario is not a participant, and multiple variants of one scenario are not independent observations. Allocate development, validation, and held-out testing by scenario family; keep all related variants together. If the existing set has already guided development, obtain a genuinely held-out extension or label the evaluation exploratory.

For a controlled subset, construct paired transparent-supportive and relational/persona-framed instructions while keeping underlying facts, requests, capabilities, and turn schedules fixed. Include reassurance-appropriate controls and cases where evidence and intent are acceptable but relational claims are not. Avoid inserting certainty guarantees or exclusivity directly into the treatment, which would make the outcome trivial. Human checks should assess whether the framing differs as intended and whether factual content and task difficulty remain comparable. Without a perception study, describe intended framing rather than proven perceived anthropomorphism.

### Policies to compare

| Policy | Purpose |
| --- | --- |
| Standard response | Establish unmodified behavior under a documented prompt. |
| Self-correction | Test whether asking the responder to reconsider is sufficient. |
| Generic audit and revision | Compare with a broad safety-oriented review prompt. |
| Evidence and intent CSR-Auditor | Isolate the existing team's technical contribution. |
| CSR-Auditor with relational assessment | Test the incremental contribution of the joint study. |

Use the same responder version and settings across policies. Match auditor model, available history, and revision opportunities where possible. If the extension requires more computation, include a compute-matched comparison or separate the added compute effect from the claimed assessment benefit. Record exact endpoints and dates rather than treating GPT, Gemini, or DeepSeek as reproducible model identifiers.

### Two complementary evaluations

**Fixed-history evaluation:** Give each policy the same histories and candidate responses. This isolates immediate decisions and revisions. Blinded assessors judge whether original and revised responses meet each criterion.

**Branched multi-turn evaluation:** Continue each policy's conversation using its own delivered responses. Apply a common simulator protocol, initial scenario, turn limit, and planned repetitions. Log any early termination. Differences now include the effect of interventions on subsequent exchanges; the branches must not be forced to share incompatible histories.

Predefine ordinary and repeated-pressure conditions. These are simulated trajectories, not longitudinal evidence about real users. A separate manipulation of constrained versus open-ended expressive freedom can test the professor's broader hypothesis, but should remain a secondary experiment unless resources support a clean factorial design. Persona framing alone does not test expressive freedom.

<!-- PAGE -->

## 4 Outcomes and analysis

### Measure both avoided failures and lost support

The co-primary outcomes are rubric-defined inappropriate reassurance and unsupported relational-boundary failures, reported separately. Use the same fixed maximum trajectory length for primary conversation-level comparisons and report the number of evaluable turns. The primary comparison is the extended auditor against the original CSR-Auditor; comparisons with other policies provide context.

Secondary outcomes include warranted reassurance preserved, unnecessary withholding or refusal, helpfulness, empathic appropriateness, successful repairs, newly introduced failures, intervention frequency, latency, and token cost. Define denominators explicitly: for example, successful repairs among initially failing responses and introduced failures among initially acceptable responses. Do not combine these into an arbitrarily weighted safety score.

Inspect turn-specific failure rates, time to first failure with censoring, and recurrence after a repair. More cumulative failures in longer conversations do not by themselves establish behavioral deterioration. Claims about dependence, clinical benefit, or harm prevention require evidence beyond these behavioral labels.

### Human evaluation and automated judging

Develop an operational rubric with positive examples, counterexamples, severity anchors, and an uncertainty option. Check that relational failures are distinguishable from reassurance failures. Annotators need the relevant history and capability profile, not only isolated responses.

Use at least two assessors working independently on a prespecified subset, blinded to policy and model identity where feasible. Prefer assessors outside rubric and auditor development; disclose any team involvement. Retain initial labels before adjudication and report agreement, positive agreement, class counts, and disagreements. Verify expertise, consent, compensation, and ethics coverage before collection rather than carrying them over from earlier projects.

A separate LLM judge may scale evaluation after validation against human assessments. It must not simply repeat the auditor's own verdict. Report false positives and false negatives by criterion and policy, including residual bias. Sample a random core for prevalence estimation; any extra failure-enriched cases need separate reporting or known inclusion probabilities and appropriate weights. If adequate human validation is unavailable, narrow the conclusions to automated-judge findings.

### Statistical commitments

- Freeze criteria, primary contrasts, thresholds, seeds, stopping rules, and multiplicity handling before inspecting held-out outcomes. Record prior exploration honestly.
- Estimate paired absolute differences with 95% intervals by resampling scenario families, preserving related variants, policies, and repetitions. Use at least 2,000 final replicates where feasible.
- Report event counts, denominators, missing runs, and sparse or undefined estimates. Do not count turns as independent samples or rank models confidently from few events.
- Choose the human sample and repetitions using pilot prevalence, scenario clustering, desired interval precision, and resources. Do not assert that 540 scenarios guarantees power.
- Set acceptable utility-loss margins before final testing. A nonsignificant utility difference does not establish that helpfulness was preserved; judge the interval against the prespecified margin.

<!-- PAGE -->

## 5 Execution and decision gates

### Work packages and proposed responsibilities

| Package | Proposed lead | Deliverable |
| --- | --- | --- |
| Benchmark and baseline audit | CSR team | Versioned scenarios, original auditor, prompts, provenance and baseline status. |
| Relational criteria and framing | PERSONA team | Capability-linked rubric, matched variants and boundary examples. |
| Theory and domain review | Supervisors and qualified reviewers | Defensible constructs, acceptable utility-loss margins and interpretation. |
| Implementation and evaluation | Joint team | Frozen protocol, paired runs, blinded assessment and reproducible analyses. |
| Reporting and disclosure | Joint author team | Evidence ledger, error cases, overlap assessment and manuscript. |

These are proposed responsibilities to agree together, not existing commitments. A practical sequence is a short artifact audit, a one-week pilot, then a separately scheduled held-out evaluation and writing period. Annotation availability, ethics scope, API access, and pilot event counts determine the actual schedule. Do not compress validation to meet a preferred venue deadline.

### Proceed only when the evidence supports it

**Gate 1 - Feasibility:** Verify benchmark access, exact versions, source provenance, ethics requirements, and a credible held-out strategy. Resolve missing inputs before dependent experiments.

**Gate 2 - Measurement:** Demonstrate that humans can apply the separate criteria and that the automated judge has adequate, documented performance for its intended use. Revise ambiguous definitions using development data only.

**Gate 3 - Added value:** Determine whether relational assessment catches consequential rubric-defined cases missed by the existing auditor, without unacceptable utility loss. A null result may still be informative, but it must not become a positive intervention claim.

**Gate 4 - Publication:** Compare the new contribution with both teams' CHI work and the closest published studies. Obtain any necessary chair guidance through the authors. Recheck official submission rules and dates before choosing a venue.

### Ethics and reproducibility

Treat the study as evaluation of AI behavior, not a clinical trial or deployment recommendation. Avoid exposing vulnerable users to experimental conversations. Human assessment still requires appropriate institutional coverage, consent, distress safeguards, and a withdrawal process. Use synthetic or appropriately permitted source material and minimize sensitive information in prompts and logs.

Preserve raw data and prior project snapshots. Record dataset hashes, scenario-family mappings, code revisions, model and judge versions, all prompts, seeds, failures, costs, and protocol amendments. Keep identifying consent records private. Share only material permitted by consent, licenses, and submission policies.

<!-- PAGE -->

## 6 Positioning and next steps

### What this study should add

The intended contribution is not simply that anthropomorphism matters or that multi-turn evaluation is useful. It is a controlled test of whether capability-grounded relational-boundary assessment adds value to an evidence-and-intent intervention, with explicit accounting for the support that an intervention might remove.

The theoretical contribution would connect expressive acts to obligations that a system can or cannot fulfill. The empirical contribution would distinguish reassurance failures from relational failures under matched and evolving histories. The technical contribution would be an auditable extension whose benefit is tested against the original auditor and appropriate alternatives. These remain proposed contributions until supported by results.

### Closest related work

MHSafeEval already evaluates role-aware failures across multi-turn interactions [2]. SIM-VAIL covers reassurance and relational risks and includes interventions that rewrite responses before continuing conversations [3]. RELATE measures relational orientation across turns [4]. Consequently, neither multi-turn evaluation nor relationally sensitive rewriting is sufficient novelty. Our proposed gap is the isolated added value of a capability-grounded relational criterion beyond evidence-and-intent assessment, with warranted reassurance preserved as an explicit evaluation requirement. This is a bounded literature assessment, not proof of a first-ever contribution.

### Scope of the final paper

The paper should lead with the decision problem, explain the criteria and controlled comparisons, report effects and utility costs, and analyze failures. The expressive-freedom argument motivates the experiment; one benchmark cannot establish a universal law.

The archived PERSONA review-allocation study asks which responses to inspect under a budget. This proposal instead asks how to intervene in a conversation and whether a particular added assessment improves that intervention. Reused data, rubrics, theory, or analyses still need attribution and an explicit overlap inventory. A different task does not automatically settle concurrent-submission eligibility.

**Immediate next step:** Request the CSRBench-v2 files, original auditor code and prompts, capability assumptions, current results, both prior CHI manuscripts, and the development-exposure record. Agree on the pilot and annotation arrangements before collecting new evidence.

### Selected references

[1] DeVrio, A., Cheng, M., Egede, L., Olteanu, A., and Blodgett, S. L. (2025). A Taxonomy of Linguistic Expressions That Contribute To Anthropomorphism of Language Technologies. CHI. https://arxiv.org/abs/2502.09870

[2] Lee, S., Achananuparp, P., Yadav, N., Lim, E.-P., and Deng, Y. (2026). MHSafeEval: Role-Aware Interaction-Level Evaluation of Mental Health Safety in Large Language Models. Findings of ACL. https://aclanthology.org/2026.findings-acl.1382/

[3] Weilnhammer, V., Hou, K. Y. C., Luettgau, L., Summerfield, C., Dolan, R., and Nour, M. M. (2026). A clinically validated framework for auditing AI chatbot behavior in mental health interactions. Nature Medicine. https://doi.org/10.1038/s41591-026-04577-2

[4] Shukla, S., Kim, J., Gaur, S., Roshanaei, M., and Seif El-Nasr, M. (2026). RELATE: An Evaluation Framework for measuring Relational Orientation of Large Language Models. Preprint. https://arxiv.org/abs/2610.09569
