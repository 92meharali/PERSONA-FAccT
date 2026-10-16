# Common-queue allocation amendment

Specified 2 October 2026 before this module's pilot or final run. This follows inspection of the corpus, earlier subgroup-specific rankings, and two rounds of manuscript review. It is exploratory, not preregistration or independent confirmation. Original criteria, sources, primary family, and all earlier outputs remain immutable.

## Question and scope

Within the same domain-wide queue, which recorded categories receive review slots and which rubric-defined concern cases remain outside it? This differs from earlier context analyses that reranked each subgroup with its own quota. It describes the distribution of review opportunities in this corpus, not demographic fairness, causal exclusion, realized harm, or population representativeness.

- Use the original 20% domain-wide capacity and deterministic tie rule (seed 20261002).
- Compare high-H, length, markers, original equal-weight rank fusion, and analytical uniform random selection. Do not pool scores from trained fold-specific models into an incompatible global ranking.
- Retain all three original concern definitions, domains, and existing condition, model, and scenario categories, including missing metadata as an explicit category. No searched mixtures, intersections, new thresholds, or selected favorable categories.
- Each grouping partitions the unchanged domain batch. Selection is calculated once per policy, independent of category or criterion. Labels only evaluate membership after selection. Totals must reconstruct the original domain counts for every partition.
- Report group response and concern counts, positive/negative supporting prompts, allocated slots, selection rate, recall, precision, missed cases, and residual prevalence. Also report group-minus-complement recall, high-H-minus-markers recall, and recall minus analytical domain-wide random selection.
- Random expected group slots are k*n_group/n; expected caught cases are k*P_group/n. Group recall expectation is k/n when P_group>0, not a separately floored group quota. Random precision is the ratio of expected counts, not an assertion about the expectation of a random ratio.
- Use 2,000 domain-level paired whole-prompt bootstrap draws. Re-rank the full resampled domain at floor(0.2*n_draw), then project onto the same category definitions. Categories absent from a draw retain zero counts and undefined ratios. Resamples are shared across policies, criteria, and categories; tie copies have deterministic distinct keys.
- Report pointwise exploratory percentile intervals and finite counts. No significance searching, simultaneous coverage claims, or subgroup winner rankings. Fewer than ten positive or negative supporting prompts flags a cell; group-versus-complement interpretation also requires adequate complement support.
- Condition is the main reporting partition because it is compact and available across all domains, not because of observed effects. Report all condition-by-criterion cells together; models and scenarios remain descriptive complete tables. Do not interpret natural/adversarial differences causally: prompt sets are unmatched.

## Presentation changes using existing evidence

Generate a two-panel summary of all nine paired HumT-minus-marker full-batch contrasts and all nine incremental trained contrasts. Keep their differing capacities and interval constructions separate. Show existing 50%, 80%, 90%, and 100% workload targets, without adding favorable targets or treating retrospective prefixes as deployment stopping rules. Move redundant oracle context out of the main narrative and explain when its fraction equals precision.

Clarify that changing concern labels changes evaluation of a fixed queue, not the queue itself. Different training targets may change learned rankings, but threshold re-training is not part of this amendment. OA is a separate-rater endpoint, not independent replication of D. Add no equivalence test: no defensible practical margin was supplied independently of inspected results. Add no invented semantic judge, new annotators, ethics scope, model version, or practitioner validation.

## Verification and provenance

Unit tests must demonstrate common rather than subgroup budgets, analytical random allocation, partition conservation, label-independent selections, empty/no-positive behavior, tie reproducibility, and reconstruction of earlier point counts. Preserve all categories, even when no concern exists. Record source and earlier-tree hashes, code/specification hashes, software versions, runtime, and every output checksum. Reproduce the final run separately and compare deterministic outputs.
