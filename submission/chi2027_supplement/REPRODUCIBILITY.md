# Reproducibility guide

## Scope

The package reproduces the paper-facing reliability, descriptive, correlation,
cross-validation, ablation, interaction, and sensitivity analyses from the
supplied anonymous processed data. It also includes the generated outputs used
for manuscript verification.

The raw-to-processed corpus build is not rerun by the packaged command because
the anonymous review package excludes named raw annotation files and
source-controlled acquisition materials. Data-audit and HumT-provenance outputs
from that build are retained under `analysis/outputs/`.

## Environment

- Python 3.11 or newer
- Dependencies pinned in `analysis/requirements.txt`
- Deterministic seed: 42
- Grouped cross-validation: 5 prompt-grouped folds, repeated 20 times
- Bootstrap uncertainty: 1,000 prompt-cluster resamples

Create an isolated environment from the supplement root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r analysis/requirements.txt
```

## Run

```bash
python3 -m analysis.run_from_processed
```

Generated files are written to:

```text
analysis/outputs/tables/
analysis/outputs/reports/
analysis/outputs/figures/
```

Random sampling and fold assignment are deterministic with the pinned
environment. Runtime depends on hardware; the correlation bootstrap is the
longest phase. Different numerical libraries or BLAS implementations can
produce differences in the final floating-point digits without changing the
reported rounded values.

## Traceability

- `cv_fold_assignments.csv` records first-repeat response assignments.
- `cv_folds.csv` records every fold in every repeat.
- `cv_performance.csv` contains the six model families presented in the paper.
- `ablation.csv` and `incremental_validity.csv` contain paired model
  comparisons.
- `domain_interactions.csv` and `domain_interaction_model_fit.csv` support the
  interaction section.
- `reliability.csv`, `construct_relationships.csv`, and `ceiling_floor.csv`
  support the corresponding manuscript tables.

The supplied outputs should be retained before rerunning if a reviewer wants to
compare the exact archived files with locally regenerated results.
