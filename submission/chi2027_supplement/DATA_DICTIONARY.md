# Data dictionary

## `analysis/processed/persona_all.csv`

One row per model response (`n = 1,490`). This is the analysis-ready,
response-level corpus.

| Field | Meaning |
|---|---|
| `domain` | `mental_health`, `education`, or `health` |
| `annotation_item_id` | Anonymous response identifier |
| `prompt_id` | Prompt-group identifier used for grouped cross-validation |
| `prompt_id_source` | Whether the prompt ID was native or deterministically reconstructed |
| `model`, `model_raw` | Normalized and source model labels |
| `model_source` | Provenance of the normalized model label |
| `condition` | Natural or adversarial generation condition |
| `scenario_type` | Domain-specific scenario category |
| `n_raters` | Number of ratings aggregated per construct |
| `n_oa_raters` | Number of Group A `OA` raters |
| `n_dimension_raters` | Number of Group B `E`/`D`/`F` raters |
| `H`, `humt` | HumT-derived human-likeness score |
| `humt_std` | Available HumT uncertainty/dispersion field from the source export |
| `humt_join_tier` | Deterministic text-join method used to recover HumT |
| `humt_source_file` | Non-identifying source-export provenance |
| `OA`, `E`, `D`, `F` | Five-rater arithmetic means |
| `*_median`, `*_std` | Median and sample standard deviation across the five raters |
| `prompt`, `response` | Stimulus prompt and generated model response |

`D` is coded so that larger values mean greater deception risk. `OA`, `E`, and
`F` are coded so that larger values mean greater appropriateness or fit.

## `analysis/processed/persona_ratings_long.csv`

One row per response-rater record (`n = 14,900`). It supports reliability
estimation while keeping the criterion and diagnostic pools structurally
separate.

| Field | Meaning |
|---|---|
| `domain`, `annotation_item_id`, `prompt_id` | Join and grouping identifiers |
| `annotator_id` | Anonymous within-pool rater identifier |
| `rater_group` | `Group A` for `OA`; `Group B` for `E`, `D`, and `F` |
| `scenario_type`, `model`, `condition` | Response metadata |
| `OA_score` | Group A score; blank on Group B rows |
| `E_score`, `D_score`, `F_score` | Group B scores; blank on Group A rows |

All human ratings use integer anchors from 1 to 5. Blank cells encode
constructs that the rater pool was not assigned; they are not missing
annotations.
