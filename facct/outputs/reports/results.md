# Screening simulation results

Exploratory reuse of PERSONA. 2,000 paired prompt-cluster bootstrap replicates; computational runtime 55.9 seconds before report/manifest finalization.

## 20% reference budget

Intervals below are pointwise 95%, not simultaneous. Random recall is an exact expectation at the same integer budget, not one sampled draw.

| Domain | Criterion | Selected / n | Caught / concerns | Recall (95% CI) | Expected random recall | Difference (95% CI) | Missed |
|---|---|---:|---:|---|---:|---|---:|
| education | D_ge3 | 83/415 | 7/12 | 0.583 [0.167, 0.909] | 0.200 | +0.383 [-0.032, +0.711] | 5 |
| education | F_lt4 | 83/415 | 10/25 | 0.400 [0.188, 0.600] | 0.200 | +0.200 [-0.012, +0.401] | 15 |
| education | OA_lt4 | 83/415 | 9/18 | 0.500 [0.235, 0.737] | 0.200 | +0.300 [+0.037, +0.537] | 9 |
| health | D_ge3 | 83/415 | 10/23 | 0.435 [0.240, 0.652] | 0.200 | +0.235 [+0.042, +0.454] | 13 |
| health | F_lt4 | 83/415 | 25/120 | 0.208 [0.136, 0.272] | 0.200 | +0.008 [-0.063, +0.073] | 95 |
| health | OA_lt4 | 83/415 | 3/9 | 0.333 [0.000, 0.701] | 0.200 | +0.133 [-0.199, +0.502] | 6 |
| mental_health | D_ge3 | 132/660 | 42/165 | 0.255 [0.192, 0.321] | 0.200 | +0.055 [-0.008, +0.121] | 123 |
| mental_health | F_lt4 | 132/660 | 18/95 | 0.189 [0.122, 0.276] | 0.200 | -0.011 [-0.078, +0.076] | 77 |
| mental_health | OA_lt4 | 132/660 | 31/133 | 0.233 [0.176, 0.306] | 0.200 | +0.033 [-0.024, +0.106] | 102 |

## Primary comparison family

D >= 3 only, high_H minus expected uniform random recall at 20%. Bonferroni 98.3333% percentile intervals across three domains; already-explored data and approximate intervals prevent confirmatory claims.

- education: +0.383, adjusted interval [-0.198, +0.801]; 7 concern-bearing clusters. Sparse flag: True.
- health: +0.235, adjusted interval [+0.001, +0.505]; 15 concern-bearing clusters. Sparse flag: False.
- mental_health: +0.055, adjusted interval [-0.020, +0.138]; 99 concern-bearing clusters. Sparse flag: False.

## Simple baselines

Paired pointwise 95% intervals for the difference in recall (HumT minus baseline), D >= 3 at 20%:

- education: versus length +0.333 [-0.111, +0.750]; versus markers -0.167 [-0.500, +0.167].
- health: versus length +0.217 [+0.000, +0.471]; versus markers -0.478 [-0.632, -0.259].
- mental_health: versus length -0.073 [-0.148, +0.018]; versus markers -0.127 [-0.219, -0.043].

## Interpretation and limits

These estimates concern review allocation for existing rubric judgments, not user harm or successful interventions. Useful enrichment and missed cases can coexist. Domain fit, anthropomorphic implication risk, and holistic appropriateness are separate criteria. The data do not establish real organizational use of HumT screening.

screening.csv includes precision, missed counts, unselected prevalence, AP/AUC, target-recall workload, uncertainty and valid replicate counts. random_draw_intervals.csv reports hypergeometric variability for one random draw, not an uncertainty interval for expected random performance. Bootstrap intervals are conditional on the fixed released ratings; rater/threshold sensitivities are separate.

Sensitivity tables include anchor thresholds, 3/5 and 5/5 votes, individual raters, tie seeds, join provenance, conditions/scenarios/models, exact criterion intersections, and continuous relationships. Context point estimates are descriptive; small cells do not justify rankings. Model comparisons restrict primary pairings to complete three-model prompts. Mixtures and review-cost ratios are hypothetical.

## Decision gates

1. Computational feasibility: passed for the released corpus. Historical provenance is only provisionally linked: matching repository supplement bytes and manuscript numbers do not authenticate what was submitted. Resolve collection-history/payment records and confirm the submitted supplement before definitive methods claims.
2. Scientific value: the screening question is computable and can reveal useful criterion-specific enrichment; assess all baselines and sensitivities, not only comparisons favorable to HumT.
3. New contribution: not yet established as an independent paper. This is the same corpus and concern constructs as CHI. External evaluation and a tested decision artifact remain pending. Treat the current package as a methods-study candidate, not proven submission novelty.
4. Eligibility: no self-certification. Official policies and any written chair guidance must govern. No communication or submission has been sent.
