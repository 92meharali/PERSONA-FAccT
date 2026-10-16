# Independent annotation analysis amendment

Specified 10 October 2026, AFTER inspecting all A/B/C ratings and point estimates.
This is an auditable implementation specification, not a preregistration.

## Scope

The supplied package contains 660 A ratings, 660 B ratings, and 14 C ratings of
A/B binary disagreements. The user confirms human assessment for A and confirms
C's independence and blinding. B was described as a second human assessor, but the
supporting updated records have not been supplied for verification. Local ethics,
eligibility, and capability-acceptance forms remain incomplete; do not infer
prospective clearance, rewrite their dates, or publish identifying records.

Preserve the entire external package and original repository inputs. Read it via
an explicit CLI path, hash all files before and after execution, and do not copy
consent, names, response text or raw rationales into this output directory. Output
study IDs only for internal checking. No upload or manuscript edit is authorized
by this implementation. The original computational manuscript remains unchanged.

## Frozen decisions and post hoc sensitivities

- Reconstruct yes/no using 2/3 versus 0/1. U and missing remain unresolved.
- Keep binary A/B agreements; require C only for disagreements or unresolved
  pairs. Resolve with two definite votes; otherwise retain unresolved status.
- Agreement statistics use A and B BEFORE resolution, never C's selected subset.
- Primary target: resolved ABC labels, 20% of the original 660-response batch.
- Reuse original policy functions, exact original text representation, original
  seed and stable IDs. Original markers are token-normalized frequencies and
  length is token count. Human labels cannot enter any screening input.
- Compare HumT with original markers and expected matched-budget random review.
  Label all added intervals and sensitivities exploratory, not confirmatory.
- Preserve imported package queues as a distinct policy family. Random queue
  performance is one realized draw, not expected random performance.
- Show 5/10/20/30% budgets for original policies; 20% remains the reference.
- Assessor sensitivity: A alone, B alone, resolved ABC, A/B union and intersection.
  Show severity >=3 for A and B separately. No invented ordinal ABC consensus.
- Version sensitivity: A used capability note v1.0, B and C v1.1. A/B differences
  confound assessor and instruction version. Do not identify a causal version
  effect. Report disagreements tagged identity/authority or capability/continuity
  by ANY assessor descriptively; these are post-label categories, not independent
  selection variables. Do not exclude those cases from the main analysis.
- Compare original versus repaired-text feature rankings as a separate encoding
  sensitivity, not a silent correction of the original policies.
- Tabulate legacy D >=3, F <4 and OA <4 overlap, and all condition/model cells
  under the ORIGINAL full-batch queues; do not rerank within subgroups.

## Uncertainty

For the finite census, counts are exact conditional on the chosen labels. The
additional 2,000 paired whole-prompt bootstrap replicates estimate a different,
secondary procedure: draw 220 prompt clusters with replacement, include every
response in each draw, and RERANK each resulting 660-response batch at 20%.
Pair draws across assessors and policies, use deterministic occurrence-specific
tie keys, and report 95% pointwise percentile intervals and undefined replicate
counts. These intervals neither establish population representativeness nor
incorporate human-judgment uncertainty. No multiplicity-adjusted significance
claims will be made. Random baselines use analytic expectations in every draw.

If any target contains unresolved labels, do not silently treat them as negative:
report unresolved counts and positive-label bounds and leave full-target point
recall/precision undefined. Bootstrap that target remains undefined pending a
separately justified missingness analysis. Zero-positive recall is also undefined.
Recall bounds condition on at least one positive existing; if all potential
positives are unresolved, the all-negative assignment also permits undefined
recall. Bounds are not a claim that a positive necessarily exists.

## Verification

Validate rating domains, uniqueness, exact frame coverage, C case membership,
raw-versus-return consistency, immutable source hashes, capability-note versions,
source-text hashes, original IDs/H values, source encoding correspondence, and
provided majority labels. Hard mismatches stop analysis. Compare original and
package queue identities. Test majority rules including U, sparse/zero positives,
exact budgets, duplicate IDs, label leakage, cluster pairing and tie handling.
Reproduce numerical tables in a second directory and compare hashes. Keep a
manifest with inputs, implementation, environment, seeds, runtime and command.

## Subsequent manuscript-integration authorization

On 10 October 2026 the user separately requested integration into the existing
paper. This supersedes only the original no-manuscript-edit scope, not any
statistical decision above. The user answered yes to confirmation of new-assessor
separation and consent/ethics coverage before collection. The assistant explicitly
stated this interpretation. Asked for assessor backgrounds, compensation and an
approval/amendment reference, the user chose to skip these details for now.
Record the author attestation and missing particulars separately; do not infer
qualifications, payment terms, approval scope from the source study, or dates.
The pre-integration manuscript and analysis manifest are preserved under
`facct/paper/history/pre-annotation-integration/`. Rerunning after authorized edits
records the new manuscript hash without changing the original numerical results.
