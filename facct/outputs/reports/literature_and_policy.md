# PERSONA: Primary-Source Literature and Submission-Policy Verification

Verification date: **2 October 2026**. Scope: the proposed FAccT study of allocating human review using a human-like-tone score. This is a targeted source-verification memo, not a systematic review, a computation/provenance audit, or publication-policy clearance.

The sibling notes `persona-ethics-repo/docs/FACTT_DIRECTION_VALIDATION.md` and `FACTT_2027_SUBMISSION_RESEARCH.md` were read as leads. Their interpretations, dataset claims, exploratory numbers, and assessments of the submitted CHI manuscript are not independently established by this memo. No local analyses were run, manuscript comparison performed, submission made, or chairs contacted.

## 1. Bottom Line

**The defensible object is a proposed review-allocation policy, not a purported existing organizational practice.** No primary source verified in this review documents an organization deploying HumT to prioritize safety reviews, approve releases, or allocate audit resources. This is a bounded negative finding, not proof that no organization does so. The author's [HumT/DumT repository](https://github.com/myracheng/humtdumt) documents scoring and fine-tuning, not an operational review program.

**Proposed question, not an established result:** If a specified reviewer can inspect only a fixed share of responses, which independently defined concern labels would a HumT-based allocation rule surface or leave unreviewed, compared with feasible alternatives? Does that answer change with domain, review budget, and the chosen concern definition?

The literature below motivates that question but does not answer it for PERSONA. The study should be described as an **offline evaluation of a proposed tone-score review-allocation rule** unless additional workflow evidence warrants stronger language. A positive result would not, by itself, demonstrate improved organizational accountability or reduced user harm. A negative result would not, by itself, invalidate HumT as a tone measure.

## 2. Verified Bibliography and Support Limits

Bibliographic metadata were checked against ACL records, conference-hosted papers, author-deposited manuscripts, and ACM's publisher-deposited Crossref records. Crossref verifies publication identity and pagination, not empirical claims. Several ACM/DOI landing-page requests returned access errors; the primary full texts actually inspected are linked below. Author manuscripts are identified as such rather than silently represented as publisher PDFs.

### L1. HumT DumT

**Myra Cheng, Sunny Yu, and Dan Jurafsky. 2025. _HumT DumT: Measuring and controlling human-like language in LLMs._** Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers, 25983-26008. DOI: [10.18653/v1/2025.acl-long.1261](https://doi.org/10.18653/v1/2025.acl-long.1261). [ACL record](https://aclanthology.org/2025.acl-long.1261/); [published paper](https://aclanthology.org/2025.acl-long.1261.pdf); [author manuscript v2](https://arxiv.org/html/2502.13259v2).

**Supports:** Sections 3.1 and 3.3 operationalize tone through relative language-model probabilities and report sign/ranking validation against human annotations from four project-familiar students. Sections 4-5 examine preferences, HumT-SocioT correlations, and DumT steering with benchmark/preference evaluation. Sections 6-7 call for downstream studies and delimit linguistic, English-language, and contextual coverage.

**Limits:** Risk mitigation is part of the paper's motivation and interpretation, not merely an external reading. Nevertheless, associations with measured social dimensions and reduced tone do not establish reduced dependence, deception, or organizational screening effectiveness. HumT is not introduced as a calibrated harm probability. Prefer "evidence supporting tone measurement in the studied settings" to an unqualified declaration that the metric is valid everywhere.

### L2. Dehumanizing Machines

**Myra Cheng, Su Lin Blodgett, Alicia DeVrio, Lisa Egede, and Alexandra Olteanu. 2025. _Dehumanizing Machines: Mitigating Anthropomorphic Behaviors in Text Generation Systems._** ACL 2025, Volume 1: Long Papers, 25923-25948. DOI: [10.18653/v1/2025.acl-long.1259](https://doi.org/10.18653/v1/2025.acl-long.1259). [ACL record](https://aclanthology.org/2025.acl-long.1259/); [published paper](https://aclanthology.org/2025.acl-long.1259.pdf).

**Supports:** An intervention inventory informed by literature and a crowdsourced rewriting study. Section 4 explicitly discusses context-dependent interventions, contradictory-looking edits, and ways an intervention might fail or worsen outcomes. Limitations distinguish consciously identified human-like features from effects outside participants' awareness.

**Limits:** This is not a demonstration that removing every anthropomorphic expression improves safety, nor a trial of HumT-prioritized review. The paper already recognizes contextual intervention tradeoffs. PERSONA cannot claim novelty merely for observing that de-anthropomorphizing can be inappropriate. Its US/English participant scope also limits generalization.

### L3. DeVrio Taxonomy

**Alicia DeVrio, Myra Cheng, Lisa Egede, Alexandra Olteanu, and Su Lin Blodgett. 2025. _A Taxonomy of Linguistic Expressions That Contribute To Anthropomorphism of Language Technologies._** Proceedings of the 2025 CHI Conference on Human Factors in Computing Systems, 1-18. DOI: [10.1145/3706598.3714038](https://doi.org/10.1145/3706598.3714038). [Author record with publication DOI](https://arxiv.org/abs/2502.09870); [author full text v1](https://arxiv.org/html/2502.09870v1); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3706598.3714038).

**Supports:** A literature- and case-informed taxonomy, including five interpretive lenses: internal states, social positioning, materiality, autonomy, and communication skills. Section 4 treats categories as overlapping and perception-dependent; the discussion warns against dehumanizing people through rigid notions of humanness.

**Limits:** It is not a validated numerical risk scale or a performance test of review allocation. It is close prior art for multidimensional anthropomorphic-expression analysis and can inform qualitative error coding. Any mapping from its expressions to PERSONA dimensions would be a new analytical choice requiring justification, not an established equivalence.

### L4. Measurement and Fairness

**Abigail Z. Jacobs and Hanna Wallach. 2021. _Measurement and Fairness._** Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, 375-385. DOI: [10.1145/3442188.3445901](https://doi.org/10.1145/3442188.3445901). [Author full text](https://arxiv.org/pdf/1912.05511); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3442188.3445901).

**Supports:** Measurement modeling makes explicit the assumptions linking constructs and observable operationalizations. Section 3.2.7 includes consequences of measurement use within the authors' account of construct validity; Section 4 addresses normative disagreement over fairness itself.

**Limits:** This is conceptual grounding, not empirical evidence about HumT. The memo's separation of measurement, association, and use below is an analytical aid, not a claim that this paper treats consequential validity as wholly separate from construct validity. PERSONA's human labels also need validity arguments; calling them ground truth does not supply one.

### L5. Evaluation Gaps

**Ben Hutchinson, Negar Rostamzadeh, Christina Greer, Katherine Heller, and Vinodkumar Prabhakaran. 2022. _Evaluation Gaps in Machine Learning Practice._** 2022 ACM Conference on Fairness, Accountability, and Transparency, 1859-1876. DOI: [10.1145/3531146.3533233](https://doi.org/10.1145/3531146.3533233). [Conference-hosted full text](https://facctconference.org/static/pdfs_2022/facct22-3533233.pdf); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3531146.3533233).

**Supports:** An empirical examination of 200 NLP/CV research papers and a distinction between learner-centric and application-centric evaluation. Section 2 specifically discusses scores becoming decisions through thresholds and the relevance of consequential validity to accountability.

**Limits:** Its observed practices are from the sampled research literature, not an investigation of HumT deployment. Context-sensitive evaluation and the score-to-decision distinction are already established motivations. PERSONA must contribute evidence about its specified allocation rule rather than present these general distinctions as new findings.

### L6. Closing the AI Accountability Gap

**Inioluwa Deborah Raji, Andrew Smart, Rebecca N. White, Margaret Mitchell, Timnit Gebru, Ben Hutchinson, Jamila Smith-Loud, Daniel Theron, and Parker Barnes. 2020. _Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing._** Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency (FAT* '20), 33-44. DOI: [10.1145/3351095.3372873](https://doi.org/10.1145/3351095.3372873). [Author record](https://arxiv.org/abs/2001.00973); [author full text](https://arxiv.org/pdf/2001.00973); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3351095.3372873).

**Supports:** SMACTR organizes internal auditing through scoping, mapping, artifact collection, testing, and reflection, with documentation across the development lifecycle. Section 4 explicitly illustrates the framework with a fictional company and hypothetical projects.

**Limits:** Do not turn those illustrations into observed organizational deployments. The framework does not establish that a single offline score evaluation closes an accountability gap, and it predates HumT. Its contribution helps delimit what a broader organizational audit would require beyond PERSONA's proposed allocation analysis.

### L7. Assurance Audits

**Khoa Lam, Benjamin Lange, Borhane Blili-Hamelin, Jovana Davidovic, Shea Brown, and Ali Hasan. 2024. _A Framework for Assurance Audits of Algorithmic Systems._** The 2024 ACM Conference on Fairness, Accountability, and Transparency, 1078-1092. DOI: [10.1145/3630106.3658957](https://doi.org/10.1145/3630106.3658957). [Author record](https://arxiv.org/abs/2401.14908); [author full text v2](https://arxiv.org/html/2401.14908v2); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3630106.3658957).

**Supports:** The criterion-audit framework specifies normative criteria, scoped assurance/compliance objectives, qualified auditors, verification, and reporting. It distinguishes direct assessment from indirect verification and illustrates criteria for NYC hiring-algorithm bias audits. The authors report practitioner experience informing the discussion.

**Limits:** Practitioner experience with those audits is not evidence of HumT adoption. This paper neither certifies PERSONA nor makes its label thresholds regulatory standards. An offline allocation simulation is not automatically an external assurance audit. The 2024 legal illustration is not treated here as current legal advice.

### L8. FAccT Anthropomorphism: Behavioral Evidence

**Jeffrey Basoah, Daniel Chechelnitsky, Tao Long, Katharina Reinecke, Chrysoula Zerva, Kaitlyn Zhou, Mark Díaz, and Maarten Sap. 2025. _Not Like Us, Hunty: Measuring Perceptions and Behavioral Effects of Minoritized Anthropomorphic Cues in LLMs._** Proceedings of the 2025 ACM Conference on Fairness, Accountability, and Transparency, 710-745. DOI: [10.1145/3715275.3732045](https://doi.org/10.1145/3715275.3732045). [Author record](https://arxiv.org/abs/2505.05660); [author full text v3](https://arxiv.org/html/2505.05660v3); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3715275.3732045).

**Supports:** Studies with 498 African American English speakers and 487 Queer slang speakers measure reliance and perceptions during question-answering. The authors report greater reliance on the standard-American-English agent in both groups, but perception and preference patterns differ by group/cue.

**Limits:** This is behavioral evidence for particular tasks and sociolect manipulations, not a universal causal law about warmth or a HumT-screening evaluation. Neither standard-language superiority nor general sociolect suppression follows. It demonstrates why perception ratings and actual reliance should not be treated as interchangeable outcomes.

### L9. FAccT Anthropomorphism: Parasociality

**Takuya Maeda and Anabel Quan-Haase. 2024. _When Human-AI Interactions Become Parasocial: Agency and Anthropomorphism in Affective Design._** The 2024 ACM Conference on Fairness, Accountability, and Transparency, 1068-1077. DOI: [10.1145/3630106.3658956](https://doi.org/10.1145/3630106.3658956). [Conference-hosted full text](https://facctconference.org/static/papers24/facct24-71.pdf); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3630106.3658956).

**Supports:** A literature-based conceptual framework connects parasociality, affordances, and trust, discussing reciprocal-engagement illusions, task misalignment, and sensitive-information disclosure.

**Limits:** It supplies conceptual mechanisms and ethical concerns, not measured incidence, a HumT threshold, or evidence that PERSONA ratings capture parasocial relationships. A response-level study should not claim to observe sustained relationships or trust-forming processes on this citation alone.

### L10. FAccT Anthropomorphism: Limits of Output-Level Harm Measures

**Jennifer Chien and David Danks. 2024. _Beyond Behaviorist Representational Harms: A Plan for Measurement and Mitigation._** The 2024 ACM Conference on Fairness, Accountability, and Transparency, 933-946. DOI: [10.1145/3630106.3658946](https://doi.org/10.1145/3630106.3658946). [Conference-hosted full text](https://facctconference.org/static/papers24/facct24-61.pdf); [publisher-deposited metadata](https://api.crossref.org/works/10.1145/3630106.3658946).

**Supports:** A conceptual expansion of representational harms to cognitive and affective states, with measurement requirements and an LLM case study. Section 5 discusses anthropomorphism among relevant design features.

**Limits:** The framework is not a validated PERSONA harm instrument or a measurement of psychological change in PERSONA participants. It motivates examining what response-only judgments cannot observe, rather than relabeling every concerning response as a realized harm.

## 3. Keep the Evidentiary Levels Separate

The following distinctions are this memo's synthesis and study-design recommendations, grounded particularly in [measurement modeling](https://arxiv.org/pdf/1912.05511), [application-centric evaluation](https://facctconference.org/static/pdfs_2022/facct22-3533233.pdf), and the different evidence types in L1-L10. They are not results from the local PERSONA data.

| Level | Question | Evidence needed | Inference not licensed |
|---|---|---|---|
| Construct interpretation | Does the score support the intended interpretation of human-like tone here? | Appropriate human judgments, reliability, linguistic/contextual coverage, and examination of alternatives. | A tone score equals overall appropriateness, deception, or harm. |
| Criterion association | Does the score covary with a separately defined concern label? | Associations with uncertainty and a defensible label construction. | Correlation establishes causation, a useful operating threshold, or calibrated risk. |
| Offline allocation performance | At a specified budget, which labeled cases enter or miss the queue? | A frozen allocation rule, independently available criteria, equal-budget comparisons, counts, and uncertainty. | The organization will detect those cases, act on them, or improve outcomes. |
| Use effectiveness | Does introducing this allocation process improve the intended review workflow? | Workflow evidence on reviewers, time/cost, decisions, escalation, and a credible comparator. | Offline recall alone establishes an effective audit program. |
| Downstream consequences | Does the process reduce deception, overreliance, dependence, or other harm? | Direct, appropriately designed evidence about those outcomes and relevant populations. | Tone reduction or favorable ratings demonstrate harm reduction. |

Do not make validity a permanent binary property of a number. Specify the interpretation, population, context, and use for which evidence is offered. Conversely, do not predetermine that HumT is useless: an allocation study must allow for useful performance, conditional utility, or no advantage over its comparators.

## 4. Precise Gap and Claim Boundary

**Candidate gap, conditional on further novelty checking:** The sources verified here do not evaluate the performance of the particular proposed policy that ranks PERSONA responses by HumT and allocates a fixed review budget against separately elicited, domain-bounded concern criteria. This is narrower than "anthropomorphism has risks," "context matters," "tone is not appropriateness," or "audits need criteria." Those broad motivations already have substantial coverage in the sources above.

The absence of this particular experiment in ten selected papers does not establish a first-ever contribution. Likewise, feasibility on an existing dataset does not establish significance, policy distinctness, or acceptance prospects.

### Proposed Study Object

Define a tuple before interpreting results: **reviewer/decision owner; response population; concern criterion; available score; allocation rule; budget; review action; comparator; evaluation outcome**. For example, a proposed pre-release reviewer might inspect the highest-scoring fraction of responses for a separately specified misleading-capability concern. This is a study scenario, not a reported industry workflow. No particular budget or threshold is justified merely because it appeared in the prior notes.

### Evidence That Would Make the Allocation Claim Informative

These are recommendations, not computations performed here:

- Compare allocation at equal review cost or explicitly assume equal per-response cost. Equal item counts need not mean equal reviewer time.
- Report concern prevalence, captured cases, missed cases, review yield, and uncertainty alongside ranking summaries. Distinguish the fraction of positive cases missed from the positive fraction among unreviewed cases.
- Separate pooled allocation from within-domain allocation. These embody different resource choices; domain composition can change apparent performance.
- Include a random-review comparator and feasible simple alternatives. An alternative using human concern ratings unavailable before review is an oracle/reference ceiling, not a cost-equivalent deployable baseline.
- Do not label all unreviewed cases "safe." "False reassurance" describes an additional interpretation of a non-flag as assurance; if that interpretation is not observed, report missed labeled cases instead.
- Distinguish human judgments of misleading implications, domain fit, or overall appropriateness from actual deception, actual domain outcomes, and universal normative truth. Retain disagreement and justify the chosen concern thresholds.
- Reserve operational-effectiveness claims for evidence about actual reviewers and actions. A replay assuming perfect detection after selection estimates opportunity for detection, not achieved detection.
- Ground the proposed use with practitioners or documented workflows if available, without claiming such evidence has already been collected. New stakeholder evidence may improve practical grounding, but it is neither a guaranteed novelty remedy nor publication-policy clearance.

**Suggested prospective wording:** "We evaluate a proposed HumT-based review-allocation rule on a bounded response corpus, measuring coverage of independently specified concern labels at fixed budgets. We do not study an established organizational HumT-screening deployment, infer realized harm from these labels, or test the causal effect of lowering tone."

## 5. Live Venue Policies: 2 October 2026

### FAccT 2027 CFP

The [official CFP](https://facctconference.org/2027/cfp.html) currently lists:

| Milestone | Date |
|---|---|
| Abstract | 27 October 2026 |
| Full paper | 3 November 2026 |
| Initial decision | 22 December 2026 |
| Revision/rebuttal | 28 January 2027 |
| Final decision | 23 March 2027 |
| Camera-ready | TBD |
| Conference | 21-24 June 2027 |

Deadlines are 23:59 AoE. Conversion to Pakistan time is 16:59 the following day: abstract 28 October; full paper 4 November. Conference dates are not deadline times.

The CFP sets 14 content pages excluding references, plus one endmatter-only page; revision/accepted versions allow 15 content pages. It prohibits identical or substantially similar concurrent/published/accepted work. Evaluation practices is a relevant focus area, but purely hypothetical concerns or insufficient social engagement are out of scope. All authors must sign up to review, subject to selection; noncompliance can trigger rejection. [Official CFP](https://facctconference.org/2027/cfp.html).

### FAccT Author Guide

The [official guide](https://facctconference.org/2027/authorguide.html) specifies single-column anonymous review: `\documentclass[manuscript,screen,review,anonymous]{acmart}`. Figures/tables count; references are unlimited. Unlimited appendices belong in the same PDF and need not be reviewed. The paper must stand alone. External materials must preserve anonymity. AI-use disclosure is required even for non-use; an ethics statement should accompany submission.

Representative abstract registration is mandatory; the author list and archival choice then freeze. Non-archival status does not enable overlapping conference submissions; its journal exception is conditional. The CHI FAQ permits abstract registration but requires FAccT withdrawal before the paper deadline if the other paper is accepted or remains under review beyond it. Its question assumes notification between FAccT deadlines, unlike CHI's general schedule below; clarify applicability rather than assume blanket permission.

Uncertainties: the guide encourages one reviewer volunteer, conflicting with the CFP's all-author requirement; seek clarification and plan for the stricter wording. Neither page supplies a numerical substantial-similarity test. Separate artifact review is not promised by these pages. [Author Guide](https://facctconference.org/2027/authorguide.html).

### CHI 2027 Papers

The [official Papers page](https://chi2027.acm.org/authors/papers/) specifies:

| Milestone | Date |
|---|---|
| Paper, including supplements | 10 September 2026 |
| Reviews | 5 November 2026 |
| Resubmission | 3 December 2026 |
| Final notification | 17 December 2026 |

CHI has no separate abstract deadline; dates use AoE. Its contingency grace period is expressly not an extension. Single-column anonymous review is required. CHI encourages 5,000-8,000 words, not FAccT's 14-page limit; over 12,000 requires strong justification. Abstracts are at most 150 words.

CHI prohibits concurrent review of the same work. Closely related concurrent submissions based on the same study, artifact, or dataset must be supplied anonymously in the concurrent-submissions field; disclosure does not itself authorize duplicate work. [CHI Papers](https://chi2027.acm.org/authors/papers/).

The [official review-process announcement](https://chi2027.acm.org/2026/08/17/how-the-chi-2027-papers-review-process-will-work/) anticipates notification **around 26 October** for papers not proceeding to full external review. This is approximate, not a promised rejection date or a guarantee for PERSONA.

### Implications and Unresolved Decisions

**Inference from the verified schedules:** November 5 CHI reviews arrive after the November 3 FAccT paper deadline. Waiting for the ordinary CHI review release therefore does not resolve a concurrent-submission conflict in time. An actual early rejection or completed withdrawal changes the situation; an anticipated rejection does not.

**No clearance:** This memo has not inspected both complete manuscripts or confirmed the private CHI submission status. Reusing a dataset does not automatically prove duplication, but replacing prediction analyses with allocation curves does not automatically prove independence either. Before relying on a related-paper route, provide both venues' chairs an honest side-by-side account of shared data, annotations, methods, figures, results, and claims. Ask CHI how to update related-submission disclosure after its September deadline, and ask FAccT about the FAQ timing mismatch and substantial similarity. No contact was made here. Contacts: [FAccT CFP](https://facctconference.org/2027/cfp.html), `program-chairs@facctconference.org`; [CHI Papers](https://chi2027.acm.org/authors/papers/), `papers@chi2027.acm.org`.

These are live-page observations, not immutable future policy. Recheck before registration/submission. The general ACM simultaneous-submission page returned HTTP 403 during verification; no detailed ACM-wide exception is asserted from inaccessible text. The venue-specific rules above were directly accessible.

## 6. Research Boundaries and Handoff

- Verified: all ten literature identities above, their linked primary-source support limits, and the live venue dates and relevant requirements stated here.
- Not established: organizational HumT-screening adoption, novelty across all literature, validity of PERSONA labels, local empirical results, real-world use effectiveness, or safe distinctness from CHI.
- Search scope: the requested works, their author/publisher/conference records, author repository, and targeted searches combining HumT/HumT DumT with screening, audit, review allocation, and organizational use. Irrelevant acronym matches and secondary summaries were not used as evidence. The three FAccT anthropomorphism entries are relevant precedents, not an exhaustive 2026 literature census.
- The sibling notes' numerical findings, annotation independence, score computation, data lineage, and model provenance remain for the local team to verify. No exploratory percentage or cutoff from those notes is promoted to a confirmed result or normative standard here.
- Only this memo was created. Nothing was published, submitted, uploaded, or sent to another party.
