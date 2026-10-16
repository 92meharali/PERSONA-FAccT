# Post-review exploratory findings

The original primary family remains unchanged. Added analyses were specified after inspecting the original results; all new intervals are exploratory pointwise 95%, not simultaneous or confirmatory. No ratings or original outputs were changed.

## Complementarity at 20%

| Domain | Criterion | H only | Markers only | Both | Fixed fusion / cases | Fusion minus markers recall, pp [95%] |
|---|---|---:|---:|---:|---:|---|
| mental_health | D_ge3 | 20 | 41 | 22 | 61/165 | -1.2 [-7.9, +5.0] |
| mental_health | F_lt4 | 13 | 17 | 5 | 25/95 | +3.2 [-6.6, +10.6] |
| mental_health | OA_lt4 | 19 | 21 | 12 | 39/133 | +4.5 [-2.3, +11.5] |
| education | D_ge3 | 1 | 3 | 6 | 9/12 | +0.0 [-33.3, +36.4] |
| education | F_lt4 | 10 | 1 | 0 | 3/25 | +8.0 [+0.0, +23.1] |
| education | OA_lt4 | 9 | 3 | 0 | 3/18 | +0.0 [-16.7, +25.0] |
| health | D_ge3 | 0 | 11 | 10 | 17/23 | -17.4 [-38.5, +0.0] |
| health | F_lt4 | 10 | 17 | 15 | 31/120 | -0.8 [-7.1, +5.4] |
| health | OA_lt4 | 0 | 6 | 3 | 7/9 | -22.2 [-60.0, +0.0] |

H-only cases establish different observed selections, not a cost-free gain from taking the union. Fusion has the same exact capacity. No broad-D fusion improvement over markers is established; neither equivalence nor absence of useful information is established.

## Direct paired workload differences

Negative H-minus-comparator values mean fewer responses reviewed by H to reach 80% criterion recall. These are retrospective workloads with known labels, not deployable stopping rules.

- mental_health, H_minus_random_workload80: -8.9 pp [-15.8, -2.6], 2000/2000 finite draws; sparse=False.
- mental_health, H_minus_length_workload80: +4.7 pp [-5.3, +14.4], 2000/2000 finite draws; sparse=False.
- mental_health, H_minus_markers_workload80: +7.4 pp [-1.2, +19.2], 2000/2000 finite draws; sparse=False.
- education, H_minus_random_workload80: -39.5 pp [-66.1, +9.0], 1999/2000 finite draws; sparse=True.
- education, H_minus_length_workload80: -30.1 pp [-71.6, +23.0], 1999/2000 finite draws; sparse=True.
- education, H_minus_markers_workload80: +13.7 pp [-9.2, +64.9], 1999/2000 finite draws; sparse=True.
- health, H_minus_random_workload80: -33.1 pp [-49.2, -17.1], 2000/2000 finite draws; sparse=False.
- health, H_minus_length_workload80: -37.1 pp [-55.3, -18.8], 2000/2000 finite draws; sparse=False.
- health, H_minus_markers_workload80: +31.1 pp [+12.6, +46.8], 2000/2000 finite draws; sparse=False.

## Label stability

| Domain | Criterion | Within +/-0.2 | Exactly at cutoff | Split votes | Mean vs majority disagreement |
|---|---|---:|---:|---:|---:|
| mental_health | D_ge3 | 172/660 | 108 | 137 | 35 |
| mental_health | F_lt4 | 343/660 | 149 | 146 | 85 |
| mental_health | OA_lt4 | 361/660 | 160 | 200 | 123 |
| education | D_ge3 | 5/415 | 4 | 21 | 10 |
| education | F_lt4 | 336/415 | 283 | 9 | 9 |
| education | OA_lt4 | 196/415 | 63 | 2 | 2 |
| health | D_ge3 | 11/415 | 3 | 10 | 1 |
| health | F_lt4 | 166/415 | 73 | 120 | 50 |
| health | OA_lt4 | 10/415 | 7 | 4 | 1 |

All source ICC point estimates reconstruct from current long ratings. Source ordinal alpha and response-bootstrap confidence intervals are imported and labeled, not independently re-estimated. Reliability is not construct validity or personnel independence.

## Text provenance

The join replay reproduces all imported H scores, source filenames, and tiers. In education 359/415 rated/export pairs are byte-identical and 56 differ after normalization; in general health 412/415 are identical and three differ. Mental health has embedded scores without a separate historical input string. Export text association does not prove actual API scorer inputs.

On the unchanged full batches at 20%, computing lexical features from export text instead of rated text leaves selected criterion counts unchanged for length, markers, and fixed rank fusion. This does not prove identical selected identities or correct joins. The separate identical-text subset analyses report both unchanged absolute capacity and unchanged fractional budget; neither identifies a causal effect of join error.

## Scope

No external study, fitted classifier, LLM judge, practical audit validation, or publication clearance is asserted. New learned comparators would need a separate grouped evaluation and cost account. The author handles venue disclosure and confirmation of intern non-participation safeguards.
