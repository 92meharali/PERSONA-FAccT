# Response to the Two Additional Reviews

Updated 2 October 2026. Completed analytical and presentation improvements, not a prediction of acceptance.

| Concern | Implemented response | Boundary |
|---|---|---|
| Contribution is a metric benchmark rather than accountable allocation | Reframed title, abstract, contribution and discussion around justification of review targets, capacity, alternatives, and the distribution of scrutiny | Exact-budget metrics are established, not claimed as a new algorithm; new wording alone does not establish novelty |
| Marker baseline overlaps D cues | Explained overlap alongside rubric exclusions for functional first person, quoted speech and other-person attribution | No claim of guaranteed detection, label leakage, HumT internal mechanism, or universal marker safety superiority |
| Need a different or independent criterion | Made separate Group A OA and different-construct fit evidence more explicit | Neither is independent replication of D; new annotation cannot be invented |
| Trained model is too limited | Added positive rationale for a transparent, fixed low-dimensional audit comparator | Conclusion remains model/budget/data specific; no claim against semantic judges or all possible models |
| Null result needs equivalence | Retained bounded effect sizes/intervals; explained why no equivalence test is added without a justified practical margin | A margin chosen to make the inspected result pass would not repair evidence; no confirmatory equivalence claim |
| Criterion choice changes who enters the queue | Corrected this distinction explicitly | Fixed-policy threshold/vote changes alter evaluation membership, not selection; trained threshold variants were not run |
| Aggregate performance may hide uneven attention | New common-queue audit with all condition/model/scenario cells, paired uncertainty, exact slot conservation, and sparse flags | No subgroup reranking; unmatched sets and pointwise exploratory intervals; not demographic fairness or causal exclusion |
| Sparse impressive percentages | Abstract reports 42/165, 7/12, 10/23; summary figure carries concern and prompt counts | Resampling count is not effective sample size; no whole-domain power claim |
| Results too dense, only HumT visually uncertain | Added complete paired-contrast forest figure; moved budget curves to appendix; retained all policy/criterion tables | Paired intervals are pointwise and separate full-batch versus held-out capacities remain explicit |
| Arbitrary 80% workload point | Added existing 50/80/90/100% target plot with every policy's uncertainty | Targets were already specified; no optimized service requirement or stopping rule |
| Oracle ratio duplicates precision | Explained exact identity when 0 < k <= P and moved the material out of the main argument | Not a coincidence or additional independent result |
| Reporting card unvalidated | Kept supporting, worked-example status and no claim of evaluated contestation | No invented walkthrough, stakeholder response, or external validation |
| Ethics, AI provenance and reproducibility | Retained factual disclosures and added explicit release/institutional/version checklist | Authors or institutions must supply missing authority/records; Overleaf ZIP is not the computational supplement |

## What the new evidence adds

Common-queue selection differs from the earlier subgroup-specific rankings. Every subgroup now competes for the same domain-wide capacity before coverage is examined. The analysis preserves all 525 cells, including zeros, and reconstructs the earlier domain totals exactly.

In general health, markers catch more fit cases overall (32 vs HumT's 25), but fewer among natural prompts (4/74 vs 8/74). The natural-prompt difference favors HumT by 5.4 pp but its interval [-1.3,+13.0] includes zero. The point pattern illustrates a distribution hidden by an aggregate comparison, not established HumT superiority. Mental-health OA and all other condition cells are reported alongside it; examples were selected for interpretation after the complete specified analysis, not promoted to new primary tests.

The work supports more explicit reporting of allocation and residual cases. It does not establish that a category quota, a different screen, or an unevaluated reporting card would improve real user outcomes.

## Reproduce and review

- Run `python -m facct.allocation.run` from the repository root (approximately 18 seconds; 2,000 draws per domain).
- Rebuild the existing Overleaf package with `python -m facct.paper.build_overleaf`.
- Full results and provenance: `facct/allocation/outputs/`.
- Existing original, first-amendment, and trained-screen outputs remain unchanged.
- The current manuscript stays in the existing editor. Full-project compilation/page count need Overleaf; the native compiler cannot load project auxiliary files.

No raw data or earlier result was changed to strengthen a conclusion. No external action, release, push, chair email, or submission was performed.

## Final verification

All **56 tests passed**. A separate full run reproduced all three new CSVs and the findings report byte-for-byte (18.4 and 17.79 seconds). All **244 protected files** remain hash-identical. The two new figures were visually inspected, and the generated package passed source/asset/citation/label/macro/ZIP checks. The native compiler again stopped at its unsupported auxiliary-file include; full PDF layout and page count remain unverified. The [verification record](allocation_verification.json) contains the final ZIP checksum and comparison results.
