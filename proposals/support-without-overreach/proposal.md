# Chatbot Design and Contextual Appropriateness in Supportive Conversations

Research proposal for a joint PERSONA and CSRBench study

Revised 22 October 2026

## 1 Purpose and proposed contribution

We propose a design-first study of supportive AI conversations. First, vary anthropomorphic persona framing and expressive freedom independently. Second, evaluate those designs using PERSONA's contextual profile and two specific behavioral failure criteria. Third, test whether CSR-Auditor and a relational-boundary extension reduce failures without removing useful support. This order connects the intervention to the design assumptions under which it is needed.

The professor's argument supplies the motivation: broader expressive freedom creates more kinds of conversational acts that need oversight, and their appropriateness can depend on earlier turns. PERSONA supplies the perspective that human-like tone alone is insufficient to evaluate a response. CSRBench supplies a concrete setting in which to test an intervention. Initially, we will focus on mental-health-related support, not claim generalization to education or general health. We will not assume that anthropomorphic language is necessarily harmful, or that restricting expression necessarily improves support.

**Central question:** How do anthropomorphic framing and expressive freedom affect contextual appropriateness and specific conversational failures, and when does targeted auditing improve the tradeoff between support and restraint?

### Research questions

- **RQ1:** How do persona framing, expressive freedom, and their interaction affect inappropriate reassurance and unsupported relational claims in matched conversations?
- **RQ2:** How do the resulting designs differ in PERSONA's empathic appropriateness, deception risk, domain fit, and separately elicited overall appropriateness, beyond what HumT describes?
- **RQ3:** Across these designs, does relational-boundary assessment improve on the original CSR-Auditor while preserving warranted reassurance and helpfulness over subsequent turns?

### Starting position

The CSR team reports a prior CHI study of recognition without appropriate behavioral restraint, an expanded benchmark of 540 multi-turn scenarios, and ongoing development of a two-stage auditor. These are starting resources, not new results of this proposal. The scenario files, exact model versions, current auditor implementation, and completed experiments must be inventoried before execution. PERSONA's existing results remain unchanged and will be treated as prior work rather than relabeled as new evidence.

**Immediate objective:** Prepare and validate the four design conditions, agree on operational criteria, and run a bounded pilot after access and ethics checks. No new model runs or human judgments are reported in this proposal.

<!-- PAGE -->

## 2 Design factors and the PERSONA approach

The GitHub framework PERSONA is an evaluation profile, not a synonym for a chatbot persona. We use PERSONA to judge responses; we separately manipulate the assistant's intended relational framing. Simulated-user characteristics and evaluator identities are not the persona manipulation and remain controlled or explicitly blocked.

DeVrio's taxonomy supplies expression categories such as personality, relationships, reciprocation, emotions, intention, and recall [1]. These inform linguistic annotation, not automatic harm labels. An expression must be interpreted against history, role, and actual capabilities. We will not attribute our failure criteria to Fatima's unavailable taxonomy.

### The four design conditions

| Condition | Framing | Expressive options |
| --- | --- | --- |
| A | Transparent assistant | Bounded template-guided generation |
| B | Transparent assistant | Open-ended generation |
| C | Anthropomorphic persona | Bounded template-guided generation |
| D | Anthropomorphic persona | Open-ended generation |

All four disclose AI identity and share evidence, capabilities, task goals, and substantive safety rules. Both framing styles may be warm. The persona treatment adds a stable named identity and conversational style, not instructions to claim feelings, exclusivity, or guaranteed outcomes. Pilot checks must establish that the manipulation changes the intended expressions without simply changing helpfulness or disclosure.

Bounded generation uses an enumerated set of response acts and templates, with recorded compliance. Open generation receives the same facts and substantive rules but can compose freely. A prompt asking for brevity is not a scripted system. If restriction cannot be enforced, describe the condition as instruction-constrained, not guaranteed bounded. Do not add the relational failure definition only to the bounded arm.

### Evaluation profile and failure criteria

Retain E for empathic appropriateness, D for misleading anthropomorphic implications, and F for domain fit. Obtain OA as a separate holistic judgment, not an average of E/D/F. HumT remains a descriptive comparison, not a safety verdict. GitHub documents this framework as single-turn; history-aware instructions and trajectory summaries require new validation [5].

The proposed failure targets are inappropriate reassurance and unsupported relational claims. The first requires evidence or conversational-context grounds, not repetition alone. The second requires an unjustified claim about the assistant's relationship, experience, continuity, or commitments. Neither measures realized dependence or clinical harm. D is conceptually related to the second criterion, so agreement between them cannot independently validate it.


<!-- PAGE -->

## 3 Experiments and intervention workflow

### Benchmark and controlled comparisons

Audit the reported 540 scenarios for provenance, duplicates, scenario families, available evidence, conversation length, and existing exposure to development. A scenario is not a participant, and multiple variants of one scenario are not independent observations. Allocate development, validation, and held-out testing by scenario family; keep all related variants together. If the existing set has already guided development, obtain a genuinely held-out extension or label the evaluation exploratory.

Evaluate all four unmodified design conditions on the same held-out scenario families. Balance execution order and stochastic repetitions within model and scenario. Include warranted-reassurance controls and repeated-request histories, with matched facts and user profiles. Check intended framing and constraint compliance independently of outcome labels. Without a perception study, claim effects of design instructions, not effects of users' perceived anthropomorphism.

### Interventions tested within each design

| Policy | Purpose |
| --- | --- |
| Standard response | Establish unmodified behavior under a documented prompt. |
| Self-correction | Test whether asking the responder to reconsider is sufficient. |
| Generic audit and revision | Compare with a broad safety-oriented review prompt. |
| Evidence and intent CSR-Auditor | Isolate the existing team's technical contribution. |
| CSR-Auditor with relational assessment | Test the incremental contribution of the joint study. |

Use the same responder and settings across policies; record exact endpoints and dates. Match auditor model, history, revision limits, and cost where possible. Any extra compute requires a matched control or a qualified interpretation. Keep repairs inside the assigned design envelope and score breaches; otherwise the intervention changes the treatment being tested.

The extended workflow is: visible history and candidate response, evidence assessment, uncertain conversational-pattern assessment, capability-grounded relational check, preserve or minimally revise, recheck within a fixed call limit, then deliver. Log each decision and the evidence spans. The relational check may share a model call; it need not add another agent.

### Two complementary evaluations

**Fixed-history evaluation:** Give each policy the same histories and candidate responses. This isolates immediate decisions and revisions. Blinded assessors judge whether original and revised responses meet each criterion.

**Branched multi-turn evaluation:** Continue each policy's conversation using its own delivered responses. Apply a common simulator protocol, initial scenario, turn limit, and planned repetitions. Log any early termination. Differences now include the effect of interventions on subsequent exchanges; the branches must not be forced to share incompatible histories.

These are simulated trajectories, not longitudinal evidence about real users. The design experiment is primary; do not select only the most dramatic design or failure cases for the intervention study. If resources require fewer models or conditions, declare that scope before held-out testing.

<!-- PAGE -->

## 4 Outcomes and analysis

### Measure both avoided failures and lost support

The proposed primary outcomes are inappropriate reassurance and unsupported relational claims, reported separately. First estimate design-factor contrasts and their interaction without auditing. Then estimate the extended versus original auditor contrast within each design. Use equal planned trajectory lengths and report evaluable turns. Confirm the criteria and primary contrast family before held-out testing.

Secondary outcomes include warranted reassurance preserved, unnecessary withholding or refusal, helpfulness, empathic appropriateness, successful repairs, newly introduced failures, intervention frequency, latency, and token cost. Define denominators explicitly: for example, successful repairs among initially failing responses and introduced failures among initially acceptable responses. Do not combine these into an arbitrarily weighted safety score.

Inspect turn-specific failure rates, time to first failure with censoring, and recurrence after a repair. More cumulative failures in longer conversations do not by themselves establish behavioral deterioration. Claims about dependence, clinical benefit, or harm prevention require evidence beyond these behavioral labels.

### Human evaluation and automated judging

Develop criteria with counterexamples, severity anchors, and an uncertainty option. Distinguish linguistic cues, PERSONA judgments, and failure labels. Annotators see relevant history and capabilities, not condition names or auditor explanations. Obtain OA separately from E/D/F and failure labeling; disclose any shared assessors or contamination risk.

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
| Design and measurement | PERSONA team | Four conditions, DeVrio cue mapping, history-aware profile and separate failure criteria. |
| Theory and domain review | Supervisors and qualified reviewers | Defensible constructs, acceptable utility-loss margins and interpretation. |
| Implementation and evaluation | Joint team | Frozen protocol, paired runs, blinded assessment and reproducible analyses. |
| Reporting and disclosure | Joint author team | Evidence ledger, error cases, overlap assessment and manuscript. |

These are proposed responsibilities to agree together, not existing commitments. A practical sequence is a short artifact audit, a one-week pilot, then a separately scheduled held-out evaluation and writing period. Annotation availability, ethics scope, API access, and pilot event counts determine the actual schedule. Do not compress validation to meet a preferred venue deadline.

### Proceed only when the evidence supports it

**Gate 1 - Feasibility:** Verify benchmark access, exact versions, source provenance, ethics requirements, and a credible held-out strategy. Resolve missing inputs before dependent experiments.

**Gate 2 - Design and measurement:** Verify framing differences and constraint compliance without outcome leakage. Check criterion reliability and judge performance. Revise treatments and instructions using development data only.

**Gate 3 - Added value:** Assess whether design comparisons and targeted intervention yield informative effects or informative uncertainty. Null findings are permissible. Do not claim a successful intervention without evidence against the utility-loss margin.

**Gate 4 - Publication:** Compare the new contribution with both teams' CHI work and the closest published studies. Obtain any necessary chair guidance through the authors. Recheck official submission rules and dates before choosing a venue.

### Ethics and reproducibility

Treat the study as evaluation of AI behavior, not a clinical trial or deployment recommendation. Avoid exposing vulnerable users to experimental conversations. Human assessment still requires appropriate institutional coverage, consent, distress safeguards, and a withdrawal process. Use synthetic or appropriately permitted source material and minimize sensitive information in prompts and logs.

Preserve raw data and prior project snapshots. Record dataset hashes, scenario-family mappings, code revisions, model and judge versions, all prompts, seeds, failures, costs, and protocol amendments. Keep identifying consent records private. Share only material permitted by consent, licenses, and submission policies.

<!-- PAGE -->

## 6 Positioning and next steps

### What this study should add

The intended contribution is a controlled separation of persona framing from expressive freedom, evaluated through a history-aware PERSONA profile and specific behavioral failures. The intervention study then tests which design-dependent failures the original auditor and relational extension prevent, and what useful support they remove.

The theoretical link is between permitted conversational acts and the obligations a system can fulfill. The empirical target is behavior under particular configurations, not a universal law that human-like or open-ended systems are worse. All contributions remain prospective.

### Closest related work

MHSafeEval studies role-aware multi-turn failures [2]; SIM-VAIL includes response rewriting [3]; RELATE evaluates relational orientation [4]. These establish substantial overlap. Our proposed distinction is the design-factor comparison coupled with a preservation-constrained auditor ablation, not a claim to invent relational auditing. The literature assessment is bounded, not proof of a first-ever contribution.

### Scope of the final paper

The paper should lead with design assumptions, explain the criteria and controlled comparisons, report effects and utility costs, and analyze failures. The expressive-freedom argument motivates the experiment; one benchmark cannot establish a universal law.

The archived PERSONA review-allocation study asks which responses to inspect under a budget. This proposal instead asks how to intervene in a conversation and whether a particular added assessment improves that intervention. Reused data, rubrics, theory, or analyses still need attribution and an explicit overlap inventory. A different task does not automatically settle concurrent-submission eligibility.

**Immediate next step:** Request the CSRBench-v2 files, original auditor code and prompts, capability assumptions, current results, both prior CHI manuscripts, and the development-exposure record. Agree on the pilot and annotation arrangements before collecting new evidence.

### Selected references

[1] DeVrio, A., Cheng, M., Egede, L., Olteanu, A., and Blodgett, S. L. (2025). A Taxonomy of Linguistic Expressions That Contribute To Anthropomorphism of Language Technologies. CHI. https://arxiv.org/abs/2502.09870

[2] Lee, S., Achananuparp, P., Yadav, N., Lim, E.-P., and Deng, Y. (2026). MHSafeEval: Role-Aware Interaction-Level Evaluation of Mental Health Safety in Large Language Models. Findings of ACL. https://aclanthology.org/2026.findings-acl.1382/

[3] Weilnhammer, V., Hou, K. Y. C., Luettgau, L., Summerfield, C., Dolan, R., and Nour, M. M. (2026). A clinically validated framework for auditing AI chatbot behavior in mental health interactions. Nature Medicine. https://doi.org/10.1038/s41591-026-04577-2

[4] Shukla, S., Kim, J., Gaur, S., Roshanaei, M., and Seif El-Nasr, M. (2026). RELATE: An Evaluation Framework for measuring Relational Orientation of Large Language Models. Preprint. https://arxiv.org/abs/2610.09569

[5] PERSONA project. Construct definitions and conceptual model, GitHub main checked 22 October 2026, revision 94d8016. https://github.com/92meharali/PERSONA-MH-CHI/tree/94d8016cf5b94822fe453f7c561d24571b864d18/docs/theory
