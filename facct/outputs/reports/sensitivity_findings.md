# Supporting sensitivity and workload findings

All sensitivities are exploratory and were specified before this pipeline's final run, on already explored data. Unless stated otherwise, sensitivity tables give point estimates without bootstrap intervals; do not treat their ordering as robust significance.

## Stronger D trigger at the same 20% capacity

- education: 8 cases in 5 concern-bearing prompts, 3 selected, recall 0.375. Sparse strong-trigger cases prevent a confident comparative claim.
- health: 8 cases in 6 concern-bearing prompts, 2 selected, recall 0.250. Sparse strong-trigger cases prevent a confident comparative claim.
- mental_health: 5 cases in 4 concern-bearing prompts, 0 selected, recall 0.000. Sparse strong-trigger cases prevent a confident comparative claim.

This shows why D >= 3 enrichment must not be generalized to every severity threshold. Zero captured cases in a small severe-label cell is reported, not evidence that all severe cases are missed in deployment.

## Rater-consensus changes (D)

- education, at least 3/5 votes: 12/22 selected concern cases; recall 0.545.
- education, at least 5/5 votes: 7/12 selected concern cases; recall 0.583.
- health, at least 3/5 votes: 11/24 selected concern cases; recall 0.458.
- health, at least 5/5 votes: 6/17 selected concern cases; recall 0.353.
- mental_health, at least 3/5 votes: 48/200 selected concern cases; recall 0.240.
- mental_health, at least 5/5 votes: 39/150 selected concern cases; recall 0.260.

## Full-text/embedded join sensitivity (D)

- education: exclude 56 prefix/fuzzy rows for this sensitivity only; 71/359 reviewed; 6/12 concerns selected, recall 0.500.
- health: exclude 3 prefix/fuzzy rows for this sensitivity only; 82/412 reviewed; 10/23 concerns selected, recall 0.435.
- mental_health: exclude 0 prefix/fuzzy rows for this sensitivity only; 132/660 reviewed; 42/165 concerns selected, recall 0.255.

The main analysis keeps all released rows. Exact-text joins are not independently authenticated IDs, and this sensitivity changes the batch rather than proving excluded joins incorrect.

## Tie sensitivity

- health, D_ge3, length: caught counts range 4-5 across 100 seeded tie resolutions.
- health, F_lt4, length: caught counts range 25-27 across 100 seeded tie resolutions.
- mental_health, D_ge3, length: caught counts range 50-55 across 100 seeded tie resolutions.
- mental_health, F_lt4, length: caught counts range 17-20 across 100 seeded tie resolutions.
- mental_health, OA_lt4, length: caught counts range 25-30 across 100 seeded tie resolutions.

Cells not listed above had identical caught counts across the 100 tested seeds; this is not an exhaustive enumeration of all possible ties.

## Review workload to reach 80% of D-trigger cases

Fractions below describe this corpus with its known labels; they are retrospective evaluation, not a deployable calibrated stopping rule.

- education, high_H: 0.376 of batch [0.092, 0.837] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- education, length: 0.677 of batch [0.290, 0.964] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- education, markers: 0.239 of batch [0.099, 0.381] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- education, uniform_random: 0.771 of batch [0.668, 0.802] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- health, high_H: 0.463 of batch [0.285, 0.614] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- health, length: 0.834 of batch [0.705, 0.930] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- health, markers: 0.152 of batch [0.098, 0.329] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- health, uniform_random: 0.794 of batch [0.752, 0.802] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- mental_health, high_H: 0.708 of batch [0.641, 0.773] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- mental_health, length: 0.661 of batch [0.586, 0.738] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- mental_health, markers: 0.633 of batch [0.529, 0.711] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.
- mental_health, uniform_random: 0.796 of batch [0.796, 0.801] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.

## Model ordering is criterion-dependent but mostly uncertain

Use model_rates.csv and paired intervals, not rankings inferred from separate means. The exploratory general-health GLM versus GPT comparison illustrates the distinction:

- D_ge3: concern-rate difference GLM minus GPT = +0.044 [+0.007, +0.088], 136 complete prompts.
- F_lt4: concern-rate difference GLM minus GPT = -0.029 [-0.118, +0.059], 136 complete prompts.
- OA_lt4: concern-rate difference GLM minus GPT = +0.044 [+0.015, +0.081], 136 complete prompts.

An apparent rate-order reversal for F is not strong evidence of a stable reversal when its interval spans zero. Mental-health comparisons are bounded to these endpoints and prompts. Incomplete sets are separately labeled, never silently mixed into pairings.

## Degenerate resamples

- education, D_ge3: 1999/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- education, F_lt4: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- education, OA_lt4: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- health, D_ge3: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- health, F_lt4: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- health, OA_lt4: 1998/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- mental_health, D_ge3: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- mental_health, F_lt4: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.
- mental_health, OA_lt4: 2000/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.

## Criterion overlap and continuous structure

criterion_intersections.csv enumerates all eight intersections, including no-trigger responses. continuous_relationships.csv includes E as well as H/D/F/OA. Paired criterion recall differences are in criterion_recall_differences.csv. Different prevalence and cut points can generate low overlap; these tables do not by themselves establish normative disagreement.
