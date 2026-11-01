# Compiled paper consistency audit

Date: 26 October 2026. Read-only review of the uploaded 31-page PDF against
repository revision `ab20461`. No manuscript, bibliography, source ratings or
analysis outputs were edited. Reference verification is recorded separately in
[reference_audit_2026-10-26.md](reference_audit_2026-10-26.md).

## Findings requiring attention

### High: the recorded therapist-role system prompt is not disclosed in methods

PDF section 3.1, page 3; `facct/paper/overleaf/main.tex:62`.
Every one of the 660 records in each of the five mental-health source annotation
files contains a system prompt beginning "You are a professional therapist
providing mental health support online." It also instructs a single-turn response,
no further interaction, under 170 words, one or two paragraphs, and avoiding bullets.
The current manuscript reports source benchmarks and endpoint identifiers but not
this generation instruction. Because D explicitly concerns professional identity,
affect and relationship implications, the role assignment is relevant experimental
context, not incidental metadata. Report it as recorded source configuration
(not authenticated provider logs), include the template in supporting methods, and
scope conclusions to this prompted batch. Do not imply spontaneous anthropomorphism
under a neutral assistant configuration. This does not change the screening counts.

### Medium: original rationale provenance and attribution need clarification

The source files frequently repeat exact rationale text across all five annotators.
For example, education E reasons match on 404/415 items and D reasons on 393/415;
mental-health D reasons match on 353/660. The earlier source audit also records
this pattern. It does not prove fabrication, lack of independent scoring, or even
that the free-text rationales were collected independently: a shared template or
later standardization may explain it. Establish whether these are raw independently
written rationales or standardized explanations, and describe the distinction.
Do not treat repeated rationale fields as independent corroboration of label validity.
Equal aggregate unanimity and rationale-match rates alone do not mathematically
prove that one field is a deterministic function of the other.

One concrete attribution edge case is `PMH2-0006`: a what-would-you-say counseling
scenario receives a wholly quoted therapist response, mean D 4.2, and source notes
explicitly treating the quoted script as the AI's own answer rather than user-directed
speech. Four source raters assign 4 and one assigns 5. The assistant's draft case
inspection instead describes quoted role demonstration. This is not an established
label error: the generation system role and distinction between performed speech and
suggested speech matter. It requires author interpretation against the documented
attribution rule before claiming what the high-D exclusive cases semantically mean.
Keep the original ratings; do not silently relabel to improve a comparison.

### Medium: follow-up assessor reporting is incomplete

PDF section 3.4, pages 4-5; `facct/paper/overleaf/main.tex:89`.
The manuscript describes R1/R2/R3 independence, task, instruction versions and
resolution, but does not state their relevant backgrounds, recruitment approach
or participation/compensation arrangement. The original Group A/B description
does not supply these facts for the new assessors. Add a concise anonymized
description from actual records. This finding does not dispute author-confirmed
consent or institutional coverage and does not infer undocumented qualifications.

### Medium: AI-use disclosure lacks the underlying model/version

PDF page 15; `facct/paper/overleaf/main.tex:252`.
The statement names OpenAI Codex and gives substantial task detail, but does not
identify the underlying model/version or explain that exact historical snapshots
are unavailable. The [official author guide](https://facctconference.org/2027/authorguide.html)
asks for model version, nature of use, and human review/validation where applicable.
Use actual logs where available; otherwise state the recording limitation rather
than inventing a version. Author responsibility is not itself a record that every
claim has already been personally reviewed.

### Medium: the advertised follow-up verifier fails after manuscript revisions

`facct/independent_annotation/verify.py:28` checks the current manuscript against
the old protected-input hash. Running `python -m facct.independent_annotation.verify`
fails with `Protected input changed: facct/paper/overleaf/main.tex`. This is a real
reproducibility-command failure even though the 135-test suite passes. It is not
a changed-rating finding: all raw-return and analysis-output hashes match, and
independent calculations reconstruct the labels and all 112 original-policy cells.
Separate historical manuscript protection from immutable analytical inputs, retain
the historical hash record, and add a test of the complete documented verifier.
Do not silently rewrite the historical manifest or weaken source-data checks.

### Low: endmatter classification is avoidably ambiguous

PDF page 15; `facct/paper/overleaf/main.tex:254`.
The data/reproducibility paragraph is on the additional endmatter-only page.
The official list expressly includes ethics and AI-use statements, but does not
expressly list a general reproducibility-methods statement. Move the detailed
paragraph into an appendix (and essential methods into the main text as needed).
This is a precaution, not an assertion that the chairs have rejected its placement.
The main paper itself ends on page 14; references occupy 16-17 and appendices 18-31.

## Numerical checks completed

- The uploaded PDF and the locally verified PDF have identical multisets of
  extracted numbers after removing standalone page/line numbers. This is a
  consistency check, not a claim of byte identity or identical float placement.
- No unresolved `??` references or replacement-character artifacts were found
  in the uploaded PDF text extraction.
- Regenerated 24 table/macro files in a temporary directory. All numeric table
  bodies and macro mappings match the active manuscript assets.
- The independent original-output verifier checked 144 ranked operating points
  against scikit-learn reference metrics; source, code and output hashes match.
- Independently reconstructed follow-up majority resolution from the raw supplied
  assessor returns, and all 112 original-policy target/budget cells.
- Recomputed all 384 latest-amendment performance rows and 256 paired contrasts
  with 2,000 prompt-bootstrap draws per domain; point estimates and intervals match.
- `python -m pytest facct -q`: 135 tests passed in 5.05 seconds. This does not
  override the separate verifier failure above.

| Check | Independently confirmed |
|---|---|
| Corpus | 1,490 responses; 660/415/415 by domain |
| Prompt clusters | 499; 220/139/140 by domain |
| Incomplete sets | Education 138 triples + 1 singleton; health 136 triples + 3 pairs + 1 singleton |
| Broad D counts / supporting prompts | Mental health 165/99; education 12/7; health 23/15 |
| Mental-health broad D at 132 slots | HumT 42, full markers 63, prefix markers 68 |
| Mental-health strict D > 3 | 57 cases, 42 prompts; HumT 13, full markers 26, prefix markers 22 |
| Follow-up pre-resolution cells | Both positive 17, both negative 629, R1-only 12, R2-only 2 |
| Follow-up agreement | 97.8788%; kappa 0.697822; positive agreement 70.8333% |
| Follow-up resolved target | 19 cases; HumT 6, full markers 12, prefix markers 10 |
| All-three original-criterion intersections | Mental health 6, education 4, health 6 |

## Interpretation boundaries

The companion reference audit identified all 24 works in primary records and
corroborated all 17 supplied DOI mappings. No fabricated work or substantive
bibliographic mismatch was established. Reference [3] omits the accent in Mark
Diaz's surname (the primary record uses D\'iaz). CounselBench's exact OpenReview
forum destination could not be authenticated through the blocked endpoint, but
the work is independently verified in the official ICLR proceedings. Three
DOI-form URL redirects were not separately tested; their DOI mappings are verified.

No numerical contradiction was found in the checked headline counts, table
content, denominators or newly reproduced intervals. This does not independently
authenticate participant identities, historical scoring invocations, scientific
validity of the concern criteria, or absence of every possible error. The audit
does not turn unknown metadata into verified facts or pending semantic coding
into completed human evidence. The full trained refitted bootstrap was not rerun
in this audit; its stored tables, intervals and existing tests were checked.

Only audit notes were added. No manuscript/data edits or GitHub push were performed.
