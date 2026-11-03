# PERSONA FAccT: Review Allocation Study

## Current Release: 3 November 2026

**When Tone Scores Allocate Attention: Auditing Human-Like Tone for Budgeted
Review of Chatbot Responses**

The current paper incorporates the professor's revision, including a
self-contained corpus/rubric account, editable workflow, fixed semantic and
trained comparisons, complete sensitivity results and verified references.
It evaluates review allocation, not downstream reviewer effectiveness or
the validity of a general appropriateness-prediction framework.

- [Active Overleaf source](facct/paper/overleaf/main.tex)
- [Compiled paper](facct/paper/overleaf/main.pdf)
- [Complete Overleaf ZIP](facct/releases/PERSONA_FAccT_Professor_Revision_2026-11-03.zip)
- [Changes and author checks](facct/concern_detector_eval/notes/professor_revision_response.md)
- [Analysis, tests and reproduction](facct/concern_detector_eval/README.md)
- [Release manifest](facct/paper/overleaf/package_manifest.json)

The compiled PDF contains **12 main-text pages, one endmatter page, two
reference pages and 28 appendix pages**. All 20 extension tests pass. No
unresolved citations, references or overfull boxes were found in the release.
On 3 November the author confirmed follow-up assessor compensation through
existing paid research roles; the manuscript placeholder is resolved. Authors
still need to check actual tool-use details, the Overleaf build and submission
portal requirements. Uploading to GitHub is not conference submission.

At 132 mental-health review slots, the independent follow-up captures are
HumT 6/19, markers 12/19, length 4/19, similarity 4/19 and NLI 2/19, versus a
random expectation of 3.8/19. The HumT-marker interval includes zero. Semantic
scores were cached; no new model calls or participant judgments were made.
Source data are unchanged. Private study inputs are required to reproduce
the follow-up join and are not included in the release.

GitHub reported this repository as **public** on 3 November 2026. The
anonymous Overleaf ZIP contains no private participant records; the repository
itself is not anonymous. Check venue anonymity and source-sharing requirements
before sharing the repository with reviewers.

## Historical Overview (Superseded)

The remainder records the earlier October 28 state, not the current release.
Its older package links, page counts and absence of semantic comparisons do
not describe the November 3 manuscript. Historical analyses remain available
without altering their original results.

Private research repository, originally snapshotted on **16 October 2026**.
The capability-grounded direction adopted on **23 October 2026** was superseded
on **24 October 2026**: the author chose no new experiments for this deadline and
restored the completed audit as the paper's evidence basis. Capability materials
remain future-work preparation, not submission findings.

## Study

**When Scores Allocate Attention: Auditing Criteria and Tone in AI Review**

The October 28 integration asks RQ1 criterion transfer, RQ2 comparative allocation,
RQ3 incremental benefit, and RQ4 coverage in a shared queue. It connects the earlier
OA-prediction diagnostic to a new crossed training-target/evaluation-target audit.
The original primary family is unchanged. Original results and ratings are preserved.
There are no new capability experiments, capability-conditioned
judgments, or semantic-screen results. The [capability materials and scaffold](facct/capability/README.md)
are retained for future work only. Superseded FAccT manuscripts and packages
are recoverable from Git history, not competing active drafts.

This study asks how criterion choice and score choice allocate limited human review. It compares HumT with random selection, conversational markers, response length and a specified trained lexical screen, then changes the screen's training target while keeping its learner/features/capacity fixed. It evaluates captured and missed concerns, not downstream review effectiveness.

At 130 held-out mental-health slots, fit-trained and OA-trained lexical screens
share 107 selections, capturing 9 versus 11 contextual-reviewworthiness cases.
All ten fit-minus-OA recall contrasts include zero for each feature set. Different
queues do not establish an optimal target or validate PERSONA's constructs.

The response corpus contains 1,490 responses: mental health 660, education 415, and general health 415. A new assessment follow-up covers the existing mental-health responses, not a new response corpus. Its resolved labels identify 19 concern cases; at 132 review slots, HumT captures six and normalized markers twelve. The paired exploratory intervals cross zero. Adding HumT to the trained lexical screen establishes no clear recall gain across the nine original domain/criterion comparisons.

## Current Materials

- [Active manuscript source](facct/paper/overleaf/main.tex)
- [Latest Overleaf package](facct/releases/PERSONA_FAccT_Overleaf_2026-10-28_integrated.zip)
- [Integration decisions and results](facct/submission/integration_review_2026-10-28.md)
- [Criterion-transfer analysis](facct/criterion_transfer/outputs/findings.md)
- [Response to the annotated PDF and checklist](facct/submission/review_response_2026-10-27.md)
- [Professor response and verified new findings](facct/submission/professor_response_2026-10-26.md)
- [Reproduce the new checks](facct/professor_revision/README.md)
- [Latest presentation: 15 slides, workflow and capacity formula, no presenter name/date](facct/presentations/output/PERSONA_FAccT_Talk_No_Name_Date.pptx)
- [Full research guide and analysis commands](facct/README.md)
- [Assessment follow-up](facct/independent_annotation/README.md)
- [Current scope and pending decisions](facct/submission/current_scope.md)
- [Readiness record](facct/submission/readiness.md)
- [Snapshot provenance and exclusions](SNAPSHOT.md)

The revised source compiles with the native compiler and isolated pdfLaTeX.
The [current layout audit](facct/paper/qa/2026-10-28/layout_report.json) records
the rendered content/endmatter boundaries; appendix sections now keep their own
tables and figures. The previous release is preserved for numerical comparison.
All 61 exclusive cases have
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
python -m facct.criterion_transfer.verify
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

This is an unpublished internal-review snapshot, not a submitted or accepted FAccT paper. On 27 October the author reported that the earlier related submission had been rejected for a submission mistake and was no longer under review. The active paper now presents the corpus, original annotation, audit and follow-up as stages of this study, without a companion-submission framing. This status update does not change historical data provenance or analysis chronology. Supporting source/recruitment records remain subject to author checks. Keep the repository private; check source rights, privacy and anonymity before wider release. No submission or chair contact was performed during this revision.
