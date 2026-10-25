# Response to Professor Junaid's feedback, 26 October 2026

## Revised pitch

The abstract and first paragraph now open with a team reviewing a mental-health
chatbot and the concrete 132-of-660 attention budget. HumT is introduced as a
published human-like-tone measure being evaluated for the new task of allocating
review. Its He/She-versus-It likelihood framing is explained plainly. Four
questions organize the introduction and results: enrichment, comparison with
inexpensive rules, incremental trained value, and distribution of coverage.
Four answers appear on page 2, led by mental health, with the criterion-dependence
message alongside them. Discussion places the screen inside a possible rules,
ranking and human-review process, supported by verified Facebook and Wikimedia
operational accounts. That two-stage process is prospective, not a tested result.

## Completed computational checks

All rows, original scores and original judgments are retained. The amendment has
its own specification, code, 2,000 paired prompt-bootstrap draws per domain,
immutable-source check, complete output tables, code/input hashes and manifest.
Original HumT, full-marker and length selected counts reproduce across all three
domains, three original criteria and four budgets. New tests distinguish D > 3
from D >= 4, exact character slicing, fixed capacity, deterministic ties,
analytical random expectation and undefined recall.

Mental health, 132 slots:

| Target | Concern cases / prompts | HumT | Full markers | 300-character markers | Random expected |
|---|---:|---:|---:|---:|---:|
| Mean D >= 3 | 165 / 99 | 42 | 63 | 68 | 33 |
| Mean D > 3 | 57 / 42 | 13 | 26 | 22 | 11.4 |
| Mean D >= 4 | 5 / 4 | 0 | 3 | 2 | 1 |
| Follow-up target | 19 / 13 | 6 | 12 | 10 | 3.8 |

- Broad D, H minus prefix markers: -15.8 percentage points, exploratory 95%
  interval [-23.4, -7.7]. Matching the available scorer's window does not remove
  the marker advantage for this target.
- D > 3, H minus full markers: -22.8 points [-38.9, -6.7]. The original full-text
  comparison is not explained solely by observations exactly at D = 3.
- D > 3, H minus prefix markers: -15.8 points [-31.4, 0.0]. This combined stricter
  comparison is less conclusive; it does not establish uniform robustness.
- Follow-up, H minus prefix markers: -21.1 points [-55.6, +3.6]. Point ordering
  persists but inference remains uncertain.
- Every domain and original target remains in the new appendix table, including
  results that favor HumT. All four budgets and both length versions are in CSVs.
- The published HumT window is 300 characters. Available scorer code follows
  that window but does not authenticate every historical input; transfer-domain
  exported/rated strings still differ. Code inspection also distinguishes the
  implementation's mean-loss contrast from a literal sequence-probability ratio.

Reproduce: `.venv/bin/python -m facct.professor_revision.run`, followed by
`.venv/bin/python -m facct.professor_revision.build_assets`. The final analysis
run took about 16 seconds in the existing local environment.

## Exclusive-case request

All 20 HumT-only and 41 marker-only broad-D cases were enumerated, with a complete
shuffled prompt-response packet and a separate policy/score key. Exact source-label
profiles are reported in the appendix:

| Characteristic | HumT-only / 20 | Marker-only / 41 |
|---|---:|---:|
| D exactly 3 | 14 | 22 |
| D above 3 | 6 | 19 |
| D at least 4 | 0 | 3 |
| Follow-up concern | 1 | 7 |

An assistant-generated descriptive coding draft covers all 61 full pairs, with
exact verified evidence spans and author-review columns. It distinguishes support,
therapeutic-role enactment and quoted role demonstrations, retaining ambiguity and
prompt context. It is not independent human coding, a new harm target, or a
validated semantic result. Its frequencies are not used in the paper. Authors
can verify the draft without arranging a new participant study; any later paper
claims about coding must accurately describe that review and AI assistance.

## Self-contained methods and companion check

Added PERSONA's profile definitions, prompt sources/adaptation, source-record
model identifiers, incomplete prompt-set structure, rating scale and group tasks,
and the D attribution/maximum-severity rule. Four source-dataset references are
copied from the existing bibliography and checked against primary records; two
operational-review references are new and primary-verified. Original references
are retained (24 cited references total).

The supplied submitted-PDF baseline has SHA256
`9c3d8cda415745d3709200ea445bc1f4b02ca0e4fea49b92a53dfad5e132a8aa`
and 20 pages, matching the original FAccT audit manifest. Its methods concern
OA prediction, grouped regression/CV and ablation. Full-PDF searches find no
20%, top-20, review-budget, screening, prioritization or capacity analysis; the
only 'recall' hit refers to a linguistic property. Inspection of its methods
and corresponding source supports that the top-20% screening analysis is new
to the FAccT work. This checks the supplied baseline, not a submission portal.

The introduction contrasts the two questions directly and the appendix retains
shared-data disclosure. Removed 'CHI results/analyses' wording from the manuscript
and the exact approval date while retaining the substantive ethics statement.

An earlier assistant message overstated the concurrent-submission rule. FAccT
prohibits identical or substantially similar submissions, not every distinct
paper by a team with another paper under review. Different analyses do not by
themselves establish distinctness; the comparison is substantive. No chair
permission is inferred or correspondence sent. Primary sources and the correction
are recorded in `professor_primary_sources_2026-10-26.md`.

## Review handoff

The revised paper and Overleaf package are prepared for Dr. Ibrahim and Dr. Wafa's
review before another round with Professor Junaid. The case-coding draft requires
author verification before any semantic coding results are promoted into the
paper. No email, registration or submission was performed by the assistant.

## Final verification

- `.venv/bin/pytest -q facct`: 135 tests passed in 5.05 seconds.
- `git diff --check`: passed.
- The existing manuscript compiled successfully with the desktop editor compiler.
- The independently rendered project has 14 content pages, one endmatter page,
  two reference pages and 14 appendix pages. All 31 pages were visually checked;
  enlarged checks covered the opening, new tables and content/endmatter boundary.
- The Overleaf archive contains 44 files and 24 cited references. Static package
  validation and frozen-asset checks passed. No private case packet is included.
- Archive SHA256:
  `4a1b7723db9f2c5ce729fa808965ca6af218feb34557abd1fe2d4202628f5815`.
- These checks establish computational and packaging consistency, not acceptance,
  submission eligibility or completion of author verification of the coding draft.
