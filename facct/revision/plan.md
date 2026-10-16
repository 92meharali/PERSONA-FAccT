# Review-response analysis amendment v1

Written 2 October 2026 after the original screening results and an AI-generated critique were examined, before executing these additions. These additions are exploratory, not preregistered, and do not replace the original three-domain D>=3, 20%-budget primary comparison family. Mental-health workload is not promoted to a new primary endpoint.

## Fixed additions

- Preserve frozen inputs, original analysis modules, protocol, and outputs. Write additions only under facct/revision/ and update the existing manuscript/package in place.
- Retain ordinary recall and add attainable oracle recall, achieved fraction of that upper bound, and precision/prevalence lift. The oracle is a reporting upper bound, not an implementable policy.
- Compare exact-budget high-H and marker selected sets at all four original budgets, with criterion-specific intersection, H-only, and marker-only counts. Their union is descriptive, not a same-capacity policy.
- Evaluate one label-free policy: equal-weight mean of within-batch midrank percentiles for H and markers. Use no outcome-dependent weights, thresholds, training, or model selection. Recompute ranks per resampled batch. This addresses additive information under one fixed rule, not all possible combinations or conditional independence.
- At 20% within each domain and each original criterion, use 2,000 paired prompt-cluster resamples for combined-minus-marker recall, H-minus-marker recall, and H-minus-random/length/marker workload at 80% recall. Report 95% pointwise exploratory percentile intervals and finite counts; sparse cells stay flagged.
- Do not add a supervised model or LLM judge in this amendment. These introduce label-acquisition or inference costs and are not needed to evaluate this fixed combination. Consider them in a separately recorded design only if the scientific question requires trained screening.
- Import all twelve existing reliability rows, explicitly labeling their source and response-level CI procedure; reconstruct ICC point estimates from current ratings. Report ordinal alpha alongside ICC, not selectively. Count item means within +/-0.2 of the three original cutoffs, the full distributions of means, five-rater trigger votes, unanimous binary agreement, and mean/majority disagreement. This neighborhood reflects one score-step by one of five raters, not an optimized band.
- Trace each education/general-health exported HumT row with the existing join implementation; verify H, source filename, and join tier against the released row. Compare byte-exact and normalized text identity and token features. Hash rather than publish text. An export string is evidence of association, not an authenticated historical scorer invocation.
- On the unchanged full batch, recompute length and marker features from matched export text as a representation sensitivity; do not recompute H or alter any rating. Separately report the full-text-join subset at original absolute capacity and at original budget fraction. Neither subset design isolates the causal effect of join error.
- Generate larger mental-health panels for the main paper and transfer panels for the appendix from the unchanged original screening output. Preserve every domain's results and uncertainty.

## Author-only decisions

No new human participation or AI-agent validation. Do not assume consequence-free non-participation for interns without source records. No chair contact, public upload, or submission. A distinct research question is a substantive distinction, but shared corpus/ratings/framing remain disclosed; neither automatic ineligibility nor automatic clearance is asserted.
