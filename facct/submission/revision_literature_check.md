# Targeted Literature and Policy Check

Verified 2026-10-02. Primary sources only; two selected studies, not an exhaustive novelty review. No chairs contacted and no eligibility approval established.

## Study Boundary

The local computational draft selects exactly `floor(n*b)` responses from each fixed batch using recorded HumT, length, or fixed lexical markers, with matched random controls. Existing D/F/OA ratings supply evaluation criteria; no predictor or deferral rule is fitted in this analysis. HumT itself is model-derived, so prefer **"no task-specific model fitting"** over "model-free." Non-selection means unreviewed, not an automated negative decision. The simulation measures opportunities to inspect criterion-labeled cases, not reviewer detection, correction, or harm reduction. [Local methods and scope](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/paper/generated/computational_review_draft.md:53)

## Two Selected Studies

### 1. Budget-Constrained Human/Machine Triage

**Nastaran Okati, Abir De, and Manuel Gomez-Rodriguez (2021), "Differentiable Learning Under Triage."** NeurIPS 34, 9140-9151. [Proceedings record](https://proceedings.neurips.cc/paper/2021/hash/4c4c937b67cc8d785cea1e42ccea185c-Abstract.html); [primary paper](https://proceedings.neurips.cc/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf).

**Verified support:** Section 2, equations (1)-(2), minimizes combined model/human prediction loss subject to an upper bound on the expected fraction assigned to humans. Sections 3-4 analyze triage and develop joint model/policy optimization; experiments include content moderation and scientific discovery. This directly motivates treating limited human capacity and allocation as explicit design variables, rather than judging a predictive model only under full automation. [Paper, pp. 2-4 and experiments](https://proceedings.neurips.cc/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf).

**Difference from our study:** Their objective is accurate predictions from a trained human-machine system, with human errors represented. Ours is criterion coverage in a review queue, without learning either component or measuring subsequent reviewer performance. Their expectation-level upper bound is not our exact per-batch quota. Their optimality results do not establish optimality of high-HumT ranking.

**Metadata note:** The official [BibTeX export](https://proceedings.neurips.cc/paper_files/paper/12322-/bibtex) lists the third author as `Rodriguez, Manuel`; the paper's title page prints `Manuel Gomez-Rodriguez`. Below uses that complete paper byline, with publication fields verified against the export. This normalization is explicit, not a verbatim export; optional editor fields are omitted.

```bibtex
@inproceedings{okati2021triage,
  author = {Okati, Nastaran and De, Abir and Gomez-Rodriguez, Manuel},
  title = {Differentiable Learning Under Triage},
  booktitle = {Advances in Neural Information Processing Systems},
  volume = {34},
  pages = {9140--9151},
  year = {2021},
  publisher = {Curran Associates, Inc.},
  url = {https://proceedings.neurips.cc/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf}
}
```

### 2. Learning When to Defer to an Expert

**Hussein Mozannar and David Sontag (2020), "Consistent Estimators for Learning to Defer to an Expert."** ICML, PMLR 119, 7076-7087. Full author list and publication fields verified against the [publisher record and BibTeX](https://proceedings.mlr.press/v119/mozannar20b.html); [published paper](https://proceedings.mlr.press/v119/mozannar20b/mozannar20b.pdf).

**Verified support:** The study learns a classifier and rejector using examples of expert decisions, formulates combined system loss, and supplies a consistent surrogate through cost-sensitive learning. It provides experimental evaluations rather than merely proposing a workflow. This motivates evaluating routing relative to the decision objective and expert behavior, not interpreting a score as intrinsically sufficient for allocation. [Publisher abstract](https://proceedings.mlr.press/v119/mozannar20b.html); [author manuscript v3, Sections 3-6](https://arxiv.org/html/2006.01862v3).

**Difference from our study:** A non-deferred case receives a model prediction; ours remains unreviewed. Their learned routing accounts for expert decisions and predictive loss; our fixed observable rankings are assessed against previously collected rubric labels. We neither implement their estimator nor test its consistency or human-machine accuracy claims. The accessible author manuscript is a January 2021 revision, not silently treated as the unchanged ICML proceedings version; no revision-specific numerical result is used here.

```bibtex
@inproceedings{mozannar2020defer,
  author = {Mozannar, Hussein and Sontag, David},
  title = {Consistent Estimators for Learning to Defer to an Expert},
  booktitle = {Proceedings of the 37th International Conference on Machine Learning},
  series = {Proceedings of Machine Learning Research},
  volume = {119},
  pages = {7076--7087},
  year = {2020},
  publisher = {PMLR},
  url = {https://proceedings.mlr.press/v119/mozannar20b.html}
}
```

## Manuscript-Ready Wording

> Prior work treats allocation between models and human experts as a decision problem: Okati et al. optimize prediction and triage under a limit on human involvement, while Mozannar and Sontag learn when a classifier should defer to an expert. We study a different, narrower setting: retrospective screening of a fixed response batch using existing scores and exact review quotas, without task-specific model fitting. Our outcome is coverage of separately defined rubric-based concern labels, not combined human-machine prediction accuracy. Cases outside the queue remain unreviewed, not cleared.

Use citation keys `okati2021triage` and `mozannar2020defer` for the first sentence; the remaining sentences describe the local design. [Okati et al.](https://proceedings.neurips.cc/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf); [Mozannar and Sontag](https://proceedings.mlr.press/v119/mozannar20b.html).

Neither study documents HumT adoption or validates these concern thresholds. They motivate allocation research, not the claim that organizations already use HumT for safety screening. No active-learning/annotation-allocation claim is needed: this simulation acquires no new labels and retrains no model.

## Current Venue Policies

**FAccT 2027:** Its concurrent/dual-submission rule excludes identical or substantially similar papers under review, accepted, or published elsewhere. It supplies no numerical overlap threshold. Full-paper deadline: **November 3, 2026**; abstract: **October 27**, both AoE. [Official CFP, Key Dates and Concurrent/Dual Submission Policy](https://facctconference.org/2027/cfp.html).

**CHI 2027:** The submission must be original and not simultaneously under review elsewhere. Concurrent papers sharing a study, artifact, or dataset must be provided anonymously in the concurrent-submissions field; omission can cause desk rejection. Ordinary reviews arrive **November 5, 2026**, after FAccT's full deadline; final notification is December 17. [Official Papers page, Important Dates and Step 1](https://chi2027.acm.org/authors/papers/).

**Distinct question versus reused corpus:** Our change from OA prediction to exact-budget allocation is a substantive methodological distinction, not a policy exemption. All 1,490 responses and ratings are reused, and the governance motivation partly overlaps. Same-corpus reuse triggers CHI's related-paper disclosure; it neither automatically proves nor disproves substantial similarity. New metrics do not establish independent publishability. This is an assessment, not a venue determination. [Local comparison](/Users/meharali/Documents/Codex/2026-08-10/ok/work/persona-facct-review/facct/submission/distinctness_assessment.md); [FAccT rule](https://facctconference.org/2027/cfp.html); [CHI disclosure rule](https://chi2027.acm.org/authors/papers/).

**No abstract/non-archival workaround:** FAccT's FAQ permits abstract registration when another conference's notification falls between its abstract and full deadlines, but requires withdrawal if that paper is accepted or remains under review beyond the full deadline. CHI's ordinary November 5 date does not fit that scenario. The non-archival journal exception does not cover a concurrent CHI conference paper; the FAQ rejects non-archival submission as a route to another archival conference. [Official Author Guide, Concurrent and Dual Submission Policy and FAQ](https://facctconference.org/2027/authorguide.html).

### Published Disclosure Route, Not Approval

- **CHI's specified route:** anonymized related manuscript in the concurrent-submissions field. Its September 10 deadline has passed; the public Papers page does not specify how to add a newly arising related paper afterward. The author should ask `papers@chi2027.acm.org` for the permitted update procedure, not assume a rebuttal disclosure suffices. [Official instructions and contact](https://chi2027.acm.org/authors/papers/).
- **FAccT routing:** the public guide does not identify a dedicated related-manuscript upload field. The author should obtain routing guidance from `program-chairs@facctconference.org`, with both manuscripts and an accurate account of shared data, ratings, analyses, and claims ready for the channel they specify. [Author Guide](https://facctconference.org/2027/authorguide.html); [official contact](https://facctconference.org/2027/cfp.html).
- **Unresolved:** neither disclosure nor a distinct RQ establishes permission. No chair-approved route for this post-deadline case, exception, or approval has been verified. The author handles all correspondence; this check sends nothing. If similarity/status remains unresolved at the full deadline, do not treat silence as clearance. Even after concurrent review ends, accepted/published-work overlap remains relevant.

Verification limit: the linked [ACM simultaneous-submission policy](https://www.acm.org/publications/policies/simultaneous-submissions) could not be retrieved in this check; no unseen ACM exception is asserted. Venue conclusions above use directly inspected official 2027 pages. Recheck before submission.
