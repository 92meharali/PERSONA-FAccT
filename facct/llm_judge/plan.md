# Semantic judge amendment

Prepared 24 October 2026 after review of existing results. This is exploratory
preparation on an already explored corpus, not a preregistration of unseen data.
The author requested runner preparation only; model, provider, transmission and
budget authorization remain to be confirmed. No provider calls or judge results
exist from this amendment. Capability experiments remain deferred.

## Scope

The default and focal task is contextual anthropomorphic reviewworthiness on all
660 existing mental-health responses. Compare the semantic queue with frozen
HumT at exactly 132 slots, and with markers, length and analytical random as
secondary comparisons. All four budgets remain visible. The human reference is
the existing resolved follow-up target, never the judge's categorical output.
The same assessor/version limitations remain; this is not new human validation.

Optional source_D, source_F and source_OA tasks cover all 1,490 responses each,
scored in separate requests to avoid cross-task answers influencing the judge.
These are separate, secondary comparisons with the existing source means. An
optional task must cover its entire declared batch, not selected favorable cases.
Preparing all four tasks entails 5,130 requests; default preparation entails 660.
Do not generalize a follow-up-only run to the transfer domains or all criteria.

## Blinding and text

Requests contain only a common instruction, one task/rubric, domain, full prompt
and response. No model identity, natural/adversarial label, scenario code, HumT,
human scores, annotator IDs, predicted answer, selected status or known counts
is supplied. Opaque request IDs remain outside model messages. Preserve original
corpus strings so primary comparisons use the same text as original fixed-policy
features. The source encoding differences are not silently repaired. Any later
repaired-text run is separately declared and re-evaluates lexical baselines too.

The follow-up prompt states the v1.1 experimental assumptions explicitly, without
claiming verified deployment capabilities. This is a fixed study-context screen,
not the proposed capability manipulation experiment. It excludes automatic
sympathy/pronoun flags. Source tasks instead use the released domain rubric;
source D remains the broad trigger. Keep those targets distinct.

## Freeze and inference

Select one version-pinned judge, settings and provider before scoring; confirm
data rights and the provider's retention terms before transmission. Do not choose
the best model after inspecting results. Record model changes as new exploratory
runs, including unfavorable ones. No examples from held-out labels are used for
prompt tuning. Review instructions on invented smoke-test cases only.

Priority is ordinal 0 to 3. Exact floor capacities and the original seed/hash
tie rule apply; scores are not probabilities. No top-quantile threshold selection.
The adapter must enforce the provider's output limit and return actual model,
response ID, usage, cost and raw output. There is no bundled live adapter yet:
provider-specific API integration follows model/budget approval and official API
documentation checks. No existing login token is reused as API authorization.

The run engine is sequential and append-only, with one attempt per request.
Failed/invalid/refused outputs are retained, priority 2 is the planned fallback,
and priorities 0 and 3 are sensitivity conditions. Failure counts and ties are
reported. No outcome-informed retry. A fatal adapter exception creates a failure
record and halts; restarting never repeats a recorded request. Interrupted calls
leave an in-flight marker and require manual billing reconciliation before resume.

A conservative per-request cost reservation must fit the remaining approved
budget before every call; an adapter must guarantee its declared ceiling through
token limits and verified pricing. The generic runner cannot independently prove
provider billing. Exceeding the declared ceiling halts the run and invalidates the
budget assurance. No prepaid balance or subscription access is assumed.

Analysis keeps all items, compares each policy on an identical full-domain queue,
and uses 2,000 paired domain-scoped prompt-cluster bootstrap replicates, re-ranking
each resampled batch. The focal contrast is judge minus HumT follow-up recall at
20%; all intervals are exploratory pointwise 95%. All nine original source cells
are secondary if collected. Do not combine full-batch queues with trained-fold
results: comparing the trained screen would require a separate matched-fold table.

Report counts, prevalence, precision, recall, misses, unselected concern rate,
AP/AUC, paired recall differences, failure sensitivity and tie-seed sensitivity.
Report zero-positive resamples and finite replicate counts, not substituted zeros.
Conditional finite-draw intervals are labeled when undefined draws occur. Human
label uncertainty and rater-population uncertainty are not resolved by bootstrap.

No model-generated score becomes a human label. No replacement annotation,
threshold search, favorable example selection, or original-result overwrite is
authorized. A null/negative result remains a result. A single judge is not evidence
about all semantic evaluators; zero-shot evaluation does not prove the model never
encountered the corpus in pretraining. Keep self-preference and possible source
model overlap in view when selecting and reporting the judge.
