# PERSONA FAccT: Review Allocation Study

Private research repository, originally snapshotted on **16 October 2026**.
The capability-grounded direction adopted on **23 October 2026** was superseded
on **24 October 2026**: the author chose no new experiments for this deadline and
restored the completed audit as the paper's evidence basis. Capability materials
remain future-work preparation, not submission findings.

## Study

**When Tone Scores Allocate Attention: Auditing HumT-Based Review Prioritization**

The October 26 professor revision asks RQ1 enrichment, RQ2 comparative allocation,
RQ3 incremental benefit, and RQ4 coverage in a shared queue. The narrative relies
on completed audit analyses, the supplied mental-health assessment follow-up and
new input-window/strict-cutoff checks. Original results and ratings are preserved.
There are no new capability experiments, capability-conditioned
judgments, or semantic-screen results. The [capability materials and scaffold](facct/capability/README.md)
are retained for future work only. Superseded FAccT manuscripts and packages
are recoverable from Git history, not competing active drafts.

This study asks whether automated human-like tone scores help allocate limited human review. It compares HumT with random selection, conversational markers, response length, and a specified trained lexical screen. It evaluates captured and missed rubric-defined concerns, incremental recall, and coverage across contexts.

The response corpus contains 1,490 responses: mental health 660, education 415, and general health 415. A new assessment follow-up covers the existing mental-health responses, not a new response corpus. Its resolved labels identify 19 concern cases; at 132 review slots, HumT captures six and normalized markers twelve. The paired exploratory intervals cross zero. Adding HumT to the trained lexical screen establishes no clear recall gain across the nine original domain/criterion comparisons.

## Current Materials

- [Active manuscript source](facct/paper/overleaf/main.tex)
- [October 26 Overleaf package](facct/releases/PERSONA_FAccT_Overleaf_2026-10-26_professor.zip)
- [Professor response and verified new findings](facct/submission/professor_response_2026-10-26.md)
- [Reproduce the new checks](facct/professor_revision/README.md)
- [Latest presentation: 15 slides, workflow and capacity formula, no presenter name/date](facct/presentations/output/PERSONA_FAccT_Talk_No_Name_Date.pptx)
- [Full research guide and analysis commands](facct/README.md)
- [Assessment follow-up](facct/independent_annotation/README.md)
- [Current scope and pending decisions](facct/submission/current_scope.md)
- [Readiness record](facct/submission/readiness.md)
- [Snapshot provenance and exclusions](SNAPSHOT.md)

The revised source compiles with the native compiler and isolated pdfLaTeX.
The [October 26 layout audit](facct/paper/qa/2026-10-26/layout_report.json) records
14 main-content pages, one endmatter page, two reference pages and 14 appendix
pages: 31 total. Only the latest release ZIP is retained. All 61 exclusive cases have
an assistant-generated coding draft for author review; the paper reports their
existing-label profiles, not unverified semantic-coding results.

## Repository Layout

`facct/` contains this study's code, protocols, results, manuscript, study materials and presentation. The root `analysis/`, `data/`, `paper/`, `docs/`, and `submission/chi2027_supplement/` directories are inherited CHI reference material. They remain at their original paths because the FAccT pipeline imports them and verifies their hashes. The root `paper/` is **not** the current FAccT manuscript.

This repository has a new independent Git history. It does not replace, push to, or rewrite [PERSONA-MH-CHI](https://github.com/92meharali/PERSONA-MH-CHI). Historical manifests and documents retain their original source revision and contemporaneous status statements.

## Verification and Reproduction

Use Python 3.12 and install the pinned dependencies in an isolated environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r facct/requirements.txt
python -m facct.analysis.verify_outputs
python -m pytest facct -q
```

The full computational rerun command is `python -m facct.consolidation.verify --fresh-env`; the earlier recorded runtime was about eight minutes. Read the full research guide before regenerating any outputs. Verification records committed here document the preserved run, not a claim that every analysis has been rerun during this repository migration.

The follow-up raw assessor returns and private consent/eligibility records are **not** included. Its reconstruction command requires the authorized external source directory. The submitted CHI PDF also remains an external input. These limitations must not be represented as complete standalone reproduction of those stages.

The original `SNAPSHOT_MANIFEST.json` and `scripts/verify_snapshot.py` describe
the initial migration, not the revised working tree. They are retained as historical
records and have not been rewritten to conceal changes. Current checks are the
analysis verifier, package manifest and test suite above. See the
[cleanup record](facct/submission/repository_cleanup_2026-10-26.md) for scope and recovery.

## Status and Access

This is an unpublished internal-review snapshot, not a submitted or accepted FAccT paper. Assessor documentation and publication-overlap decisions remain subject to the recorded author checks. No chair contact or submission is authorized by this archive operation. Keep the repository private; review source rights, participant privacy and venue anonymity before sharing it more broadly. No new blanket data license is granted by this snapshot.
