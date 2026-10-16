# Independent annotation follow-up

Local analysis of supplied A/B/C records, added 10 October 2026. The analysis
command does not change original ratings, the supplied package, original outputs
or the manuscript. A separately authorized [manuscript integration](../submission/annotation_integration.md)
now reports these results. Practitioner interviews remain deferred.

## Reproduce

From the repository root, with `facct/requirements.txt` installed:

```bash
python -m facct.independent_annotation.run --source "/Users/meharali/Downloads/PERSONA-MH-CHI-main-2/independent_annotation_study"
```

The default is 2,000 paired whole-prompt bootstrap replicates. Runtime is recorded
in `outputs/manifest.json`. A pilot must specify another directory, for example
`--replicates 20 --output /tmp/persona-annotation-pilot`.

```bash
python -m pytest facct/independent_annotation/test_analysis.py facct/tests -q
python -m facct.independent_annotation.verify
```

For byte-for-byte numerical reproduction, repeat the analysis command with
`--output /tmp/persona-annotation-reproduction`, then run
`python -m facct.independent_annotation.verify --compare /tmp/persona-annotation-reproduction`.
The verifier independently reconstructs majority labels, all original queue
identities and 112 original-policy target/budget cells using the standard library.
Bootstrap intervals are tested for paired clustering and deterministic reruns;
they are not checked against an independent statistical implementation.

See [analysis amendment](plan.md) before interpreting results. It was written
AFTER the ratings and point estimates were inspected, not preregistered. The
original policies use their original code, seed, IDs and text representation;
imported package queues and repaired-text features are separate sensitivity
families. Labels never enter screening features. No model is trained here.

## Outputs

- `findings.md`: generated summary and limits.
- `policy_metrics.csv`: all targets, policies, budgets and policy families.
- `resolved_labels.csv`: independently reconstructed binary resolution with
  pseudonymous IDs, no response text, rationale, or participant identity.
- `agreement.json`: original A/B agreement with unambiguous cell orientation.
- `policy_selections.csv`, `queue_comparison.csv`: original selections and overlap
  with imported queues.
- `bootstrap_intervals.csv`: exploratory hypothetical-batch procedure intervals,
  not uncertainty of exact finite-corpus counts or human judgments.
- `context_cells.csv`, `legacy_overlap.csv`, `version_category_descriptives.csv`:
  descriptive subgroup/criterion/version-related sensitivity summaries.
- `manifest.json`: source and implementation hashes, Git revision, software,
  seeds, command, runtime and output hashes. No inference of collection dates.

Outputs are for local review, not automatically approved for public release.
Source data and private consent/eligibility records remain outside this package.
Human provenance is author-reported. During manuscript integration the author
confirmed separation from the original author/rater team and consent/coverage
before annotation. Supplied forms still show pending status; the author deferred
providing backgrounds, recruitment/payment details and an applicable approval
reference. Preserve this discrepancy, rather than silently filling the forms.
No action here independently certifies ethics scope or submission eligibility.

## Version limitation

A used capability note v1.0; B and C used v1.1. Person and instruction version are
confounded. Rater-specific comparisons and post-label category counts cannot
identify the causal effect of the note revision. We retain every response and
report both streams. C assessed only disputed cases, so no full-corpus three-rater
reliability statistic is justified.
