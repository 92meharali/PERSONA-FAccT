# Integration and evidence review, 28 October 2026

## Requested outcome

Develop the connecting criterion-to-decision idea, assess it honestly, revise the
paper again where needed and deliver a fresh portable Overleaf ZIP. No new
participants, scores, semantic-judge calls, private records, or source-rating
changes are part of this work. No commit, push or submission is implied.

## What changed

1. Added `facct/criterion_transfer/` with a dated exploratory specification,
   reusable selection/measurement code, runner, tests and independent verifier.
2. Crossed D/F/OA training targets with all original evaluation targets. Added
   contextual reviewworthiness as an evaluation-only mental-health endpoint.
   Original feature sets, five prompt folds, C=1 logistic model and preprocessing
   are held fixed. No target is selected using follow-up results.
3. Ran 2,000 paired within-fold prompt-bootstrap refits per domain and ten
   alternative partitions. Four capacities are retained, with reference-fraction
   uncertainty only. Reconstructed every previous diagonal prediction and CI.
4. Integrated the old OA-prediction diagnostic as motivation, not independent
   framework validation. Human-rating predictors are explicitly distinguished
   from cheap test-time text features.
5. Revised title, abstract, four questions, contribution, methods, results,
   discussion, limitations and reproducibility narrative in the existing source.
6. Generated seven new tables, retained every domain/criterion cell, and added two
   primary references with verified title/author/year/DOI records. Obermeyer et
   al. is a direct target-choice allocation precedent; the matrix is not claimed
   as a newly invented algorithm. The literature memo records the positioning.
7. Reduced repetition and moved duplicate original-result tables to the appendix
   to retain the unchanged ACM formatting and a self-contained main paper.
8. Updated active repository pointers, scope/readiness records, claim ledger and
   portable package instructions. Earlier releases and historical evidence remain.

## Results and interpretation gate

At 130 held-out mental-health slots, lexical screens trained on D/F/OA capture:

| Training target | Broad D / 165 | Fit / 95 | OA / 133 | Reviewworthy / 19 |
|---|---:|---:|---:|---:|
| D | 70 | 19 | 25 | 11 |
| Fit | 53 | 32 | 34 | 9 |
| OA | 62 | 26 | 26 | 11 |

Fit/OA queues share 107/130 MH selections, 52/80 education selections and 59/80
general-health selections. Yet all ten fit-minus-OA paired recall intervals
include zero, both with and without H. MH reviewworthiness difference is -10.5
percentage points, 95% interval [-20.0,+18.2]. Alternative partitions give
[-10.5,+5.3] as the range of point differences, not a confidence interval.

Only two of 30 lexical training-target-pair comparisons have pointwise intervals
excluding zero: MH D-trained minus fit-trained on D (+10.3 pp [+.5,+20.9]), and
education D-trained minus OA-trained on fit (-52.0 pp [-73.0,-8.7]). These are
exploratory, not multiplicity-controlled discoveries. The full table retains the
other comparisons, different prevalences and sparse targets. General-health
counts are similar across several targets; no general transfer-failure claim.

**Decision after inspecting results:** retain the integrated measurement-use
audit, but reject the stronger interpretation that the new analysis proves
PERSONA's constructs distinct, determines a superior target, or resolves the
earlier validation criticisms. This is a better-connected empirical argument,
not evidence that the paper has become a high-confidence acceptance. The original
tone comparisons and their primary-family status remain intact.

The repeated run did not change its results. Independent reconstruction checks
240 operating points, 60 reference-budget paired intervals and 72 queue-pair
overlaps against original predictions, source labels and saved refit arrays.
All existing source/prior-output hashes are preserved. The final manifest records
175.69 seconds for the 2,000-refit run on this machine (approximately three minutes).

## Reproduce

From the repository root, using the existing pinned virtual environment:

```bash
.venv/bin/python -m facct.criterion_transfer.run
```

Then verify and regenerate the manuscript tables:

```bash
.venv/bin/python -m facct.criterion_transfer.verify
.venv/bin/python -m facct.criterion_transfer.build_assets
.venv/bin/pytest facct -q
```

The runner needs the original follow-up immutable frame at the source path in its
existing manifest; it verifies that hash and joins by response ID, not CSV order.
Consent/recruitment forms are not read or packaged. The Overleaf ZIP compiles
without any of these data files or external network access. It is a typesetting
package, not a full anonymous data artifact.

## Formatting and delivery

Title: **When Scores Allocate Attention: Auditing Criteria and Tone in AI Review**.
The current pdfLaTeX layout is 14 content + 1 endmatter + 2 references + 23 appendix
pages (40 total), with unchanged ACM class/fonts/margins. The 14-page limit applies
to content, not the entire PDF. Detailed hashes and visual-audit status are in
`facct/paper/qa/2026-10-28/layout_report.json`. The release is
`facct/releases/PERSONA_FAccT_Overleaf_2026-10-28_integrated.zip`.

## Completion audit

| Requirement | Inspected evidence | Outcome |
|---|---|---|
| Implement the connecting analysis, not just reword the paper | New runner, complete matrices, refit arrays, split sensitivity and source-hash manifest | Completed; 2,000 draws per domain |
| Iterate after assessing the results | Full matrix and paired contrasts; interpretation gate above; revised abstract/results/discussion | Strong superiority/validation interpretation rejected; bounded claim retained |
| Preserve data and previous findings | Immutable source/prior-output hashes and original diagonal reconstruction | Unchanged |
| Independently verify new calculations | `criterion_transfer/outputs/verification.json` | 240 operating points, 60 paired intervals and 72 queue-pair overlaps checked |
| Verify earlier screening evidence | `python -m facct.analysis.verify_outputs` | 144 ranked operating points checked against scikit-learn; hashes pass |
| Run regression tests | `.venv/bin/pytest facct -q` | 146 passed |
| Check citations and anonymous source | `build_overleaf.validate()` and compiled log | 26 cited keys resolve; no duplicate labels/private identifiers; no undefined refs or overfull boxes |
| Compile current saved document | Desktop compiler success and isolated pdfLaTeX | Passed |
| Check venue length and visual layout | Matching-source layout report; all 40 pages viewed as contact sheets, pages 8/31 enlarged | 14 content + 1 endmatter + 2 references + 23 appendix pages |
| Deliver a new portable archive | ZIP integrity and byte comparison of all 51 entries with current project | Passed; 550,536 bytes |

Archive SHA-256:
`22599b6948f7db3e10eb683cb7eceba5e457657c8745ab9b91a90d7b8c72fbcb`.
No GitHub push, submission, participant collection or paid API call was performed.

## Remaining author checks, not manufactured completion

- Review the revised argument, quotations, methods and bibliography before use.
- Match recruitment/consent/compensation/ethics language to the retained records;
  documentation is not inferred from anonymity or from code verification.
- Confirm actual submission registration, source redistribution rights, anonymous
  supplemental access, and the precise AI model versions used where available.
- Semantic comparison, authenticated historical HumT scorer calls, independent
  dimension replication and practitioner workflow outcomes remain absent.

The supplied desk-rejection letter describes substantive methodological concerns;
the earlier explanation that it was merely a submission mistake is superseded in
internal records. The manuscript need not discuss rejection history, but continues
to report who supplied the original ratings and what the evidence can establish.
