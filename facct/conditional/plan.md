# Conditional-lift amendment v2

Specified 2 October 2026 before running the trained comparisons, after the original results, first revision, and critique were examined. This is exploratory analysis on previously inspected data, not preregistration or an independent validation sample. Original primary tests, source annotations, original outputs, and revision-v1 outputs remain frozen.

## Question and estimand

Does adding recorded HumT improve concern recall at the same review capacity beyond marker fraction and response length in one fixed trained model class? Conditional lift means **absolute recall difference, extended minus reduced**, not a ratio, causal effect, conditional independence test, or proof of all possible incremental information. Original prevalence lift retains its separate meaning.

## Fixed specification

- Separate models for each domain and each original D>=3, F<4, OA<4 criterion. No pooled model and no outcome/metadata predictors. Labels remain the original five-rater-mean criteria.
- Reduced predictors: marker fraction and log(1 + regex word count). Extended adds recorded H. The fixed log transform limits length skew; no transform is chosen from outcomes. Both use StandardScaler fitted on training rows only and L2 logistic regression, C=1, lbfgs, intercept, no class weighting, max_iter=2000, tol=1e-8. No hyperparameter tuning, calibration, threshold search, or feature selection.
- Five folds per domain. Assign sorted unique prompt IDs by a deterministic seeded permutation to five nearly equal prompt-count chunks; every model response to a prompt stays together. Fold assignment is label-independent and shared across criteria and policies. Primary partition seed 20261002. Alternative partition seeds 20261003 through 20261012 are split sensitivity, not independent observations or a best-split search.
- Train on four folds, score the fifth. Evaluate each held-out fold as its own batch, not one pooled ranking of probabilities from different fitted models. Every policy in a batch receives floor(b*n_batch) slots, b in {0.05,0.10,0.20,0.30}. These smaller-batch quotas differ from the original full-domain quota; report actual achieved counts/fractions and never substitute original-batch baselines.
- Policies: descending H, descending length, descending markers, fixed equal-midrank H/marker fusion recomputed inside each held-out batch, reduced logistic, extended logistic, analytical uniform random. No LLM judge or new external labels.
- Aggregate caught cases, available concern cases, and selected slots across all five held-out batches before computing recall and precision. Do not average undefined per-fold recall or treat the five folds as independent replications. Record fold-level outcomes separately.
- Retain exact deterministic seed-based tie handling. Constant scores and zero-capacity batches are allowed. All policies get identical tie keys. Scores must be finite. If a training fold has only one outcome class, emit its constant prevalence score and flag the fallback; do not invent an estimable logistic fit. Fail on convergence errors rather than silently ignore them.

## Uncertainty and completeness

- At 20%, use 2,000 paired prompt-cluster bootstrap draws within the original five fold strata. Preserve each original prompt's fold, retain all sibling responses and all sampled copies, retrain both models and their scalers on each draw, and rerank each resampled held-out batch. A sampled original prompt can never occur in both training and test for the same fitted model.
- Use identical draws across criteria and all policies. Save replicate metrics and extended-minus-reduced differences. Report percentile 95% pointwise intervals, effective counts, and number of single-class fallback fits. These are approximate exploratory intervals conditional on the fixed original partition, empirical prompt distribution, and source labels; they are not universal confidence guarantees for CV or independent-sample inference.
- The 20% reference remains originally explored, not optimized. Other budgets and ten alternative partitions are descriptive sensitivity. Report all nine domain/criterion conditional-lift cells, all seven policies for D/F/OA, and sparse flags for fewer than ten positive or negative prompt clusters. No post-hoc selection of favorable domains or outcomes.
- Record train/test response and prompt counts, training positives/negatives, coefficients/scaler parameters, fold assignments, OOF predictions, and source/code/output hashes. Verify against sklearn metric implementations where applicable. Preserve zero-positive undefined recall and zero-slot undefined precision as missing.
- These are label-trained comparators, not equally label-free baselines. Per fitted model, count training response labels and their five underlying ratings; label reuse across folds is not five independent annotation purchases. Existing benchmark labels were available for retrospective fitting and evaluation, not newly collected. Deployment labeling time/cost and future effectiveness remain unmeasured.
- Report the original full-batch fixed-policy matrix separately from the held-out-batch trained matrix. Complete D/F/OA cells remain visible, including sparse, negative, and inconclusive estimates.

## Publication wording

Rewrite complementarity as an incremental-prediction question with descriptive selected-set overlap as supporting evidence. Preserve evidence that scores sometimes identify different cases, without equating this with added predictive value. Soften conclusions according to all nine results. Disclose reused CHI data, original prediction versus new allocation estimands, sequential exploration, substantial AI assistance, and actual model class/cost assumptions. No claim of submission eligibility, independent external validation, or publication acceptance. The author handles chairs.
