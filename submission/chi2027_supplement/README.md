# PERSONA anonymous supplementary materials

This supplement supports review and replication of the manuscript, *Beyond
Human-Likeness: A Context-Aware Framework for Evaluating Appropriateness in
Anthropomorphic AI Responses*.

The main paper is self-contained. These files provide the full scoring
protocols, anonymized analysis data, analysis code, and machine-readable result
tables behind the reported findings.

## Contents

| Path | Contents |
|---|---|
| `ETHICS_AND_PARTICIPANT_PROTECTIONS.md` | Anonymous ethics-review context and participant safeguards |
| `ANONYMIZATION_AND_DATA_HANDLING.md` | Anonymization, sensitive-content, and review-use notes |
| `PROTOCOL_APPLICATION_NOTE.md` | How the two instruments and separate rater pools were implemented |
| `MATERIALS_SCOPE.md` | Included and deliberately excluded materials |
| `SOURCE_AND_MODEL_PROVENANCE.md` | Prompt sources, model endpoints, HumT, and redistribution status |
| `DATA_DICTIONARY.md` | Definitions for the two analysis datasets |
| `REPRODUCIBILITY.md` | Environment, commands, expected outputs, and scope |
| `protocols/` | Full mental-health, education, and general-health annotation protocols |
| `analysis/` | Deterministic analysis source and pinned Python dependencies |
| `analysis/processed/` | Response-level consensus data and anonymous rating-level data |
| `analysis/outputs/` | Generated tables, reports, figures, and machine-readable results |
| `MANIFEST.sha256` | SHA-256 checksums for all other files |

## Important interpretation notes

- `OA` was elicited by three distinct five-person domain pools (15 Group A
  raters total).
- `E`, `D`, and `F` were elicited by a separate five-person Group B pool.
- No individual rated both `OA` and the diagnostic dimensions.
- `H` is the automated HumT human-likeness score.
- Higher `D` means greater deception risk; therefore, negative `D`--`OA`
  associations are directionally expected.
- General-health findings are exploratory because of outcome ceiling
  restriction, sparse `D` variation, and bootstrap intervals crossing zero.
- Group B included author-team members and research interns familiar with the
  framework. This expectancy risk is a limitation, despite separate elicitation
  of `OA`.

## Review status and reuse

This is an anonymized review package, not the final public data release and not
a grant of a data or software license. A public release is planned upon
acceptance, subject to institutional and source-dataset requirements. The
package contains potentially distressing mental-health and health scenarios;
please handle it accordingly.
