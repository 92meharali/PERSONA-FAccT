# Conditional-lift results

Exploratory post-review analysis; original primary family unchanged. Conditional lift is the absolute recall difference when adding H to a fixed logistic screen using markers and log-length, evaluated in common held-out prompt batches. It is not a causal effect or universal information test.

## All reference-budget comparisons

| Domain | Criterion | Slots | Reduced / cases | Extended / cases | Recall change, pp [95%] | Positive prompts | Sparse | Split range, pp |
|---|---|---:|---:|---:|---|---:|---|---|
| mental_health | D_ge3 | 130/660 | 70/165 | 66/165 | -2.4 [-6.0, +2.3] | 99 | False | [-3.0, +1.2] |
| mental_health | F_lt4 | 130/660 | 32/95 | 33/95 | +1.1 [-8.2, +4.1] | 77 | False | [-5.3, +1.1] |
| mental_health | OA_lt4 | 130/660 | 26/133 | 30/133 | +3.0 [-3.9, +8.5] | 111 | False | [-1.5, +4.5] |
| education | D_ge3 | 80/415 | 7/12 | 8/12 | +8.3 [-28.6, +33.3] | 7 | True | [-8.3, +0.0] |
| education | F_lt4 | 80/415 | 13/25 | 13/25 | +0.0 [-15.0, +7.4] | 17 | False | [-4.0, +4.0] |
| education | OA_lt4 | 80/415 | 12/18 | 12/18 | +0.0 [-15.4, +11.8] | 10 | False | [+0.0, +0.0] |
| health | D_ge3 | 80/415 | 21/23 | 21/23 | +0.0 [-15.0, +12.0] | 15 | False | [-8.7, +4.3] |
| health | F_lt4 | 80/415 | 29/120 | 30/120 | +0.8 [-5.6, +8.7] | 69 | False | [-3.3, +1.7] |
| health | OA_lt4 | 80/415 | 8/9 | 8/9 | +0.0 [-9.1, +9.1] | 7 | True | [+0.0, +0.0] |

The ten alternative partition results are sensitivity, not independent replication, a confidence interval, or a best-seed selection. Read the full seed-level table. All nine cells are reported, including sparse and negative effects.

## Interpretation boundaries

- Reduced and extended models share training prompts, labels, settings, and test quotas. Scalers are fitted on training data only; no tuning or threshold optimization is performed.
- The 2,000 paired resamples retain original fold membership, resample whole prompts within folds, and refit both models. Intervals remain approximate and conditional on this partition, source judgments, and observed distribution. They are not independent-sample tests or simultaneous nine-cell coverage.
- Counts aggregate held-out batches. Per-batch rounding means total selected count can differ from the original full-domain simulation. All competing fixed policies are re-evaluated in the same held-out batches; do not compare trained recall directly with the original table as if capacities/batches were identical.
- Separate policies are trained for each criterion. The learned scores are ranking tools for these labels, not calibrated harm probabilities. A null or negative incremental result does not establish conditional independence or no possible value from H.
- Different selected cases in the earlier overlap table are not proof of incremental improvement. The paired trained comparison, not a larger union, addresses the specified added-value question.

## Label acquisition and safeguards

- mental_health: each fitted model uses 528-528 labeled training responses (2640-2640 underlying criterion ratings). Labels are reused across fits; these numbers must not be summed as separate annotation purchases. Observed single-class point fits: 0.
- education: each fitted model uses 331-334 labeled training responses (1655-1670 underlying criterion ratings). Labels are reused across fits; these numbers must not be summed as separate annotation purchases. Observed single-class point fits: 0.
- health: each fitted model uses 331-333 labeled training responses (1655-1665 underlying criterion ratings). Labels are reused across fits; these numbers must not be summed as separate annotation purchases. Observed single-class point fits: 0.

Historical annotations supply both retrospective training and held-out assessment. No new labels, external participant outcomes, annotation time/cost estimate, LLM judge, or deployment effectiveness is claimed. Training label requirements distinguish these models from the label-free baselines.

## Reproduce

Run `python -m facct.conditional.run` from the repository root with pinned facct requirements. This writes separate outputs and verifies source/earlier-output hashes. The manifest records measured runtime and software versions. Source code, seed, predictions, fold assignments, coefficients, and bootstrap replicate deltas are retained.
