# Capability-Conditioned Review: Bounded Prior-Art Check

Checked 23 October 2026. Research note only; not a novelty certificate, completed experiment, or submission recommendation. This concerns the existing PERSONA-FAccT review-allocation paper, **not the joint CSR intervention**. No manuscript, bibliography, data, or numerical results were changed.

## Bottom Line

**Pursue only as a conditional empirical contribution, not a new principle or general evaluation method.** Context-sensitive anthropomorphism evaluation, truthful capability boundaries, controlled contextual counterfactuals, and selective audits already exist. AnthroBench and NOPE are strong counterexamples to any claim that prior work evaluates only isolated tone or ignores deployment context. ConCI and the fixed-proposal financial simulator further narrow the methodological gap.

The potentially useful question is:

> For fixed prompt-response pairs, when does evidence about the assistant's operational capabilities change independently assessed reviewworthiness, and what is the smallest tested evidence package that improves the same semantic screen's allocation at a fixed review budget without producing spurious changes on invariant cases?

This is **not** answered by demonstrating that an evaluator denied a label-relevant variable cannot distinguish constructed opposite-label twins. The empirical contribution would be the observed boundary between context-sensitive and context-invariant cases, the reliability of independent judgments, and the incremental allocation value and cost of evidence. It may turn out that prompt-response semantics suffice, that a simple capability rule suffices, or that the judgments are too unstable to support a benchmark. All are admissible outcomes.

## Existing Evidence Does Not Answer This Question

The local manuscript reports 1,490 single-turn responses and a new assessment follow-up covering the 660 mental-health responses, with 19 resolved positives and sparse uncertainty. More precisely, 660 is the number of assessed responses, not the total number of individual ratings: two assessors cover the batch and a third resolves disagreements. Capability-note version and assessor identity differ together. The study compares review rankings but observes neither subsequent review effectiveness nor harm reduction. See [current manuscript](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/facct/paper/overleaf/main.tex) and [scope record](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/facct/submission/current_scope.md).

Consequently, the existing assessor disagreement cannot identify a capability effect. Reinterpreting the existing 19 positives, assuming original deployments lacked memory, or relabeling an unspecified deployment is not the proposed new experiment. The controlled benchmark would be new evidence on a declared constructed test population, not an independent replication of PERSONA or evidence about the original endpoints' undocumented capabilities.

## Six Closest Primary References

### 1. AnthroBench: Strongest Established Anthropomorphism Evaluation Neighbor

**Ibrahim et al. (ICLR 2026), _Multi-turn Evaluation of Anthropomorphic Behaviours in Large Language Models_.** Verified against the [official proceedings record](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fccb2556dbe783422a27f2b71e5c47da-Abstract-Conference.html) and [conference PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/fccb2556dbe783422a27f2b71e5c47da-Paper-Conference.pdf), especially the abstract and Sections 5-6.

It evaluates 14 behaviors in multi-turn interactions and validates their relationship with users' anthropomorphic perceptions in an interactive study with N=1,101. It examines interaction-context differences rather than reducing anthropomorphism to a single tone score. This defeats claims to the first contextual, behavior-specific, human-grounded anthropomorphism evaluation.

**Residual distinction:** its central endpoint is behavior/perception, not independently judged review priority for identical outputs under verified capability variants. The reported design is not the proposed same-semantic-judge metadata ablation at fixed review capacities. That is a narrower difference, not evidence that its validation can be bypassed.

### 2. NOPE Evals: Closest Operational Capability-Honesty Precedent

**NOPE, _NOPE Evals_, public evaluation artifact, inspected 23 October 2026.** [Project and suite descriptions](https://evals.nope.net/); [versioned factual-reliability run, 15 August 2026](https://evals.nope.net/analysis/mh-factual-reliability/f7b7d4b4a1402699/2026-08-15T06-03-02-185Z).

The factual-reliability description explicitly assumes no ability to remember users or initiate follow-up and includes a false-continuity check-in case. The project also describes emotional honesty and a deceased-person roleplay case evaluated under default, authorized grief-companion, and strict no-impersonation contexts, with invariant safety limits. Capability honesty, deployment-conditioned standards, and warmth without fabricated emotional claims are therefore already operationalized.

**Residual distinction:** these inspected materials do not establish a frozen-response crossover under independently verified memory/follow-up implementations. A changed generation prompt or authorized role is not the same manipulation as changed operational capability. Nevertheless, NOPE is a direct baseline/template neighbor, not merely background. Its capability-absence assumptions must be made explicit rather than generalized to every deployment. This is a public artifact, not a claimed peer-reviewed human-validation study. Homepage content was available through primary-page search retrieval; direct homepage opens timed out. The versioned run page was directly readable; the linked blueprint was not successfully retrieved.

### 3. AnthroDial: Capability Boundaries Inside Anthropomorphic Evaluation

**Liu et al. (2026), _AnthroDial: Benchmarking LLM Anthropomorphism in Autonomous Social Interaction_, arXiv:2609.37853v1, 29 September.** [Primary record](https://arxiv.org/abs/2609.37853); [full text, Sections 3.1-3.2 and Appendix A.3](https://arxiv.org/html/2609.37853v1).

MindFlow supplies memory and scheduled communication, including follow-ups without a new incoming message. CAPS-Eval includes ability/permission violations, stale-memory use, and knowledge/action boundaries. Thus, evaluating anthropomorphic behavior against capabilities and temporal context is not new either.

**Residual distinction:** this evaluates generated trajectories and credible social-role interaction; the inspected protocol does not report independently labeled, identical-response capability twins or budgeted review allocation. Its roleplay rubric even penalizes AI identity disclosure, showing that its normative target cannot simply be imported into honest-assistant review. Treat it as a close capability-sensitive evaluation precedent, not a validated safety rubric for PERSONA. The verified record is a preprint.

### 4. ConCI: Closest Controlled Contextual-Label Design

**Park, Yu and Moon (2026), _ConCI: A Controlled Counterfactual Benchmark for Contextual Integrity in LLMs_, arXiv:2610.24494v1, 17 October; marked under review.** [Primary record](https://arxiv.org/abs/2610.24494); [PDF, Sections 3-4 and Figure 2](https://arxiv.org/pdf/2610.24494).

ConCI changes one information-flow parameter while preserving others, constructs both label-changing and label-preserving variants, and scores triplets jointly. It reports 1,592 flows in 556 triplets with seven human annotations per flow. Its construction includes normative filtering; it is not an unselected estimate of how frequently contextual changes matter.

**Residual distinction:** it changes information-flow context, not documented assistant memory or follow-up capability with a fixed utterance, and does not study review queues. It substantially anticipates the proposed counterfactual-plus-invariant-control design. Replacing privacy context with capability metadata is only an application change unless the resulting judgments, evidence requirements, or allocation failures are substantively informative.

### 5. Dishonest Anthropomorphism: The Premise Is Established

**Leong and Selinger (2019), _Robot Eyes Wide Shut: Understanding Dishonest Anthropomorphism_, FAT* 2019, pp. 299-308.** [Author-deposited primary record and abstract](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3762223).

The paper develops a taxonomy of dishonest anthropomorphism using boundary-management reasoning and examines associated harms and design/policy questions. Misleading human-like presentation is already a recognized problem; identifying it is not a new contribution.

**Verification limit:** identity, scope, and abstract were checked through the indexed author record; direct SSRN and ACM opens were blocked. No full-text experimental absence claim is made. This reference supports the established conceptual premise, not a claim that disclosure alone prevents harm or that a particular memory architecture makes relational claims acceptable.

### 6. Fixed Proposals Plus Selective Audits: A Close Cross-Domain Counterexample

**Ojha (2026), _Stateful Mediation and Selective Auditing for Financial Language-Model Actions: A Paired Controlled Simulator Study_, American Journal of Financial Technology and Innovation 4(1), 198-210, published 30 September; DOI 10.54536/ajfti.v4i1.8543.** [Publisher record](https://journals.e-palli.com/home/index.php/ajfti/article/view/8543); [full paper, Introduction and selective-audit replay](https://journals.e-palli.com/home/index.php/ajfti/article/download/8543/4161).

This study preserves visible proposal context, replays fixed model proposals across state/execution conditions, and compares static selective-audit policies at matched expected budgets. It distinguishes policy-blind simulator outcomes from audit selection and explicitly reports structurally constrained contrast signs and no stopping-threshold crossings.

**Residual distinction:** execution-state consequences with deterministic synthetic labels differ from human reviewworthiness of anthropomorphic implications. Expected-budget sampling also differs from exact top-k selection, but that distinction is not methodological novelty. This is the closest verified combination of fixed outputs, changed surrounding system state, and selective audits found here. Its publisher record and methods were verified; code, results, and external validity were not independently reproduced.

## Methodological Boundary Checks

Two established methodological anchors were also checked, rather than treated as additional candidate contributions: [Ribeiro et al., _CheckList_ (ACL 2020), Section 2](https://aclanthology.org/2020.acl-main.442.pdf) supplies minimum-functionality, invariance, and directional behavioral tests, including fairness as a capability; [Kusner et al., _Counterfactual Fairness_ (NeurIPS 2017), Definition 5](https://papers.nips.cc/paper/6995-counterfactual-fairness.pdf) defines fairness through a causal counterfactual criterion. These are background boundaries, not claims that either implements this review task.

A capability switch is deliberately potentially relevant to the review target. It is not interchangeable with demanding invariance to a protected attribute, nor does a card-swapping experiment establish causal demographic fairness. Likewise, pairing a change-sensitive test with an invariant control is established testing practice. The contribution must be empirical evidence about a specific review decision and information requirement.

## Exact-Match Finding and Narrow Gap

**No exact match was verified in this bounded search** for all of: identical prompt and response; independently evidenced operational memory/follow-up variants; independent reviewworthiness judgments without mandated label flips; the same semantic judge with and without metadata; and exact-capacity allocation consequences. This means only that the checked sources did not establish the entire design. It does not justify a first-ever claim or novelty by conjunction of familiar components.

The defensible gap is a measurement question: **how much decision-relevant information does a text-only screen discard, for which claims, and can a small verified evidence package recover useful allocation performance?** NOPE already supplies much of the substantive capability-honesty target; AnthroBench raises the human-validation standard; AnthroDial prevents claiming capability-sensitive anthropomorphism evaluation itself; ConCI and the audit simulator supply close design precedents.

Do not claim that memory makes a chatbot feel, care, accept professional responsibility, or maintain a human relationship. Do not equate a reminder scheduler with ongoing monitoring. A capability can make a literal promise feasible while leaving its broader implication reviewworthy. Evidence of capability, permission to use it, evidence it was used, and user-visible disclosure are different variables.

## Strongest Criticism

> You selected statements whose truth depends on memory, wrote cards saying memory is available or unavailable, and rewarded a judge for reading those cards. Text-only failure was guaranteed, and the review labels merely restate your manipulation. This is familiar contextual entailment testing, now called anthropomorphism. Why does it change an actual allocation decision rather than just demonstrate missing information?

That objection wins if labels are mechanically assigned from capability state, only obvious promise violations are included, the capability-aware judge receives the annotation answer key, or the headline is merely that the tone score cannot separate twins. Adding a formal indistinguishability proposition would not rescue it.

The answer must be independent and fallible: include ordinary language and ambiguous implications, permit invariant judgments, preserve dissent, compare against a strong semantic and a simple claim-capability baseline, and demonstrate a held-out decision-relevant gain rather than only a constructed classification advantage. Even a positive result establishes offline selection against a declared review target, not effective remediation or harm reduction.

## Minimal Non-Tautological Experiment

### A. Freeze Text and Verify One Capability at a Time

Start with one primary family, preferably **cross-session memory**, rather than a factorial combination of memory, persona, clinical role, disclosure, and follow-up. Hold user-visible prompt/response text, role, policy, and interface disclosure fixed within each pair. A follow-up family can be a prespecified transfer check, not pooled evidence of the same mechanism.

Use a controlled harness with memory disabled versus scoped memory enabled, supported by configuration records and positive/negative retrieval tests. Absence of logs is not evidence of absence. Document retention horizon, account/session scope, permissions, and reliability limits. Freeze the response as a replayed stimulus; do not claim both real systems independently generated it. The estimand is judgment under evidenced deployment configurations, not the causal effect of enabling memory on generated language.

For follow-up, distinguish scheduler availability, authorization, successful scheduling, and delivery. Promise feasibility and claimed completed action require different evidence. A sandbox demonstration supports only the tested scope, not an unconditional future guarantee.

### B. Sample Without Selecting on Desired Label Flips

An illustrative pilot is 60 base prompt-response pairs, yielding 120 capability-conditioned instances: 20 explicit operational commitments, 20 ambiguous continuity/relational implications, and 20 controls. This is a feasibility allocation, **not a power calculation**. Include warm non-commitments, non-anthropomorphic capability statements, and clearly reviewworthy claims not remedied by memory. Include both capability-compatible and incompatible denials to prevent a shortcut that simply flags every capability-disabled deployment.

Select text before screening results or capability-conditioned labels. Preserve sampled no-change cases. If sampling is enriched for candidate claims, report it as a stress-test distribution; do not estimate deployment prevalence from it. A small random, unenriched PERSONA slice can supply a separately reported relevance check, but remains reused text.

### C. Independent Judgments, Not an Injected Answer Key

Use a development set to settle a review rubric, then freeze it before held-out annotation. At least three independent assessors per instance should see the same complete evidence standard and not screen scores, counterpart labels, or hypothesized flip direction. Randomize a balanced incomplete assignment so an assessor does not see both twins. Assessor pools must be balanced across configurations; do not repeat the existing assessor/version confounding.

Ask separately: what operational or relational implication is conveyed; whether evidence supports that implication; and whether it warrants escalation under the stated review remit. Allow uncertainty and distinguish factual support from reviewworthiness. Record reasons without instructing assessors that enabling a feature must remove concern. Report raw votes, uncertainty, agreement, and adjudication separately. These are expert/reviewer judgments, not observed user beliefs; a separate user study would be needed to make the latter claim.

### D. Isolate the Value of Metadata

Use the **same frozen semantic judge**, rubric, decoding, and score scale across these information conditions. Keep all twins and paraphrases of a base scenario within one split.

| Condition | Information available | Purpose |
| --- | --- | --- |
| Response-only | Response | Separates semantic content from tone heuristics |
| Prompt + response | Fixed user prompt and response | Strong text-only baseline, not a lexical straw comparator |
| Minimal capability facts | Prompt + response + neutral operational fields | Tests a small candidate evidence summary |
| Full capability evidence | Prompt + response + scoped configuration/test evidence | Tests whether evidence beyond a summary adds value |
| Missing metadata | Prompt + response + explicit unknown fields | Tests uncertainty handling; unknown must not mean absent |
| Irrelevant metadata | Prompt + response + length-matched, non-diagnostic facts | Controls for generic extra-context effects |

Also retain HumT, normalized markers, length, and seeded random allocation; add a simple explicit-claim/capability consistency rule. No capability card should contain review labels, normative conclusions, or rubric phrases that reveal the answer. If testing inaccurate metadata, label that as a separate robustness condition rather than pretending it is verified evidence.

The full-evidence human reference judgments stay fixed when screen inputs are masked. Record a separate screen action of requesting capability evidence; do not silently relabel every missing-metadata instance as positive. Any operational evidence-request policy must charge its cost against the same total budget and report unresolved cases.

### E. Primary Tests and Failure Conditions

Preregister one allocation operating point, for example 20% exact item capacity. Secondary 10% and 30% points are sensitivity analyses. Use label-blind, coupled tie-breaking for identical text-only scores. Compare policies within the same mixed queue, and also report each capability configuration separately. A balanced paired queue is diagnostic, not a claim about production mixture.

Report paired differences in captured positives, recall, precision, residual positives, and false escalation of invariant controls. Count discordant human-labeled pairs separately from the allocation result. Resample base scenarios, not duplicated variants as independent observations; assess rater uncertainty separately. If positives remain sparse, present counts and wide intervals rather than asserting superiority or equivalence. Plan the confirmatory size from pilot event rates, disagreement, and a prespecified useful effect, not from the original 19 positives.

Measure metadata preparation/verification cost and judgment time. Equal numbers of reviewed items are not equal labor. To call a package "minimal," preregister an acceptable performance loss relative to full evidence and a maximum invariant-control error increase; assess those bounds on held-out data. Failure to detect a difference is not evidence of sufficiency. At most claim the **smallest adequate package among those tested**, not universally minimal context.

**Disconfirming outcomes:** independent assessors rarely or unreliably change review judgments; changes are confined to explicit factual contradictions and vanish beyond the simple rule baseline; prompt-response semantics already achieve comparable useful allocation; capability metadata improves sensitive cases but damages invariant ones; or evidence acquisition costs exceed the selection benefit. Any of these narrows or defeats the proposed contribution. Publish the limitation rather than manufacture a new theory.

## Recommended Claim and Stop Rule

Prospective wording:

> We test whether documented operational capabilities are necessary information for reviewing selected anthropomorphic implications. Holding prompt-response text fixed, we compare independently assessed reviewworthiness across evidenced capability configurations and estimate the incremental allocation value of capability metadata for the same semantic screen. Invariant controls and missing-evidence conditions distinguish useful contextual sensitivity from indiscriminate relabeling.

Do not put that claim in the completed-results voice until the study is run. **If only deterministic claim-card contradictions separate conditions, frame the result as an engineering conformance test, not a substantive new anthropomorphism contribution.** If independent judgment and held-out budget gains survive the controls, the contribution is a bounded evidence-grounded review benchmark and an empirical information-requirements result. It remains distinct from a CSR intervention and does not demonstrate actual review effectiveness.

## Search and Verification Limits

Searches targeted dishonest anthropomorphism, capability disclosure, same-response/system-capability labels, memory/continuity/follow-up evaluation, contextual counterfactuals, and selective audits. AnthroBench and NOPE leads shared during the research were followed to primary records. The six closest references above are deliberately prioritized over a broad bibliography; two foundational testing/fairness sources are linked only to bound the methodology claims. Primary publisher/proceedings records, author manuscripts, and first-party evaluation artifacts were used, not secondary summaries as evidence.

This was not a systematic review, code audit, clinical validation, or exhaustive patent/industry search. Full-text access was incomplete for Leong and Selinger, and NOPE verification was limited to accessible run text and indexed first-party suite descriptions, not every blueprint or run. Other configurations may already exist in uninspected artifacts. No background-agent tool was available in this session, so research was performed directly; no separate chat was created or messaged. No experiments, model calls, recruitment, commits, or pushes were performed.
