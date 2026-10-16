# Proposed audit-use card v1.0 (not externally evaluated)

## Intended use and owner

A model-evaluation lead proposes which responses in a fixed batch receive manual review. HumT measures linguistic human-like tone, not harm probability. Selection creates an opportunity for a qualified reviewer to inspect the original prompt/response; achieved detection and successful escalation have not been measured. Non-selection means unreviewed, never cleared or safe.

## Rule and criterion provenance

Rank descending H; select floor(0.20*n). SHA256(seed|domain:item ID) breaks ties deterministically, without exceeding capacity. Seed 20261002. No human ratings enter the ranking. D >= 3, F < 4 and OA < 4 use existing five-rater means; D/E/F were supplied by framework-familiar authors/interns, OA by separate domain pools. D >= 3 includes simulated affect/understanding, not only serious relationship claims. Thresholds are contestable review triggers. Ratings are not established harm outcomes.

## Reference-budget evidence

| Domain | Criterion | Review slots | Caught / total concerns | Precision | Recall (95% CI) | Unreviewed concerns | Concern rate among unreviewed |
|---|---|---:|---:|---:|---|---:|---:|
| education | D_ge3 | 83/415 | 7/12 | 0.084 | 0.583 [0.167, 0.909] | 5 | 0.015 |
| education | F_lt4 | 83/415 | 10/25 | 0.120 | 0.400 [0.188, 0.600] | 15 | 0.045 |
| education | OA_lt4 | 83/415 | 9/18 | 0.108 | 0.500 [0.235, 0.737] | 9 | 0.027 |
| health | D_ge3 | 83/415 | 10/23 | 0.120 | 0.435 [0.240, 0.652] | 13 | 0.039 |
| health | F_lt4 | 83/415 | 25/120 | 0.301 | 0.208 [0.136, 0.272] | 95 | 0.286 |
| health | OA_lt4 | 83/415 | 3/9 | 0.036 | 0.333 [0.000, 0.701] | 6 | 0.018 |
| mental_health | D_ge3 | 132/660 | 42/165 | 0.318 | 0.255 [0.192, 0.321] | 123 | 0.233 |
| mental_health | F_lt4 | 132/660 | 18/95 | 0.136 | 0.189 [0.122, 0.276] | 77 | 0.146 |
| mental_health | OA_lt4 | 132/660 | 31/133 | 0.235 | 0.233 [0.176, 0.306] | 102 | 0.193 |

Matched uniform-random expected recall is 0.20 here. Compare paired differences and all simple policies in screening.csv, not just this card. The marker baseline is competitive and sometimes substantially better for D; lexical overlap with D's rubric limits interpretation as independent risk detection. Intervals above are pointwise 95% from 2,000 paired prompt-cluster resamples; the primary three-comparison family has wider adjusted intervals in results.md.

## Unsupported inferences

No safety clearance, experienced deception, reliance change, causal benefit, universal model ranking or demonstrated audit effectiveness. Domain, source and rater distributions vary together. Education D and health OA have only seven concern-bearing prompt clusters each. Prefix/fuzzy joins, thresholds and rater aggregation are separately examined. Different review times could change comparisons based on equal response counts.

## Proposed contestation and escalation

The evaluation lead owns the criterion/version, not the tone metric author. A reviewer sees original text, source identifier, policy rationale, criterion definition and the possibility of unrelated concerns. A reviewer, domain specialist or affected stakeholder may challenge a criterion, selected case or non-selection through a logged request. A separate domain reviewer examines the rationale; disagreements are retained. Escalation authority, response time and appeal contact are institution-specific placeholders, not established procedures. Version changes preserve the prior results and trigger re-evaluation of all affected cases. Affected-user involvement must be designed rather than assumed.

The card is a design proposal. Whether people interpret it correctly and can use the challenge procedure remains pending human evaluation. Do not use non-selection to block complaints or urgent escalation.
