# Common-queue allocation audit

Exploratory third amendment. Each domain is ranked once at 20% capacity; the selected queue is then described by category. Subgroups do not receive independent quotas. Earlier studies and primary comparisons remain unchanged.

## Complete condition view

| Domain | Criterion | Condition | N | Cases / positive prompts | H slots | H caught | H missed | Marker slots | Marker caught | Sparse |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|
| mental_health | D_ge3 | adversarial | 360 | 81 / 50 | 54 | 21 | 60 | 69 | 33 | False |
| mental_health | F_lt4 | adversarial | 360 | 48 / 37 | 54 | 7 | 41 | 69 | 11 | False |
| mental_health | OA_lt4 | adversarial | 360 | 64 / 54 | 54 | 9 | 55 | 69 | 15 | False |
| mental_health | D_ge3 | natural | 300 | 84 / 49 | 78 | 21 | 63 | 63 | 30 | False |
| mental_health | F_lt4 | natural | 300 | 47 / 40 | 78 | 11 | 36 | 63 | 11 | False |
| mental_health | OA_lt4 | natural | 300 | 69 / 57 | 78 | 22 | 47 | 63 | 18 | False |
| education | D_ge3 | adversarial | 147 | 12 / 7 | 42 | 7 | 5 | 68 | 9 | True |
| education | F_lt4 | adversarial | 147 | 16 / 9 | 42 | 9 | 7 | 68 | 1 | True |
| education | OA_lt4 | adversarial | 147 | 18 / 10 | 42 | 9 | 9 | 68 | 3 | False |
| education | D_ge3 | natural | 268 | 0 / 0 | 41 | 0 | 0 | 15 | 0 | True |
| education | F_lt4 | natural | 268 | 9 / 8 | 41 | 1 | 8 | 15 | 0 | True |
| education | OA_lt4 | natural | 268 | 0 / 0 | 41 | 0 | 0 | 15 | 0 | True |
| health | D_ge3 | adversarial | 150 | 20 / 12 | 56 | 9 | 11 | 71 | 19 | False |
| health | F_lt4 | adversarial | 150 | 46 / 23 | 56 | 17 | 29 | 71 | 28 | False |
| health | OA_lt4 | adversarial | 150 | 9 / 7 | 56 | 3 | 6 | 71 | 9 | True |
| health | D_ge3 | natural | 265 | 3 / 3 | 27 | 1 | 2 | 12 | 2 | True |
| health | F_lt4 | natural | 265 | 74 / 46 | 27 | 8 | 66 | 12 | 4 | False |
| health | OA_lt4 | natural | 265 | 0 / 0 | 27 | 0 | 0 | 12 | 0 | True |

## Interpretation contract

- All condition, model, and scenario cells, including zero-concern and sparse cells, are retained in category_coverage.csv. Intervals are paired prompt-bootstrap pointwise summaries, not simultaneous subgroup tests.
- Selection rate describes access to review. Recall describes coverage conditional on the recorded criterion. A larger missed count may reflect more concerns rather than a poorer ranking; read rates and counts together.
- H-minus-marker contrasts are paired within the same group and full-domain quota. Group-minus-complement contrasts compare coverage under one common policy, not a counterfactual intervention. Shared prompt clusters remain together across model categories.
- Random expected group slots and caught counts use the full-domain budget fraction. Expected-count precision is a ratio of expectations; random single-draw variability is not what its bootstrap interval estimates.
- Category labels are existing corpus metadata, not validated demographic groups. Natural/adversarial prompts are unmatched. Patterns describe this corpus and criterion, not causal discrimination or deployment harm.
- Changing the concern threshold does not change these label-free selections. It changes which selected and unselected items count as concerns. No subgroup has been given a quota or policy recommendation on the basis of these exploratory results.

Run `python -m facct.allocation.run` from the repository root. The manifest records runtime, software, seeds, source hashes and all output hashes. Selection identities are retained without raw text.
