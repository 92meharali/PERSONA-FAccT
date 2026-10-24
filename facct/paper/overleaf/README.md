# PERSONA: FAccT 2027 Overleaf manuscript

## Compile on Overleaf

1. Choose **New Project > Upload Project** and upload this ZIP.
2. Set **Main document** to `main.tex` and compiler to **pdfLaTeX**.
3. Use the newest available TeX Live environment and recompile. Overleaf's normal build runs BibTeX automatically. If references show question marks after an interrupted build, use **Recompile from scratch**.

The main document, 18 cited references, generated result tables, vector figures, and ACM template files are included. No external image download, shell escape, custom font installation, or separate data download is needed to typeset the paper.

## Format and status

This draft reports the **completed audit and supplied mental-health assessment follow-up only**. The capability experiment is deferred. A provider-neutral LLM-judge runner is prepared separately, but no external calls or independent judge results are reported. A full in-chat exploratory pass is documented outside the paper; it is not a version-pinned or isolated comparator and does not change the main claims. The author confirms that institutional and recruitment records are available. The document uses `acmart` options `manuscript,screen,review,anonymous`; single-column output is intentional.

The official FAccT 2027 author guide and FAQ, checked on **24 October 2026**, allow **14 main-content pages including figures and tables**, **one additional endmatter-only page**, and unlimited reference and appendix pages. Appendices must be at the end of the same PDF; the main paper must stand alone. Ethics and generative-AI-use statements are retained, with identifying acknowledgments omitted. No template margins or fonts were reduced. See `package_manifest.json` for rendered page-count verification rather than judging compliance by the PDF's total length.

Official guide: https://facctconference.org/2027/authorguide.html

The October 24 pdfLaTeX build has **14 main-content pages + 1 endmatter page + 1 reference page + 12 appendix pages = 28 total pages**. The saved source also compiled successfully in the desktop editor. All pages were inspected in a contact sheet, with enlarged checks of the paired figure, main/endmatter boundary and dense appendix tables. No overfull boxes or unresolved citations/references remain. Overleaf or later edits can change pagination; recheck there before submission. This verifies layout, not unresolved author reporting or eligibility.

The bundled unmodified ACM class is **v2.19 (27 June 2026)** from the existing project, with its matching repository bibliography style. CTAN now lists v2.20, but this package deliberately retains the available template rather than silently substituting uncompiled class code. The original v2.19 source and license notices are supplied in `template-source/acmart.dtx` from https://github.com/borisveytsman/acmart/tree/v2.19. ACM class copyright and LPPL terms remain intact. No template fonts or margins have been modified.

## Contents

- `main.tex`: full manuscript, endmatter, and appendices.
- `references.bib`: 18 references, retaining the existing 17 and adding AnthroBench after checking its official ICLR 2026 proceedings record.
- `tables/`: generated original and post-review numerical tables and macros. Do not manually change result values.
- `figures/`: separate mental-health and transfer budget panels, D-mean distributions, and the original nine-panel asset retained for history.
- `figures/paired_summary.*` and `figures/workload_targets.*`: complete paired baseline/incremental comparisons and all four original workload targets with uncertainty for every policy.
- `acmart.cls`, `ACM-Reference-Format.bst`: unmodified template files.
- `AUTHOR_CHECKLIST.md`: decisions and checks before actual submission; not included in the compiled paper.
- `package_manifest.json`: checksums and validation status; no identifying local paths.

The package does not include raw response text, participant records, institutional letters, a CHI submission PDF, or uncompleted human-study materials. It is a typesetting package, not the full reproducibility supplement.

## Revision status

### Completed-evidence submission restored on 24 October 2026

Current title: *When Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization*. RQ1 concerns comparative allocation, RQ2 incremental value, and RQ3 shared-queue coverage. The review revision leads with three findings, clarifies who allocates review and bears its costs, and moves detailed join diagnostics to the appendix. Source reuse is disclosed neutrally, and author-confirmed institutional wording replaces outdated pending-record descriptions. All numerical tables, figures, original scores, judgments and citations are unchanged. The independent semantic comparator remains preparation only; exploratory in-chat outcomes must not be substituted for it.

### Historical capability direction, 23 October (superseded above)

Current title: *From Tone Scores to Capability Evidence: Auditing Review Allocation for Anthropomorphic AI*. New prospective RQs concern capability sensitivity, allocation value and information requirements. Completed results are labeled audit questions A1-A3; none of their numerical tables were changed. The main protocol now specifies fixed-text capability contrasts, independent judgments, the same semantic judge with/without evidence, a simple consistency baseline, invariant controls, unknown information and costs. The previous broad bounded/open-ended proposal remains a separate future question rather than the immediate experiment. New assessments, capability verification and semantic model runs remain pending. The package contains no invented new results and no raw candidate texts.

### Earlier design-assumption revision (superseded in scope above)

The manuscript now distinguishes chatbot design from screening-policy design, explains PERSONA's evaluation role and label-acquisition costs, and connects capability assumptions to reviewworthiness. A discussion subsection and a clearly prospective appendix describe a focused matched bounded/open-ended design comparison, candidate concern types, independent contextual screening, and prevalence-versus-recall reporting. These are proposed experiments, not new findings. The current research questions, numerical results, source annotations, bibliography, and ACM template are unchanged. This revision concerns the review-allocation paper, not the separate joint CSR proposal.

The mental-health follow-up's 6/19 versus 12/19 comparison remains separate from general-health natural-prompt fit coverage of 8/74 versus 4/74. No result was relabeled as a chatbot-design effect.

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

On October 24 the author confirmed that institutional and recruitment records are
available. Earlier pending-record language is superseded by that confirmation.
Private records are not bundled here, and unspecified individual backgrounds,
payment terms or approval identifiers have not been invented.
