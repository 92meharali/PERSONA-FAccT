# Claim-to-evidence ledger

## Current assessment amendment: 10 October 2026

The historical ledgers below freeze earlier computational stages. Statements that
there were no new judgments no longer describe the integrated manuscript.

| Current claim | Evidence | Boundary |
|---|---|---|
| Two complete new streams and selective third assessment cover the MH frame | independent_annotation/outputs/resolved_labels.csv, manifest.json | 660 A, 660 B, 14 C; no three-rater full-corpus claim |
| 19 resolved positives occur in 13 prompt clusters | policy_metrics.csv, reconstructed majority resolution | Conditional on supplied judgments and capability-note assumptions |
| Original HumT catches 6 versus normalized markers' 12 at 132 slots | original/resolved_ABC/0.2 policy_metrics.csv rows | Same queues as old analysis; not imported lexical alternatives |
| Main paired follow-up contrasts include zero | bootstrap_intervals.csv | H-M -31.6 pp [-66.7,+4.3]; H-random +11.6 [-6.7,+30.0]; exploratory hypothetical batches |
| Observed binary agreement is 97.9%, kappa .698, positive agreement 70.8% | agreement.json before C resolution | Not same-instruction reliability, validity or proof of independent conduct |
| New labels are not a strict subset of broad D | legacy_overlap.csv: 15 shared, 4 follow-up-only | Different criterion, assessor population and instructions; no causal attribution |
| New assessors were outside original team and had prior consent/coverage | Author confirmation during integration; explicit interpretation in conversation | Author attestation; forms still pending, backgrounds/payments/approval reference deferred |
| Follow-up improves evidence distinctness from CHI | New reviewworthiness records and unchanged-queue test | Same responses; novelty and eligibility not self-certified |
| Main paper values are output-derived | build_annotation_assets.py, generated tables/macros and package manifest | No new rating, pretrained judge, citation or favorable threshold search |

The trained-screen analysis remains limited to original labels. Human ratings and
raw rationales are not changed. The follow-up specification was written after
inspection, not preregistered; new-source compensation and ethics are not inferred
from original Group B records.

## Historical original-analysis ledger

| Candidate claim | Evidence | Status / boundary |
|---|---|---|
| Released corpus has 1,490 responses and 499 prompt clusters | input_counts.csv, prompt_audit.csv; hashed inputs | Recomputed; does not establish original collection size |
| Every stored E/D/F/OA mean reconstructs from five ratings | input_checks.csv, immutable long ratings | Recomputed; anonymous stream IDs do not authenticate rater identities |
| Current data match the repository submission snapshot | byte comparisons in input_checks.csv | Verified locally; author must confirm the actual submitted supplement |
| CHI headline numbers match released outputs/current counts | chi_headline_crosscheck.csv, submitted_pdf_checks.md | Numerical consistency; CHI CV not refitted in this study |
| HumT has criterion-specific allocation utility | screening.csv with matched-budget random and paired baseline intervals | Exploratory offline performance, not all-metric or causal claim |
| A simple marker score may outperform HumT for D-trigger allocation | paired delta_markers fields and marker definition | Same linguistic cues partly appear in D rubric; not independent harm detection |
| Some concern cases remain unreviewed | caught/missed counts at exact capacities | Not "false reassurance" or safety clearance |
| Threshold/consensus choice changes outcomes | threshold_sensitivity.csv, consensus_sensitivity.csv, rater_sensitivity.csv | Descriptive criterion sensitivity, not proof one criterion is correct |
| Criteria label different cases | criterion_intersections.csv, continuous_relationships.csv, criterion_recall_differences.csv | This changes evaluation membership, not the fixed queue; cut points/prevalence can explain low overlap |
| Model rates differ | model_paired_differences.csv, model_completeness.csv | Complete prompt sets only; pointwise exploratory; no family rankings |
| Results robust to joining/ties | join_sensitivity.csv, tie_sensitivity.csv | Assess each result; do not use blanket robustness language |
| Proposed card could support contestation | audit_use_card.md, study materials | Design hypothesis, not tested effectiveness |
| Practitioners find this workflow useful | None | Not established; study deferred and excluded from current draft |
| HumT screening is organizational practice | None found in targeted primary review | Do not claim adoption; proposed simulation |
| Labels measure user harm/deception experienced | None | Unsupported |
| New study is independent enough for concurrent submission | overlap_matrix.md and future written chair guidance | Unresolved; no clearance |
| Ethics covers new participation | No institutional scope confirmation in this package | Pending; no recruitment |
| Available professors provide independent external validation | Author confirmed their involvement in PERSONA | Unsupported; any contribution is internal research development |
| AI agents supply replacement practitioner evidence | None | Excluded; no new AI-agent experiment conducted |
| Current computational review draft is numerically traceable | paper/generated/review_manifest.json and generated tables | Source-derived numerical sections; not submission eligibility or validated page count |
| Phase labels imply the same people rated OA and E/D/F | Final PROTOCOL_APPLICATION_NOTE.md, checked against fresh origin/main | Incorrect for the documented implemented design; note explicitly says separate pools and fallback not used |
| Compensation is unresolved because participation was voluntary | Final ethics record and submitted PDF p. 8 | Final documents report existing paid research roles; voluntary participation is compatible; payroll not independently audited |
| Exact repository ZIP was uploaded to CHI | Author's tentative recollection and local ZIP checks | Not authenticated; all 69 local archive entries match, but no portal artifact/receipt checked |

Current provenance and overlap interpretation: see submission/provenance_resolution.md, submission/distinctness_assessment.md and submission/resolution_tracker.md. These supersede the initial unresolved-phase narrative without rewriting the frozen audit history.

Every numerical paper table should be generated from outputs, not hand-copied into a separate source of truth. The manifest records code/config/source versions. Literature interpretations and verified metadata are separately traceable in the primary-source memo.

## Post-review additions

| Claim | Evidence | Boundary |
|---|---|---|
| HumT selects 20 mental-health broad-D cases outside marker selection at 20% | revision/outputs/complementarity.csv | Different selected cases, not a same-budget gain from the union |
| Fixed rank fusion does not establish improved broad-D recall over markers | paired_comparisons.csv; equal midrank definition | One untuned rule; not equivalence or conditional redundancy |
| Mental-health H workload is lower than expected random workload | Direct paired difference: -8.9 pp [-15.8,-2.6] | Exploratory pointwise; length/marker workload differences include zero |
| Some criterion cases cluster near cutoffs | cutoff_diagnostics.csv, mean_distributions.csv, trigger_vote_distribution.csv | Descriptive; fixed +/-0.2 neighborhood; no criterion modification |
| Existing average-rating ICC is high | source_reliability.csv, reconstructed ICC points | Also report ordinal alpha; agreement does not establish validity or independence |
| 771 export/rated text pairs are byte-identical and 59 differ | text_provenance.csv and summary, score/source/tier replay | Export association not historical scorer-input authentication; mental-health scorer string unavailable separately |
| Lexical selected concern counts persist on export-text scoring at 20% | text_representation_sensitivity.csv | Does not establish identical selection sets, all-budget robustness, or correct joins |
| Intern declining/withdrawal would not affect role/pay/supervision/evaluation | Explicit author confirmation of consent/recruitment records, current conversation | Private documents not independently inspected; does not eliminate supervisory power differences |

The revised Overleaf manuscript supersedes the earlier Markdown draft for current presentation. The original analysis family and its hashes remain unchanged; new analyses are exploratory and separately versioned under revision/ and conditional/.

## Trained-screen amendment

| Claim | Evidence | Boundary |
|---|---|---|
| Adding HumT gives no clear incremental-recall gain in the specified screen at the reference fraction | conditional/outputs/conditional_lift.csv; nine paired intervals include zero | Exploratory, fixed logistic family and partition; not equivalence, conditional independence, or universal redundancy |
| New policies are evaluated without own-prompt training labels | fold_assignments.csv, oof_predictions.csv, fit_audit.csv; group/scaler/own-label-invariance tests | Other shared raters, sources, and templates remain possible dependencies |
| Training uncertainty is included | 2,000 paired within-fold cluster draws, both models refitted; bootstrap_differences.csv | Conditional on observed judgments and original partition; not simultaneous nine-cell inference |
| Education's positive D increment is unstable | Reference 7 to 8 cases; ten alternative partitions give -8.3 to 0.0 pp | Sparse seven concern-bearing prompts; no best-seed selection or independent replication |
| Fit/OA does not establish general HumT superiority | All original/fusion and held-out policy cells in generated tables | Separate batch capacities; sparse health OA; pointwise exploratory comparisons |
| Trained screens are not equally label-free alternatives | fit_audit.csv, five source ratings per training response | Reused historical labels; no estimated annotation time, price, or sum across overlapping fits |
| No LLM-judge evidence or new human validation is used | Model implementation, source hashes, AI-use disclosure | Codex assisted research preparation; actual human ratings preserved |

## Common-queue and accountability revision

| Claim | Evidence | Boundary |
|---|---|---|
| Domain-wide allocation can distribute review differently across recorded categories | allocation/outputs/category_coverage.csv and selection_register.csv; every category partition reconstructs original domain totals | Projection of a single queue, unlike earlier subgroup reranking; not causal discrimination or deployment frequency |
| General-health markers catch more fit cases overall but fewer natural-prompt fit cases in point counts | Overall 32 vs 25; natural 4 vs 8; paired_policy_differences.csv | Natural H--marker difference +5.4 pp [-1.3,+13.0] is uncertain; no confirmed superiority or policy preference |
| Mental-health OA coverage differs across recorded conditions under HumT | Natural 22/69, adversarial 9/64; adversarial-minus-natural -17.8 pp [-34.2,-5.0] | Exploratory pointwise, multiple comparisons, unmatched prompt sets; not causal condition effect |
| Different thresholds change the evaluation of a fixed queue | Fixed-policy selection invariance test; original threshold/consensus outputs | Do not claim changed queue membership without changing the policy; trained threshold variants were not evaluated |
| Surface cues overlap the D rubric without guaranteeing its labels | Source rubric attribution exclusions and functional first-person rule | Baseline performance does not establish HumT internals or general safety superiority |
| OA is a separate-rater endpoint | Final documented group arrangement | Different construct, not independent replication of D or external harm validation |
| Fraction-of-oracle equals precision when 0 < k <= P | Algebra: (T/P)/(k/P)=T/k | Redundant contextual quantity, not independent corroboration |
| Added figures show every paired comparison and original workload target | Generated assets read immutable original/conditional outputs | No new favorable effect, changed target, or simultaneous significance claim |

No practical equivalence claim is added without a substantively justified margin. No new evaluator, semantic judge, institutional determination, AI model version, release clearance, or publication authorization is assumed. The existing source limitations and disclosure remain.

## Final computational-only claim freeze

This is a freeze of presentation on explored data, not new preregistration. RQ1 maps
to original full-batch comparisons; RQ2 to the trained amendment; RQ3 to the
common-queue amendment. Changing their presentation does not promote the latter two
to primary tests. The original three-domain H-versus-random D family remains intact.

| Claim | Traceable evidence | Permitted interpretation |
|---|---|---|
| Existing identical-text subset results reconstruct independently of join tier | consolidation/outputs/verified_subset_operating_points.csv, 48 rows | Verification of available-string sensitivity; not historical API authentication |
| Excluded education rows contain two F cases, no D/OA cases; excluded health rows contain none | consolidation/outputs/subset_composition.csv, all-category rows | Composition matters; nonconcern candidates still affect queue competition |
| Baseline comparisons address cheap transparent screening, not strongest evaluators | Fixed policy definitions and conditional/config.json | No semantic-judge or state-of-the-art competitiveness claim |
| Category examples were chosen for interpretation after the complete analysis | allocation/plan.md and complete 525-cell outputs | Exploratory illustrations; no new primary test or population-fairness claim |
| Same data can support a genuinely different decision analysis | submission/distinctness_assessment.md, updated section mapping | Does not by itself establish publishable novelty or venue permission |

The main document uses a concrete review purpose, not claimed organizational adoption.
All-zero-crossing incremental intervals remain non-establishment, not evidence of equivalence.
