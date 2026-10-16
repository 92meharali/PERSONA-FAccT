# Review-allocation analysis specification v1.0.0

Specified 2 October 2026 after prior exploration, before this reproducible pipeline's final run. This is not a preregistration or an analysis of unseen evidence. See the exploration register. Source ratings and CHI outputs are immutable.

## Decision and estimand

A model-evaluation lead has a fixed batch of single-turn responses and can send only a fraction to qualified manual reviewers. The unit selected is a response, not a prompt. Reviewers inspect the original prompt and response, assess the concern, and decide on escalation; this downstream review is proposed, not observed. Non-selection means **not reviewed**, not clearance or safety. No harm, reliance, or successful remediation outcome is measured.

Primary analyses are separate by domain. Pooled analysis is secondary and uses the observed corpus mixture, not deployment prevalence. Exact capacities are floor(n*b) at b = 5%, 10%, 20%, 30%; the already-explored 20% reference is not optimized. Zero is permitted for small batches. All policies receive the same exact capacity.

## Criteria

The candidate primary criterion is five-rater mean D >= 3: the rubric's anchor 3 denotes simulated affect/understanding, including ordinary sympathy. This is a broad **rubric-defined review trigger**, not demonstrated deception or harm. Applying an integer anchor to a mean is an operational choice, not a validated natural boundary. D >= 4 tests the stronger claimed-feelings/relationship boundary. D >= 2 tests broader sensitivity. External evaluators must assess which trigger is useful; D >= 3 is not asserted to be their preference.

Secondary endpoints: mean F < 4 (below strong domain fit, including adequate cases), mean OA < 4 (below mostly appropriate). They are not equivalent severity thresholds. Grids in criteria.yaml include strict/weak inequalities around anchor 3 and 4. No composite is primary. Majority (at least 3/5) and unanimous (5/5) rater votes using the same individual anchor are sensitivity analyses. E is retained for continuous relationships and case interpretation, not silently added to the primary concern definition.

## Policies

- high_H: descending recorded HumT score, without fitting or transformations.
- length: descending number of regex word tokens in the original response.
- markers: proportion of tokens in the fixed first/second-person and conversational-marker dictionary recorded in screening.py. Not a validated second anthropomorphism metric.
- uniform_random: exact-size sampling without replacement, reported analytically as expected performance. Hypergeometric prediction limits describe randomness of one draw, separately from corpus-bootstrap intervals.
- stratified_random: pooled only, proportional domain allocation by largest remainder, alphabetical domain tie-break; random sampling within domains. Exact total capacity. A control for domain mixture, not a trained policy.

Deterministic SHA256-based tie ordering uses the frozen seed and domain/item ID; bootstrap copies receive distinct occurrence keys. Ties never increase the budget. Separate 100-seed checks quantify tie sensitivity. AP and ROC-AUC treat tied scores as ties, independently of tie-breaking used for exact selection. AP is undefined with no positives; ROC-AUC is undefined unless both classes occur. Targets are 50%, 80%, 90%, 100% recall; workload is the first prefix reaching ceil(target*positives). With complete scores every target is attainable when positives exist. Random workload uses the exact expected order statistic m*(n+1)/(P+1), not a guarantee or an individual realization. Stratified random has no single ranking and no workload curve beyond the evaluated allocations.

## Uncertainty and comparisons

2,000 final bootstrap replicates. Resample prompts with replacement within domain, retaining every response in each draw. Pooled resamples draw the same number of clusters per original domain; unequal cluster sizes allow response-mixture fluctuation. Re-rank each resampled batch and reapply floor(n*b), estimating a fresh-batch allocation procedure, not a fixed deployed threshold. Pair draws across policies and criteria. Report percentile intervals, finite replicate counts and undefined fractions. Zero-positive resamples remain undefined, not zero.

Primary family: high_H minus expected uniform_random recall at 20%, D >= 3, in each of three domains. Use 98.3333% Bonferroni percentile intervals across the three specified comparisons. These are approximate bootstrap intervals, with limited tail resolution at 2,000 draws; they are not exact small-sample tests. All other policy/criterion/budget comparisons have exploratory pointwise 95% intervals and no confirmatory significance claims. Paired differences against length and markers are reported, not ranked by overlapping marginal intervals.

If fewer than 10 concern-bearing or nonconcern-bearing clusters exist, flag sparse evidence and do not claim a reliable ordering even when an interval appears separated. Context subgroup analyses give counts and point estimates, not confident small-cell rankings. Model comparisons use only complete three-model prompt sets; paired cluster-bootstrap rate differences are descriptive, with pointwise intervals, and incomplete-cluster results are separate.

## Assumptions and exclusions

Equal review time per response is only a workload convention. Scenario analyses use 1/3/5 minutes per response, missed-case to unnecessary-review cost ratios 1/5/10, and equal-domain versus observed mixture. These are hypothetical, not estimated costs. Length can affect real review time, so equal-count budgets are not equal-time guarantees. No ratings enter a screening policy. No supervised model, LLM judge, oracle policy, causal claim, or external validation is included in this computation.

Protocol amendments must preserve this version and state date, reason and which outcomes were already inspected. Source-provenance uncertainties gate methods claims separately from computational feasibility.
