# Repository cleanup: 26 October 2026

The author requested the latest professor revision on GitHub and removal of
superseded clutter. The repository remains private. The active paper is
`facct/paper/overleaf/main.tex`; the sole current release is
`facct/releases/PERSONA_FAccT_Overleaf_2026-10-26_professor.zip`.

## Removed from the current tracked tree

- `facct/releases/PERSONA_FAccT_Overleaf_2026-10-24_chat_audit.zip`
- `facct/capability/archive/main_capability_prospective_2026-10-23.tex`
- `facct/paper/history/pre-annotation-integration/main.tex`
- `facct/paper/history/pre-annotation-integration/manifest.json`

These files remain recoverable from Git revision
`a9d1800ca82e9e31d5e8b106250526c99e9a89f0`, without rewriting history.
Dated provenance notes may still name historical paths; they describe prior
states rather than current entry points. Current navigation has been updated.

## Preserved deliberately

Original annotations, processed datasets, rubric definitions, analytical outputs,
source hashes, amendment protocols, verification records and test code remain
unchanged. Inherited companion manuscripts and the supplement remain because
current source-integrity checks depend on them. They are not active FAccT drafts.
Future-study code and protocols remain clearly labeled prospective.

The initial migration manifest is a historical snapshot, not the current package
manifest. Its old verifier already reported revised manuscripts and previously
removed release copies before this cleanup. It was not rewritten to make history
appear unchanged. Use the current analysis verifier, tests, and package manifest.

Local compiler files, render images, extracted release copies and untracked
future-study preparation are excluded from Git. Private assessor records, the
case-coding review packet, credentials and environments remain excluded.
No data or unfavorable result was removed to improve the paper's claims.

## Checks

Verify the current tree with `python -m facct.analysis.verify_outputs` and
`python -m pytest facct -q`. The latest package is hash-checked against the active
source. Original manuscript compilation/layout checks remain valid because the
cleanup does not edit `main.tex`, its bibliography, figures or tables.

Post-cleanup results: all 135 tests passed in 4.14 seconds; the independent
analysis verifier checked 144 ranked operating points, unchanged source hashes,
and matching code/output hashes. `git diff --check` also passed. The old snapshot
verifier is not represented as a passing current-tree check.
