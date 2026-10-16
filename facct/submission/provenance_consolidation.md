# Final available-record provenance assessment

Date: 2 October 2026. No source annotations or historical outputs modified.

| Record | Evidence available | What remains unestablished |
|---|---|---|
| Current response scores and ratings | Stored means reconstruct from five ratings; all 1,490 response records retained | Real-world identities cannot be authenticated by anonymous stream IDs |
| Imported H association | Existing replay reproduces scores, source filenames, tiers and source-row links | Matching a deterministic join is not proof of historical scorer input |
| Transfer export/rated strings | 359/415 education and 412/415 health pairs are byte-identical; source hashes rechecked | Export strings are not independently authenticated invocation logs |
| Differing strings | 56 education pairs contain two F cases and no D/OA cases; three health pairs contain none | Nonconcern candidates still compete for slots; this is not proof of harmless join error |
| Existing subset sensitivities | All 48 points reconstructed using byte equality rather than tier; both same capacity and same fraction preserved | No causal estimate of join error or new independent validation |
| Mental-health H | Embedded scores for all 660 responses | No separate historical scorer-input string |
| CHI version linkage | Available PDF numerical checks and repository supplement hashes agree | Exact portal-uploaded ZIP still supported only by tentative author recall |
| Personnel and consent | Final repository account plus author confirmation of withdrawal safeguards | Private records were not independently inspected |

The repository inventory contains a scorer implementation, generation notebooks,
HuMT CSV exports, join reports and provenance audits. Code capable of generating a
score is not a historical invocation record. No newly authenticated per-call record
was supplied or identified in this consolidation. This is a bounded available-record
assessment, not a claim that no such records exist elsewhere.

Machine-readable composition by condition/model/scenario is in
`facct/consolidation/outputs/subset_composition.csv`; the independently reconstructed
descriptive operating points are in `verified_subset_operating_points.csv` alongside
the audit manifest. No fresh model score was substituted for a historical score.

The manuscript may report robustness of specified observed operating points, not
blanket join correctness. Authentication remains open; factual uncertainty is not
silently marked resolved because the available sensitivity check is reassuring.

## Additional available-field check

The scorer implementation `compute_humt_sociot_colab.py` truncates to the first 300
characters and exports `text_trunc`. All 830 recorded truncations equal the available
export prefix. Only 369/415 education and 414/415 health prefixes match the rated
text's first 300 characters. Twelve of the 59 full-string discrepancies therefore
preserve the recorded prefix; 47 do not. This narrows what is known about available
preprocessing, not historical invocation identity/version. It does not justify
replacing the conservative full-string subset or silently declaring the 12 pairs
authenticated. These checks and the scorer-code hash are recorded in the new manifest.
