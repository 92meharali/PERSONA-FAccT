# Submitted PDF checks

Local supplied PDF only; not a verified portal download.

Page 1: by automated human-likeness (𝐻) and three context-aware judgments: empathic appropriateness (𝐸), deception risk (𝐷), and domain fit (𝐹). Across 1,490 responses spanning mental health, education, and general health, grouped repeated cross-validation showed that 𝐻 alone weakly and inconsistently predicted overall appropriateness (𝑂𝐴), rated by separate domain-relevant pools. The full profile explained more 𝑂𝐴variation in mental health (𝑅2 =.659) and education (𝑅2 =.562), where 𝐹 carried most signal and 𝐻 added at most

Page 1: 𝐻 alone weakly and inconsistently predicted overall appropriateness (𝑂𝐴), rated by separate domain-relevant pools. The full profile explained more 𝑂𝐴variation in mental health (𝑅2 =.659) and education (𝑅2 =.562), where 𝐹 carried most signal and 𝐻 added at most .003 beyond 𝐸, 𝐷, and 𝐹. In ceiling-restricted general health, the D-only model had the strongest single-dimension point estimate (𝑅2 =.241), but its interval crossed zero, the full-profile gain was uncertain, and sensitivity checks showed dependence on sparse

Page 2: author involvement in dimension rating introduces expectancy risk that we address in Section 8. We evaluate PERSONA on a corpus of 1,490 AI responses spanning three high-stakes domains: mental health (𝑛= 660), education (𝑛= 415), and general health (𝑛= 415). Mental-health prompts were drawn from CounselBench [22], while education and general-health scenarios were developed around interactive tutoring and health-assistance

Page 3: profile–𝑂𝐴relationships are empirical rather than arithmetic. • An annotated multi-domain corpus and protocol: 1,490 responses across mental health, education, and general health, each with five holistic ratings and five ratings per diagnostic dimension. • Evidence on what carries the signal: in mental health and education, domain-fit judgments recovered nearly all

Page 6: General health 415 140 2,075 2,075 415/415 Pooled 1,490 499 7,450 7,450 1,490/1,490 The empirical question is therefore how much the association varies by domain and whether the remaining profile dimensions contribute information beyond𝐹.

Page 6: 4.1 Dataset Construction and Provenance The final analytical dataset contains 1,490 responses: 660 mental-health responses, 415 education responses, and 415 general-health responses (Table 1). The corresponding prompt clusters are 220, 139, and 140, giving 499 prompt clusters overall. HumT is available for all responses in the final analytical dataset.

Page 7: Grouped analyses retain these clusters intact. The final analytical corpus contains no incomplete annotation rows and has HumT coverage for all 1,490 responses. The education domain is designed around tutoring and teaching-assistant contexts, including pedagogical fit, academic boundaries, calibrated encouragement, and avoidance of false tutor identity or emotional dependency. The

Page 7: claude-opus-4.8 and z-ai/glm-5.2 through the OpenRouter Chat Completions API. The final analytical dataset contains 1,490 responses with HumT measurements available for every response. Model identity was hidden from annotators. 4.3 Rater Populations and Separation

Page 7: medical training evaluated the 415 general-health responses. Group B comprised five members of the author team and research interns; each evaluated all 1,490 responses on𝐸,𝐷, and𝐹. No person served in more than one pool. Group B participated in rubric development and was therefore not blinded to the study’s conceptual aims. Before annotation, these raters jointly reviewed and agreed upon the construct definitions, anchor examples, attribution rules,

Page 8: ethics review board; identifying approval and funding details are withheld during anonymous review. Annotators provided informed consent, and compensation was provided through their existing paid research roles rather than through a separate per-response payment scheme. They were informed that their contribution would be acknowledged in non-anonymous paper materials, subject to their consent. Participation was self-paced over a two-week annotation

Page 9: intercept. Predictors enter on their recorded scales; the pooled analysis additionally includes domain indicators. We apply no regularization, imputation, feature selection, hyperparameter tuning, or outcome transformation. All 1,490 evaluated responses are complete for the variables used. We use grouped 5-fold cross-validation repeated 20 times, grouping by prompt identifier so responses to the same

Page 10: interval excluding zero. Second, in mental health and education, domain fit alone recovered almost all of the signal captured by the full profile (.651 vs. .659; .562 vs. .562), and adding 𝐻 to 𝐸+𝐷+𝐹 changed the 𝑅2 point estimate by at most .003, with every interval including zero. Because HumT varies little in two domains and 𝐹 and 𝑂𝐴are not shown to be discriminant, we read this as evidence about this measure of human-likeness and these domain-fit judgments

Page 10: to be discriminant, we read this as evidence about this measure of human-likeness and these domain-fit judgments rather than as a general claim about human-like style. Third, general health differed: with 63.86% of 𝑂𝐴scores at the maximum, deception risk had the highest single-dimension point estimate (𝑅2 =.241), but its interval crossed zero and sensitivity checks showed dependence on few observations, so we treat it as exploratory. Reliability, distributional

Page 11: Domain Baseline𝑅 2 Full𝑅2 Gain 95% CI Mental health (𝐻) .026 .659 .632 [.567, .686] Education (𝐻) .099 .562 .462 [.278, .598] General health (𝐻)−.007 .256 .264 [−.053, .400]

Page 11: Domain𝐻 𝐸 𝐷 𝐹 𝐸+𝐷+𝐹Full (𝐻+𝐸+𝐷+𝐹) Mental health .026 .012 .035.651.658.659 [−.005, .055] [−.009, .031] [.000, .065] [.583, .704] [.596, .711] [.596, .711] Education .099−.020 .001.562.559.562

Page 11: The informationally richer profile captures substantially more 𝑂𝐴-associated variation than 𝐻 alone in mental health and education. In mental health, the full model achieves 𝑅2 =.659, a gain of .632 over the 𝐻-only baseline. In education, the full model achieves 𝑅2 =.562, a gain of .462. The pooled gain is .278. Table 4 summarizes the grouped repeated cross-validated comparison. In general health, the full-profile point estimate is positive (𝑅2 =.256), but the gain interval

Page 11: and sensitivity results, this supports only an exploratory interpretation. The in-sample domain-interaction OLS model fitted to 1,490 responses yielded 𝑅2 =.651and adjusted 𝑅2 =.648; its covariance matrix clusters standard errors across 499 prompt groups. This value is distinct from the cross-validated results above. Table 6 reports the reference-domain main effects and all eight interaction terms.

Page 14: 𝐻.031 .023−.037 .094 — — 𝑂𝐴4.852 .402 1.8 5.0 0.00% 63.86% 𝐸2.516 .888 1.2 5.0 0.00% 1.69% 𝐷1.286 .636 1.0 5.0 49.40% .48%

Page 14: (SD =.022) and general health (SD =.023), while education has a wider range driven by a small upper tail. General health also shows a strong 𝑂𝐴ceiling (63.86%) and a substantial 𝐷 floor concentration (49.40%); education has a still stronger 𝐷 floor (87.23%). These constraints limit detectable relationships and qualify the domain-level interpretations. 6.6.1 Predictor Collinearity Diagnostics.Maximum variance inflation factors are 1.345 in mental health, 1.393 in

Page 17: The present evidence is strongest in mental health and education. General health provides exploratory cross-domain evidence, although inference is limited by substantial ceiling restriction in 𝑂𝐴(63.86% at the maximum), concentration of non-minimum 𝐷 values in relatively few observations, and the confidence interval for the incremental gain over 𝐻 alone crossing zero. Education also contains a strong𝐷floor effect, with 87.23% of observations at the minimum.

Page 18: told us little about the second. Across 1,490 responses, human-likeness alone was a weak and domain-dependent predictor of overall appropriateness. The full profile showed substantial added predictive performance over the𝐻-only baseline in mental health and education. Domain fit accounted for most of the available predictive signal in those domains. In general health, the D-only model