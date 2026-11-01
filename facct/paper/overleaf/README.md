# PERSONA: FAccT 2027 Overleaf manuscript

## Compile

Upload this ZIP as an Overleaf project, choose `main.tex`, and use pdfLaTeX.
Recompile from scratch if an interrupted build leaves unresolved citations.
The package includes 26 cited references, generated result tables, vector figures,
and the unmodified ACM v2.19 class and bibliography style. No shell escape or
external data download is needed for typesetting.

## Current revision: 28 October 2026

Title: **When Scores Allocate Attention: Auditing Criteria and Tone in AI Review**.
The manuscript integrates the PERSONA measurement diagnostic, review-allocation
audit and contextual-reviewworthiness follow-up. A new exploratory computation
changes the training target while fixing learner, features and held-out capacity,
then evaluates each queue against all criteria. Original sources and prior
numerical results are unchanged. The follow-up is evaluation-only in this new
analysis and adds judgments on existing responses, not a new response corpus.

This revision retains the earlier review corrections and adds:

- RQ1 criterion transfer; RQ2 policy comparison; RQ3 incremental HumT value;
  RQ4 category coverage. The original three primary comparisons remain unchanged.
- 240 trained operating points, 60 reference-budget target contrasts, 2,000
  paired refit resamples per domain and ten alternative partitions.
- A complete main-text cross-criterion count matrix and seven generated tables.
- A bounded bridge from fit/OA prediction to review queues, not a claim of
  independently validated PERSONA constructs or an optimal training target.
- Two verified primary references: Obermeyer et al. (2019) and Passi/Barocas (2019).
- Clearer separation of human-rating predictors from deployable text features.

No new scores, annotations, semantic-judge experiment, independently sourced
marker list or participant study is claimed. Historical scorer calls and
pre-inspection marker-list selection are not authenticated. The author checklist
retains these evidence boundaries.

## Format and verification

The official author guide, checked 28 October 2026, permits 14 single-column
content pages including figures/tables, one additional endmatter-only page, and
unlimited references and appendices in the same PDF:
https://facctconference.org/2027/authorguide.html

The local pdfLaTeX build has **14 content pages, 1 endmatter page, 2 reference
pages and 23 appendix pages: 40 total**. Appendix sections start on separate
pages to prevent floats appearing under the wrong heading. Total PDF length is
not the main-content limit. The saved source also compiles in the desktop editor.
No fonts or margins were reduced. Check `package_manifest.json` for hashes and
the layout report, and recheck pagination after any Overleaf edits.

Existing numerical tables are unchanged. New tables are generated from the
criterion-transfer outputs and the recorded OA-prediction diagnostic. New
operating points are independently reconstructed from earlier held-out predictions.
The two added citations acknowledge direct precedents rather than claim a new
algorithm. No undefined citations/references or overfull boxes remain in the local
pdfLaTeX log. Generic class notices and incomplete optional bibliographic metadata
warnings are not missing citations or compilation failures.

## Contents and boundaries

- `main.tex`: manuscript, ethics/AI-use endmatter and appendices.
- `references.bib`: 24 retained records plus two verified primary-source additions.
- `tables/`, `figures/`: generated presentation assets, not source judgments.
- `acmart.cls`, `ACM-Reference-Format.bst`, `template-source/`: unchanged template.
- `AUTHOR_CHECKLIST.md`: author checks, not part of the compiled paper.
- `package_manifest.json`: package checksums and verification status.

The package excludes raw participant records, identifying institutional documents,
source response datasets and prospective human-study materials. It is a portable
typesetting package, not a standalone full-data reproducibility release. The
prepared semantic-judge runner and exploratory in-chat scoring are outside the
paper; neither is represented as an independent semantic comparator.
