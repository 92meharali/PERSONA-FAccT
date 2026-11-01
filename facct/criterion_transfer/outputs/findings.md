# Criterion-to-decision results

FINAL: 2000 resamples. Exploratory analysis; all cells retained. No new primary family, outcome labels, or algorithm.

## Lexical screen, 20% reference fraction

| Domain | Training target | Assessment target | Caught / cases | Slots | Recall [95%] |
|---|---|---|---:|---:|---|
| mental_health | D_ge3 | D_ge3 | 70/165 | 130 | 42.4 [34.2, 48.2] |
| mental_health | D_ge3 | F_lt4 | 19/95 | 130 | 20.0 [12.6, 29.5] |
| mental_health | D_ge3 | OA_lt4 | 25/133 | 130 | 18.8 [14.0, 27.7] |
| mental_health | D_ge3 | contextual_reviewworthiness | 11/19 | 130 | 57.9 [31.6, 84.2] |
| mental_health | F_lt4 | D_ge3 | 53/165 | 130 | 32.1 [22.2, 40.6] |
| mental_health | F_lt4 | F_lt4 | 32/95 | 130 | 33.7 [22.1, 44.2] |
| mental_health | F_lt4 | OA_lt4 | 34/133 | 130 | 25.6 [17.5, 32.5] |
| mental_health | F_lt4 | contextual_reviewworthiness | 9/19 | 130 | 47.4 [26.9, 80.0] |
| mental_health | OA_lt4 | D_ge3 | 62/165 | 130 | 37.6 [28.0, 45.3] |
| mental_health | OA_lt4 | F_lt4 | 26/95 | 130 | 27.4 [15.6, 37.9] |
| mental_health | OA_lt4 | OA_lt4 | 26/133 | 130 | 19.5 [14.5, 30.2] |
| mental_health | OA_lt4 | contextual_reviewworthiness | 11/19 | 130 | 57.9 [27.8, 80.0] |
| education | D_ge3 | D_ge3 | 7/12 | 80 | 58.3 [14.3, 100.0] |
| education | D_ge3 | F_lt4 | 0/25 | 80 | 0.0 [0.0, 29.4] |
| education | D_ge3 | OA_lt4 | 2/18 | 80 | 11.1 [0.0, 54.5] |
| education | F_lt4 | D_ge3 | 0/12 | 80 | 0.0 [0.0, 25.0] |
| education | F_lt4 | F_lt4 | 13/25 | 80 | 52.0 [6.7, 73.9] |
| education | F_lt4 | OA_lt4 | 11/18 | 80 | 61.1 [0.0, 88.9] |
| education | OA_lt4 | D_ge3 | 3/12 | 80 | 25.0 [0.0, 66.7] |
| education | OA_lt4 | F_lt4 | 13/25 | 80 | 52.0 [12.5, 75.0] |
| education | OA_lt4 | OA_lt4 | 12/18 | 80 | 66.7 [0.0, 91.7] |
| health | D_ge3 | D_ge3 | 21/23 | 80 | 91.3 [57.1, 100.0] |
| health | D_ge3 | F_lt4 | 31/120 | 80 | 25.8 [16.7, 32.2] |
| health | D_ge3 | OA_lt4 | 9/9 | 80 | 100.0 [50.0, 100.0] |
| health | F_lt4 | D_ge3 | 19/23 | 80 | 82.6 [27.6, 95.2] |
| health | F_lt4 | F_lt4 | 29/120 | 80 | 24.2 [12.7, 31.8] |
| health | F_lt4 | OA_lt4 | 8/9 | 80 | 88.9 [0.0, 100.0] |
| health | OA_lt4 | D_ge3 | 19/23 | 80 | 82.6 [48.0, 96.2] |
| health | OA_lt4 | F_lt4 | 30/120 | 80 | 25.0 [15.7, 32.2] |
| health | OA_lt4 | OA_lt4 | 8/9 | 80 | 88.9 [50.0, 100.0] |

## All F-trained minus OA-trained contrasts (lexical, 20%)

| Domain | Assessment target | Recall change pp [95%] | Finite draws |
|---|---|---|---:|
| mental_health | D_ge3 | -5.5 [-16.4, +3.2] | 2000 |
| mental_health | F_lt4 | +6.3 [-3.2, +20.2] | 2000 |
| mental_health | OA_lt4 | +6.0 [-3.1, +9.4] | 2000 |
| mental_health | contextual_reviewworthiness | -10.5 [-20.0, +18.2] | 2000 |
| education | D_ge3 | -25.0 [-62.5, +0.0] | 1998 |
| education | F_lt4 | +0.0 [-19.2, +7.7] | 2000 |
| education | OA_lt4 | -5.6 [-41.2, +0.0] | 2000 |
| health | D_ge3 | +0.0 [-50.0, +26.3] | 2000 |
| health | F_lt4 | -0.8 [-8.6, +6.8] | 2000 |
| health | OA_lt4 | +0.0 [-87.6, +25.0] | 1998 |

## Boundaries

All models use original training labels only. Follow-up outcomes never enter fitting. The follow-up is an additional outcome on the same corpus, not unseen validation data. Its 19 positives constrain inference.

Intervals refit and rerank 2,000 paired prompt-cluster resamples within original folds. They are pointwise, exploratory, and conditional on the empirical judgments and partition. Sparse targets, zero-positive draws and constant-score fallback fits remain explicit. Off-diagonal performance is criterion transfer, not domain transfer or causal evidence.

Target changes include differences in prevalence, threshold and rubric content; they do not isolate pure construct effects. Queue differences do not demonstrate better review or experienced harm. Trained screens require historical labels, unlike fixed lexical/HumT rules. Every target pair and the H-augmented feature sensitivity remain in the tables; no winning screen is selected using follow-up results.

Reproduce: `.venv/bin/python -m facct.criterion_transfer.run`. Runtime and source checks are in manifest.json. Source follow-up frame is required at the recorded local path; identifying consent/recruitment records are not read or packaged.
