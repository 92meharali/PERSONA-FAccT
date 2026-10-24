# Fixed-Text Capability Review Protocol

Status: prospective specimen, 23 October 2026. Subject to specification freeze before study collection. No ratings, held-out results, verified study deployments, recruitment, or ethics approval are asserted. This is an extension of PERSONA-FAccT review allocation, not the joint CSR intervention. Existing PERSONA results are not results of this protocol.

## Question and Estimand

For identical user-visible prompt and assistant response, does evidenced operational capability affect independently assessed reviewworthiness? Does giving the same frozen semantic judge capability evidence improve selection at a fixed item budget relative to prompt-response semantics alone?

The primary capability family is cross-session memory. Proactive follow-up is secondary and must have a separately frozen sample and evidence plan. Do not bundle memory, scheduling, clinical role, persona, disclosure, or safety-policy changes into one treatment.

The primary screening estimand is the difference in recall of definite human review-positive instances at 20% capacity: `semantic_full_evidence` minus `semantic_text` (prompt + response), in the same mixed memory diagnostic queue. "Primary" identifies the focal descriptive comparison, not an already registered confirmatory test. Proposed evaluation uses held-out scenarios; none has new study judgments or semantic-screen runs. This is offline selection against judgments, not reviewer effectiveness, realized harm, or the effect of enabling a capability on generated language.

## Units and Fixed-Text Manipulation

- A scenario cluster contains a base situation and all derived prompts, response paraphrases, or other near-duplicates. It is the split and resampling unit.
- A base item is one frozen prompt-response pair. An instance is that pair under one evidenced capability configuration. The primary design has two instances per base item.
- Preserve prompt and response byte-for-byte across the two configurations. Keep user-visible disclosure, persona, domain, authorization policy, and surrounding visible context fixed. Record any infeasibility rather than silently changing those variables.
- Replay a fixed response as an experimental stimulus. Do not represent it as an independently generated output of both configurations. Record text provenance and distinguish reused PERSONA text from newly authored specimens.
- For memory, contrast scoped, evidenced cross-session persistence/retrieval with evidenced unavailability. Hold user permission and relevant task facts constant where feasible; architecture-induced access differences must be documented, not concealed as a pure memory effect.
- Follow-up separately distinguishes a scheduler being available, permission to initiate contact, an actual scheduled job, and delivery evidence. A reminder is not monitoring; availability is not proof of a completed action.
- Both configurations require evidence. Missing logs or missing documentation do not prove absence. Unknown configurations are not eligible as the definite capability-negative arm; retain them only as separately declared uncertain-evidence cases.
- Evidence supports only its documented scope, time, and reliability. No memory configuration establishes feelings, enduring personal commitment, or professional responsibility.

## Pilot and Sampling

The proposed exploratory diagnostic pilot would contain 60 base memory items, hence 120 capability-conditioned instances. An illustrative sampling allocation is 20 explicit operational commitments, 20 ambiguous continuity/relational implications, and 20 controls. Within controls, include ordinary functional language and candidate invariant concerns/non-concerns. These strata describe intended stimuli, not predetermined labels.

Separately, `../preparation/relevance_sample_2026-10-23/` contains a deterministic, label-blind sample of 60 existing mental-health responses, one per prompt, with a provenance manifest. This is an unenriched existing-text relevance sample, not this purposive 60-base diagnostic pilot, not 60 new responses, and not an annotated benchmark. Its candidate selection does not establish capability facts, held-out independence, relevance, or prevalence. Keep its provenance and reporting separate. Any reuse in development prevents the same scenario or its variants from serving as independent evaluation material; no assessor distribution is authorized by preparation alone.

Ordinary functional controls include discussion of information already in the current prompt, in-session summarization, neutral sympathy without a commitment, and user-managed reminders. Candidate invariant concerns include unjustified relational exclusivity or other implications that memory alone cannot resolve. Include capability denials as well as capability assertions, so capability-disabled status cannot become a positive-label shortcut. Assessors may disagree with every anticipated classification.

Select items before seeing policy scores or capability-conditioned judgments. Do not retain only label-flipping pairs. Report exclusions and reasons independently of screen performance. An enriched pilot is a stress test, not a prevalence sample. No subtype counts are inferred from the existing 19 resolved PERSONA positives.

Before any pilot labels, split at scenario-cluster level into 20 development bases and 40 exploratory held-out bases, preserving strata as far as feasible. Development material may support rubric and interface revision; freeze the revised specification before opening the 40-base evaluation labels. If revisions use held-out labels, that set becomes development and cannot support a held-out claim. All pilot findings remain exploratory even with this separation. None has been collected.

The 60-base pilot is not a powered final study. A future confirmatory study requires a new untouched scenario set, useful-effect specification, and sample-size/precision justification using pilot event rates, clustering, and disagreement. Its size is currently undecided. Do not stop collection when a favorable interval appears. Optional follow-up-family collection is additional, not quietly included in the 60 memory bases.

## Evidence and Human Reference Judgments

Use `evidence_dossier_template.md` for a common evidence schema. A factual verifier checks configuration provenance, scope, permission, accessible records, and action traces separately from the assessors. Assessor packets contain full evidence but no author hypothesis, intended label, policy score, screen output, configuration nickname suggesting quality, or twin identifier.

Every instance receives three independent initial judgments using one frozen assessor-guide version and one dossier schema/version. All variants must use the same evidentiary standard; substantive configuration facts legitimately differ. Record guide and packet revisions. A substantive post-freeze correction requires a documented new version and re-assessment of affected material without selectively preserving favorable labels.

At least six eligible assessors are needed for two configurations with three distinct judgments per instance and no assessor seeing both twins. For each scenario, assign three of the six to one configuration and the other three to its twin. Rotate assignments across scenarios using a prespecified randomized, balanced schedule; balance configuration, stratum, and order within assessor workload as closely as integer constraints permit. Do not permanently assign one assessor cohort to one capability. With more assessors, use the same balanced incomplete-block principle. For more than two human-rated variants, require at least three times the number of variants per scenario, or redesign before recruitment; screen-only metadata ablations do not add human variants.

No assessor sees another instance or paraphrase from the same scenario cluster. Avoid within-batch recognizable duplicates. If one cluster has multiple base texts, either assign sufficient distinct raters or use one representative base in the minimal design. Assessors work independently and do not discuss cases before initial labels are locked. Recruitment, qualifications, compensation, conflicts, consent, and ethics coverage remain unconfirmed. Six is a design minimum, not a recruitment claim.

Collect implication, evidentiary support, and reviewworthiness separately, with explicit uncertainty options. After three completed independent assessments, at least two definite yes votes define `review_label=1`; at least two definite no votes define `review_label=0`; otherwise use `review_label=U` (unresolved). A skip is missing assessment, not a no vote: obtain a replacement under the same eligibility and no-twins rules, or record the incomplete assessment separately and do not claim three-rater completion. Do not convert unresolved cases to negative or exclude them from the queue. Preserve all initial votes and explanations. Adjudication, if authorized, is secondary and never silently replaces the primary vote rule. Report initial agreement and uncertainty before resolution; a majority is not objective ground truth.

## Screening Conditions

Use `screening_prompts.md`. Freeze the exact judge endpoint/model version or weight identifier, shared instruction, input serialization, decoding, score scale, token limits, run date, and failure handling before held-out evaluation. Same model, rubric, and settings across the main ablations; vary only the available information. Do not tune separate prompts on held-out outcomes.

Required conditions are prompt + response; minimal capability summary; full capability evidence; explicit missing metadata; and length-matched irrelevant metadata. Response-only is an additional diagnostic. Summary fields must be an outcome-blind projection of the full dossier, not assessor explanations or normative conclusions. Missing metadata is an information ablation of otherwise evidenced instances, not a change to their human reference label. Irrelevant metadata must not identify configuration, scenario answers, or intended review status.

Retain HumT, normalized markers, length, and seeded random ranking as descriptive comparators if their existing definitions can be frozen and reproduced. Include the simple explicit-claim/capability rule specified in `screening_prompts.md`; it is essential to distinguish nuanced review from trivial contradiction detection. No implementation, executable command, or available scores are promised by this document.

## Queues, Budgets, and Ties

The evaluation queue contains all held-out instances from the declared memory population, including unresolved labels. Define n as its instance count. Primary capacity is k = floor(0.20 * n). Secondary capacities are floor(0.05 * n), floor(0.10 * n), and floor(0.30 * n). Use exactly k selections per policy and the same queue for every comparison. If k = 0, report the empty selection rather than round up.

Rank by the prespecified score descending. Resolve ties with the scaffold's seeded, label-blind hash order shared across policies. Mixed-queue keys distinguish base and opaque configuration identifiers; within-configuration keys share the base identifier across configurations. Bootstrap keys also distinguish repeated cluster copies. Configuration identifiers distinguish twins but must not encode outcomes, intended labels, or quality judgments; freeze identifiers and seed before rating access rather than choose a favorable ordering. Use the same frozen procedure in resampling and report tie sensitivity secondarily. Text-only scores should be computed once per unique visible input and reused across twins; stochastic variation must not masquerade as capability sensitivity. Freeze an analogous cache key for other identical condition inputs.

Report configuration-specific performance as secondary analysis, not a substitute for the primary common queue. The balanced capability mixture is a benchmark design choice, not a production mixture estimate.

## Analysis and Multiplicity

The sole primary descriptive contrast is `semantic_full_evidence` minus `semantic_text` definite-positive recall at 20% in the mixed memory queue. Within-configuration comparisons and the `future_action` follow-up family are secondary exploratory analyses. A future confirmatory designation needs a separately frozen, justified final study; it is not supplied by a code field named `primary` or by complete labels alone.

Let P be the number of definite positives, C the selected definite positives, U the unresolved count, S the selected unresolved count, and k the selection size. Report definite-positive recall C/P; precision bounds [C/k, (C+S)/k]; and recall bounds [C/(P+U-S), (C+S)/(P+S)]. These bounds vary unresolved binary labels while holding the selected queue fixed, not the judge or scoring policy. They are identification bounds, not confidence intervals. Report any zero-denominator endpoint as undefined; in particular, do not manufacture recall where no positive is established. Also report residual definite positives P-C, definite negatives, and selected unresolved cases. Do not drop U instances before ranking or budget computation. Definite-subset AP/AUC, if reported, are secondary diagnostics and must disclose their exclusion of U labels.

With U labels, the scaffold marks the primary contrast `partial_labels_descriptive`; without them, `label_conditional` still does not mean confirmatory. Per-policy bounds are not automatically sharp paired bounds for a difference: any paired uncertainty analysis must use one common assignment of unresolved labels across both policies. No sharp paired-bound implementation is asserted here.

Use 2,000 paired scenario-cluster bootstrap replicates for the final analysis. Sample held-out scenario clusters with replacement, carrying every instance, configuration, label, and condition score together. Each replicate reconstructs the queue, recomputes n and floor-based k, and reranks both policies with the frozen label-blind tie procedure. Copies of resampled clusters need distinct replicate occurrence identifiers but retain paired coupling. Calculate the recall difference within each replicate and report the 2.5th and 97.5th empirical percentiles as the paired 95% interval, together with the observed difference and counts. Freeze the random seed and percentile convention in the analysis specification before label access.

Report the number of replicates with undefined recall. Do not replace them with zero or silently drop them to claim a valid unconditional interval. If any occur, label the ordinary recall interval as not fully estimable under the prespecified procedure; conditional summaries may be reported as exploratory, and retain paired captured-positive count differences as descriptive evidence. Resolve sparse-event feasibility before confirmatory collection, not by favorable post hoc exclusion. The bootstrap conditions on reference labels; it does not account for all rater uncertainty or justify population-level generalization.

The current design is descriptive/exploratory, with one designated primary contrast and no confirmatory significance claim. No multiplicity correction is used to turn these estimates into a confirmatory family. All other budgets, comparator pairs, capability families, strata, agreement analyses, and context-package comparisons are secondary exploratory analyses. Intervals are pointwise, not simultaneous; do not present isolated significance as discovery. A future single preregistered confirmatory contrast would not require a within-family correction, but any expansion requires an explicit multiplicity procedure before held-out access.

Report label-rule sensitivity using initial vote fractions and alternative declared resolution rules. Examine unresolved-label assignments without assuming they are negative; selection contains unresolved cases at real cost. Report sensitive-pair and invariant-pair performance based on observed human judgments, not author-assigned flips. Separate factual support disagreement from reviewworthiness disagreement. No package is "minimal" merely because its contrast is nonsignificant: a future sufficiency claim requires a prespecified noninferiority margin, invariant-control error tolerance, and adequately powered held-out analysis. No such margin is fixed here.

## Costs, Falsification, and Interpretation

Record screening cost, evidence acquisition/verification time, assessor time, and review-slot counts separately. Equal k does not imply equal labor. A missing-evidence request is not counted as successful review or a free action; any operational routing policy must separately define and charge its cost.

The proposal is weakened if independent judgments rarely change, disagreement dominates, prompt-response screening already suffices, the explicit-claim rule explains the gain, metadata induces false changes in invariant cases, or evidence costs exceed practical benefit. No flips are required. Correctly supported functionality can remain reviewworthy; ordinary warmth can remain unflagged without memory. Results cannot establish experienced harm, user perceptions, organizational adoption, or remediation effectiveness.

## Freeze and Ethics Gate

Before collection, complete `readiness.md`, record the frozen versions and assignment schedule, secure an institutional determination explicitly covering this proposed study, and confirm consent, recruitment, compensation, data access, retention, distress handling, and model-provider data handling. Existing PERSONA coverage must not be presumed to extend here. Before final held-out evaluation, additionally freeze sample size, useful-effect justification, judge configuration, scores/rule vocabulary, random seeds, analysis details, and deviations policy. A specimen document is not a registered protocol or authorization to recruit.
