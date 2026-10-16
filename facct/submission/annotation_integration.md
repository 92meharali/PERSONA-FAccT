# Assessment follow-up integrated into the paper

10 October 2026. Author-authorized update to the existing Overleaf manuscript.
No push, submission, chair contact, source-rating change or CHI revision.

## What changed

1. Abstract, contribution and RQ1 now distinguish original concern labels from
   new mental-health reviewworthiness judgments on the same responses.
2. Added methods for two full-corpus streams, a third assessor on 14 disagreements,
   0/1 versus 2/3 resolution, uncertainty, and author-reported independence.
   Manuscript R1/R2/R3 map to archive A/B/C, not original source Groups A/B.
3. Disclosed capability-note v1.0 versus v1.1 and the confounding of assessor with
   instruction version. No same-instruction or full-corpus three-rater reliability claim.
4. Added a generated main table and three appendix tables: assessor/target
   sensitivity, four budgets and legacy-criterion intersections. New numerical
   macros read verified outputs; output hashes are checked before typesetting.
5. Reported exact-corpus counts separately from hypothetical-batch uncertainty.
   Main paired intervals cross zero; point ordering is not general superiority.
6. Kept original normalized-marker/word-length queues. Imported alternative
   queues and repaired-text rankings remain separately labeled sensitivities.
7. Updated discussion, limitations, conclusion, ethics, AI-use and data statements.
   Trained-screen conclusions still concern original labels only. No new citations.
8. Updated current scope, claim ledger, disclosure, a separate current overlap matrix, readiness,
   professor brief, package checklist and README. Earlier computational-only
   records are explicitly historical rather than silently rewritten as prior plans.
9. Preserved the pre-integration manuscript and annotation manifest in
   `paper/history/pre-annotation-integration/`. Regeneration updates current hashes,
   not the statistical results or earlier source artifacts.

## Key evidence and allowed conclusion

- 660 responses; two full streams; 14 selective third assessments.
- Before resolution: 17 both positive, 629 both negative, 12 R1-only, 2 R2-only.
  Raw agreement 97.9%, kappa 0.698, positive agreement 70.8%. Negative prevalence
  dominates raw agreement; mixed note versions limit reliability interpretation.
- Resolution: 19 positives in 13 prompt clusters; none unresolved.
- Original 132-slot queue: HumT catches 6, markers 12, word length 4, expected
  random 3.8. Recall is 31.6%, 63.2%, 21.1%, 20.0%, respectively.
- HumT minus markers: -31.6 pp, exploratory paired 95% interval [-66.7, +4.3].
  HumT minus expected random: +11.6 pp, interval [-6.7, +30.0]. Each uses 2,000
  effective whole-prompt re-ranking draws, conditional on recorded labels.
- Markers capture more flags in both individual streams and all specified target
  sensitivities. These related targets are not independent replications.
- Fifteen new positives overlap broad D; four fall outside it. New contextual
  reviewworthiness is not simply a higher numerical D cutoff.

The follow-up provides new judgment evidence beyond reanalysis of original labels,
but not a new corpus, representative assessor sample, harm validation or evidence
that organizations use the proposed workflow. Sufficient publication distinctness
still requires author/venue assessment; the disclosure describes both reuse and additions.

## Author confirmations and deliberate gaps

The author answered yes to confirmation of assessor separation from the original
author/rater team and consent/institutional coverage before annotation. This was
explicitly restated to the author. Previously, C's independent blinded assessment
was also confirmed. These are author attestations, not independently inspected records.

The follow-up question requested backgrounds, compensation and the applicable
approval/amendment reference; the author replied "lets skip for now". Those details
remain missing. Supplied forms still show pending status. Do not infer specific
credentials, compensation or coverage from the original study, and do not amend
private forms or collection timestamps. The paper remains an internal-review draft
until the reporting record is reconciled. Practitioner interviews are still deferred.

## Reproduce

```bash
python -m facct.independent_annotation.run --source /absolute/path/to/independent_annotation_study
python -m facct.independent_annotation.verify
python -m facct.paper.build_overleaf
python -m pytest facct -q
```

The annotation stage takes about 8 seconds for 2,000 paired draws; the paper build
reads completed analyses rather than rerunning trained models. A separate repeat
directory permits byte-for-byte comparison of nine numerical outputs. See the
[integration verification record](annotation_integration_verification.md) for the
actual test/compile outcome, not this plan.
