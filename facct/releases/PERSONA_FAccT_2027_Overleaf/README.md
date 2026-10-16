# PERSONA: FAccT 2027 Overleaf manuscript

## Compile on Overleaf

1. Choose **New Project > Upload Project** and upload this ZIP.
2. Set **Main document** to `main.tex` and compiler to **pdfLaTeX**.
3. Use the newest available TeX Live environment and recompile. Overleaf's normal build runs BibTeX automatically. If references show question marks after an interrupted build, use **Recompile from scratch**.

The main document, 17 cited references, generated result tables, vector figures, and ACM template files are included. No external image download, shell escape, custom font installation, or separate data download is needed to typeset the paper.

## Format and status

This is an internal-review manuscript combining the computational audit with a new mental-health assessment follow-up. It is not a promise that submission is eligible or that human-study reporting is complete. It uses the official `acmart` review options `manuscript,screen,review,anonymous`. Single-column output is intentional.

The FAccT 2027 author guide checked on 2 October 2026 specifies 14 content pages including tables and figures, unlimited references, and an additional endmatter page. Appendices belong in the same PDF. Check the complete compiled layout before submitting. The latest built-in single-document compile loaded an ACM class but stopped at `tables/numbers.tex`: that compiler does not load this project's auxiliary files. The table file and class are present in this ZIP for Overleaf, and package tests verify them. No local multi-file TeX compiler was available, so compilation, overflow, and final page count remain unverified. Static checks passed for included assets, citations, labels, balanced braces, anonymous identifiers, and ZIP integrity.

Official guide: https://facctconference.org/2027/authorguide.html

The bundled unmodified ACM class is **v2.19 (27 June 2026)** from the existing project, with its matching repository bibliography style. CTAN now lists v2.20, but this package deliberately retains the available template rather than silently substituting uncompiled class code. The original v2.19 source and license notices are supplied in `template-source/acmart.dtx` from https://github.com/borisveytsman/acmart/tree/v2.19. ACM class copyright and LPPL terms remain intact. No template fonts or margins have been modified.

## Contents

- `main.tex`: full manuscript, endmatter, and appendices.
- `references.bib`: 17 references checked against primary publication records, including the publisher-verified OpenL2D/FiFAR capacity-aware benchmark.
- `tables/`: generated original and post-review numerical tables and macros. Do not manually change result values.
- `figures/`: separate mental-health and transfer budget panels, D-mean distributions, and the original nine-panel asset retained for history.
- `figures/paired_summary.*` and `figures/workload_targets.*`: complete paired baseline/incremental comparisons and all four original workload targets with uncertainty for every policy.
- `acmart.cls`, `ACM-Reference-Format.bst`: unmodified template files.
- `AUTHOR_CHECKLIST.md`: decisions and checks before actual submission; not included in the compiled paper.
- `package_manifest.json`: checksums and validation status; no identifying local paths.

The package does not include raw response text, participant records, institutional letters, a CHI submission PDF, or uncompleted human-study materials. It is a typesetting package, not the full reproducibility supplement.

## Revision status

The manuscript includes agreement estimates, cutoff stability, oracle/lift context, fixed rank fusion, paired workload differences, text-provenance sensitivity, and a later prompt-group-held-out trained comparison. That comparison adds HumT to a logistic screen using markers and log-length, with 2,000 paired refitted bootstrap draws per domain and ten additional split checks. All nine incremental-recall intervals include zero, without establishing equivalence or universal redundancy. Complete D/F/OA tables report every original/fusion and held-out policy cell at the reference fraction. Full-batch and held-out capacities differ and are explicitly separated.

All additions are post-review exploratory analyses; the original primary comparison family is unchanged. The models use historical human training labels, not LLM-judge outputs. No external validation or deployment effectiveness is claimed. The ethics section includes the author's confirmation that consent/recruitment records explicitly protected interns' role, pay, supervision, and evaluation if they declined or withdrew; private documents were not independently inspected during preparation.

The common-queue audit ranks each full domain once before examining existing categories;
it does not give each category a separate quota. The final computational-only
consolidation organizes Results into comparative allocation, held-out incremental
benefit, and common-queue coverage. Detailed criterion/provenance checks are in a
referenced appendix, with essential limitations remaining in main text. The new
provenance composition table is generated from verified source-string comparisons.
No historical scorer-input authentication is claimed. The comparator scope excludes
state-of-the-art semantic-evaluator claims. No new threshold or annotation was invented.

## Assessment follow-up integrated on 10 October

Two complete assessment streams cover all 660 existing mental-health responses;
a third assessor covers their 14 binary disagreements. Resolved labels identify
19 cases in 13 prompt clusters. The original HumT queue captures 6 versus 12 for
normalized markers at 132 slots. The paired recall difference is -31.6 percentage
points with a wide exploratory interval [-66.7, +4.3]; HumT versus expected random
also has an interval crossing zero. This does not establish general superiority.

Four generated tables cover the main comparison, all rater/target sensitivities,
four budgets and legacy-label intersections. Capability-note version differences,
selective third assessment, imported queue discrepancies and text encoding are
reported. Original labels, queues, trained results and references are unchanged.
No new corpus, independent criterion design or practitioner validation is claimed.

The author confirms prior consent/ethics coverage and assessor separation, but
backgrounds, recruitment/compensation details and an approval reference remain
deferred. The manuscript explicitly retains this internal-review reporting gap.
Do not submit before resolving it and completing layout/eligibility checks.
