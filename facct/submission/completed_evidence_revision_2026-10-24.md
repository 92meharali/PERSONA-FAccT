# Completed-evidence revision: 24 October 2026

## Decision and changes

The author deferred new experiments because of the deadline. The active paper is
*When Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization*.
RQ1 concerns comparative allocation, RQ2 incremental value, and RQ3 coverage
within a shared queue. The abstract, introduction and conclusion now describe
completed evidence rather than a promised capability experiment.

- Removed the prospective capability-study section, prospective research questions
  and readiness appendix from the submission manuscript.
- Preserved the previous manuscript in
  `facct/capability/archive/main_capability_prospective_2026-10-23.tex` and retained
  all separate capability-study materials. The paper has one future-work paragraph.
- Shortened repetition without changing ratings, criteria, statistical results,
  tables, numerical macros or figures. No new experiment was run.
- Moved the workload figure and supporting slot-allocation table to appendices;
  retained key numerical findings and uncertainty in the main text. All fit/OA
  comparison cells remain available.
- Preserved actual assessor-note version differences, exploratory status,
  uncertain follow-up contrasts, ethics and substantial AI-assistance disclosure.
- Updated scope/readiness documentation, claims ledger, package instructions and
  author checklist. Historical preparation records remain marked as historical.

## Format and verification

The official [FAccT 2027 author guide and FAQ](https://facctconference.org/2027/authorguide.html)
were checked on October 24: 14 main-content pages including figures/tables, one
additional endmatter-only page, unlimited references and appendices. Appendices
belong at the end of the same PDF, and the main paper must stand alone.

The actual pdfLaTeX build contains **14 main pages, 1 endmatter page, 1 reference
page and 12 appendix pages: 28 total**. The class is unchanged; fonts and margins
were not compressed. The desktop editor also compiled the saved source successfully.
There are no unresolved references/citations or overfull-box warnings. Generic ACM
warnings about CCS concepts and suppressed ACM reference format remain; BibTeX
also reports incomplete optional publication metadata, not missing citation keys.

All 28 pages were visually surveyed in a contact sheet. Enlarged checks covered
the main paired figure, pages 14/15 boundary and dense appendix tables. The layout
report binds counts to source, bibliography, class and PDF hashes:
`facct/paper/qa/2026-10-24/layout_report.json`.

The original-output verifier independently checked 144 ranked operating points
and source/output integrity. The targeted capability, manuscript/package and
screening suite passed **39 tests**. The 42-file ZIP was read back and compared
byte-for-byte with the package sources. `git diff --check` passed.

Package: `facct/releases/PERSONA_FAccT_Overleaf_2026-10-24_chat_audit.zip`.
The generic Overleaf ZIP and extracted release directory are synchronized.
The October 23 ZIP is historical. Recheck pagination on Overleaf after uploading
or editing; local pagination does not guarantee an identical later engine layout.

## Still requiring the authors

Follow-up assessor backgrounds, recruitment/payment particulars and supporting
ethics/consent records require completion. Author attestations were not replaced
with invented documentary verification. CHI distinctness, accurate disclosure,
concurrent-review status and venue eligibility remain author responsibilities.
Chair contact remains assigned to the author. No GitHub push, submission, public
release or contact with chairs was performed in this revision.
