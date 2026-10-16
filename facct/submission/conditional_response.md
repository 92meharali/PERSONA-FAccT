# Response to the Four Follow-up Comments

Prepared 2 October 2026. This records completed work, not acceptance, publication clearance, or independent validation.

| Comment | Implemented | What the evidence permits |
|---|---|---|
| Run conditional lift and rewrite complementarity | Compared logistic regression using markers/log-length against the identical model plus HumT; five prompt-group folds; 2,000 paired refitted cluster draws per domain; ten further partitions | All nine incremental-recall intervals include zero. Different selected cases do not establish improved combined allocation; null results do not establish universal redundancy |
| Add a trained or LLM-judge comparator, or narrow the claim | Added transparent criterion-specific trained screens, training-only standardization, no tuning, matched held-out batches, saved predictions/coefficients, and label acquisition requirements | A tested low-dimensional model, not the best possible screen, a semantic judge, or a label-free alternative. No LLM judge or new labels were fabricated |
| Report all fit/OA cells and soften the conclusion | Generated every reference-budget policy cell: 45 full-batch original/fusion rows plus 63 common-held-out rows; all 252 trained-evaluation budget cells retained in CSV | Education-fit behavior is not generalized to other criteria/domains; negative and sparse cells are visible, and point comparisons are not promoted to proven policy superiority |
| Fix wording and disclosure | Revised abstract, RQ1, methods, results, discussion, limitations, conclusion, AI-use statement, and author documentation | Proposed offline simulation; rubric judgments not harm; no proven complementarity, equivalence, external validation, real-world adoption, or submission eligibility |

## Main incremental results

At the reference fraction, reduced -> extended concern counts are:

| Domain | D >= 3 | F < 4 | OA < 4 |
|---|---|---|---|
| Mental health | 70 -> 66 / 165 | 32 -> 33 / 95 | 26 -> 30 / 133 |
| Education | 7 -> 8 / 12 | 13 -> 13 / 25 | 12 -> 12 / 18 |
| General health | 21 -> 21 / 23 | 29 -> 30 / 120 | 8 -> 8 / 9 |

Read these as `(reduced count -> extended count) / all criterion cases`. Full intervals and all split ranges are in the generated [findings](../conditional/outputs/findings.md). The education D increase is only one case and does not recur positively in any of the ten alternative splits. Every reference-partition interval includes zero, with uncertainty especially broad in sparse cells.

## Comparison and inference safeguards

- These new policies share held-out quotas: 130/660 mental health, 80/415 education, 80/415 general health. Original full-batch tables use 132/83/83 and remain separate. Raw cross-fold probabilities are never pooled for ranking.
- Every response to a prompt stays in its fold, including repeated bootstrap copies. Each scaler and model is refitted without its held-out prompts. The bootstrap conditions on the fixed partition and empirical labels, not unseen population truth.
- Separate screens are fitted for D/F/OA. Historical labels are not test-time features. Per-fit training requires 528, 331-334, and 331-333 labeled responses respectively, each derived from five ratings; overlapping fits are not separate label purchases.
- All nine intervals are exploratory pointwise intervals, not confirmatory or simultaneous tests. The original three-domain primary family is unchanged.
- Education and health have single-class training fallbacks in 68 and 50 of 2,000 bootstrap draws across all criteria/models; none in point fits. Undefined paired differences remain recorded, with 1,998 valid education-D and health-OA draws.
- Original data, scores, CHI results/manuscripts, original computational outputs, and first-amendment outputs were preserved and hash-checked.

## Files and verification

The added reproducible module is `facct/conditional/`; the existing open Overleaf manuscript remains authoritative. Build-generated tables are sourced from frozen original/revision outputs and the new conditional manifest. The portable package includes the unchanged ACM template and the same 16 verified references; this amendment adds no bibliographic entries.

The paper retains a concise account of shared CHI data and framework. The unsent overlap disclosure now includes the trained-screen amendment and its inconclusive incremental results; a new model alone does not settle publication distinctness. No chair draft was sent or account connected.

Run `python -m facct.conditional.run` from the repository root; measured runtime was 178 seconds. Rebuild the ZIP with `python -m facct.paper.build_overleaf`. Full-project compilation and layout still require Overleaf because the native single-document compiler cannot load project auxiliary files. Remaining source authentication, anonymity/rights, author approval, and publication-policy decisions are not falsely marked complete. Chair contact remains with the author; no external communication or push was made.

Final verification: all **48 tests passed**. A second full 2,000-draw-per-domain run took 179 seconds and reproduced all eight result CSVs and the findings report byte-for-byte. All 228 protected input/history files remain hash-identical. The [machine-readable verification record](conditional_verification.json) records the output comparisons and final ZIP checksum. Native compilation was attempted on the existing open source and stopped at the unsupported auxiliary-file include; no compiled PDF, page count, or overflow check is claimed.
