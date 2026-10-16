# Already explored data

The entire existing corpus and the submitted CHI results were visible before this specification. All new corpus analyses are exploratory reuse.

Known prior exploration, supplied in the execution prompt and preceding discussion:
- Thresholds OA < 4, OA <= 3, D >= 3, F < 4, F <= 3.
- A different composite OA < 3 OR D > 2 OR F < 3. This is not interchangeable with the current criteria.
- High-H top-20% selection, AUC, precision-recall, criterion overlap, and model means/orderings.
- Pilot uncertainty with approximately 300 cluster resamples; early average-precision code was not independently validated for ties. Those values are not final results.
- Concern counts previously observed at OA < 4 / D >= 3 / F < 4: mental health 133/165/95, education 18/12/25, health 9/23/120. These are checks to reproduce, not assumptions enforced by data modification.
- CHI analyses: regression, grouped CV, ablation, reliability, correlations, distribution diagnostics and D-scope case audit.

The new final pipeline uses versioned rules, tested estimators and 2,000 paired cluster resamples. Recomputing does not restore confirmatory status. No previously explored model reversal is promised as a result. Unknown earlier exploration cannot be ruled out; authors should add dated notebooks or analysis records if available.
