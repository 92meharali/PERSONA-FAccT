# Response to the professor's revision comments

Prepared 3 November 2026. This records implemented changes, not a claim of
submission approval. No source ratings, historical scores or adverse findings
were removed. The previous draft remains recoverable from Git.

## 1. One clear story

- Rewrote the title, abstract, introduction and conclusion around the decision
  to allocate limited human review, with mental health as the lead case.
- Defined HumT and its intended measurement role before introducing the audit.
- Replaced the unsupported claim of routine tone-score deployment with a
  proposed screening workflow and cited moderation/delegation precedents.
- Generalized the research questions without claiming empirical validation
  beyond HumT or demonstrated reviewer effectiveness.
- Reduced the contributions to three concrete items.

## 2. PERSONA and self-contained methods

- Took the professor's lighter resource route, not a rushed combination with
  the earlier regression paper. The paper documents PERSONA's data and
  annotation design without claiming discriminant validity or a second
  framework-validation contribution.
- Added a main-text table of H/E/D/F/OA definitions, score anchors, rating
  sources and evaluation uses.
- Brought the mental-health professional-therapist generation role, source
  datasets, scenario types, rater pools and domain counts into the main text.
- Retained the author/intern dimension-rater provenance and independent
  follow-up arrangement. No licenses, payment facts or generation dates were
  inferred. Repository visibility was checked: the original repository was
  private when checked, but this does not prove it was never public.

## 3. Structure, related work and figures

- Expanded Related Work into anthropomorphism, measurement/use validity, and
  limited review/auditing, with ten verified bibliographic additions (not all
  must be cited if their full text was unavailable).
- Positioned the audit as an operational application of existing validity
  principles; removed the unsupported claim that no worked procedure exists.
- Consolidated the method and retained a separate Results section.
- Added an editable monochrome TikZ workflow in ACM style, separating scoring,
  exact quotas, evaluation labels and held-out training.
- Added a two-panel result figure comparing original and contextual targets
  at all four capacities. Added every plotted point/interval to appendices.
- Discussed AnthroBench, AnthroScore, contextual generative judges and safety
  classifiers without pretending to have evaluated unrun comparators.

## 4. Readability

- Replaced lengthy abstract and contribution sentences with shorter prose.
- Replaced Group A/B shorthand in the active manuscript with descriptive rater
  names, and defined computational terms at first use.
- Moved detailed chronology into one appendix status table; retained the
  distinction between exploratory and previously specified analyses.
- Removed revision-process phrasing from active captions and maintained one
  concise limitations section rather than repeating every qualification.

## 5. Correctness and additional analysis

- Removed claims that alignment was ruled out or that all five implications
  failed. Reported attenuation, the education tie and OA point reversal.
- Removed the semantic comparison as a supposed converse proof against
  alignment; identified its higher-severity and response-only scope.
- Joined all 660 follow-up items by stored IDs, checked text encoding, prompt
  groups and HumT values, and reproduced the original selected IDs in all 12
  policy/budget checks before evaluating cached semantic rankings.
- At 132 slots, captures among 19 positives are: HumT 6, markers 12, length 4,
  similarity 4 and NLI 2; random expectation 3.8. All cells are reported.
- Used 2,000 paired prompt-cluster draws. Similarity minus HumT is -10.5 pp
  [-36.9, +16.7]; NLI minus HumT is -21.1 [-42.3, +5.6]. NLI minus markers is
  -52.6 [-78.6, -25.0], an exploratory comparison, not independent confirmation.
- Retained HumT-marker follow-up uncertainty [-66.7, +4.3]. Qualified the
  exact-binomial/Beta descriptions and sample-size illustration as assuming
  independent cases rather than resolving cluster-level uncertainty.
- Corrected random-baseline, education-fit, equivalence and provenance claims.
- Matched stricter-threshold counts and intervals to the same input variant.
- Replaced the unsupported diagnosis of embedding overfit with observed weaker
  held-out performance and documented the post-inspection PCA choice.
- Identified an additional methodological difference: semantic-feature
  bootstraps resample across domains while retaining folds; the original
  lexical analysis resamples within each fold. Described the difference rather
  than attributing all interval differences to seeds. No historical interval
  was silently changed.

## 6. FAccT framing

- Grounded the interpretation/use distinction in Kane, Coston, Jacobs/Wallach
  and related measurement work. No claim of inventing use validity.
- Added a bounded layered-review interpretation as a proposed application,
  not a tested governance intervention.
- Replaced cost-matched rhetoric with matched review capacity and explicit
  unmeasured inference, annotation and reading costs.
- Distinguished retrospective workload from work saved over sampling.

## 7. Submission and reporting checks

- Added CCS XML and descriptive keywords without overriding ACM labels.
- Expanded ethics adverse-impact language and AI disclosure, including
  editing, paraphrasing, instruction preparation, testing and verification.
- Recorded the author's supplied ChatGPT model label, GPT-6.1-sol. Historical
  Codex snapshot IDs were not inferred.
- Supplied missing MH fit/OA interval endpoints with their resampling-seed
  provenance, and all 18 embedding-feature HumT increment intervals.
- Reported original 100-seed tie ranges, AP/ROC-AUC with prevalence, and pooled
  reference results. Independently checked all fixed-score AP/AUC calculations.
- Corrected the NLI runner's chosen 512-token cap versus architectural capacity;
  separated software environments; preserved unauthenticated endpoint labels.
- Corrected verified bibliography details, numeric minus signs and plot labels.
- Kept every table/figure referenced and checked compilation, anonymity and
  pagination. Numerical source data are immutable.

## 8. Remaining author actions

- Resolved on 3 November 2026: the author confirmed that follow-up assessors
  were compensated through existing paid research roles. The visible
  endmatter placeholder has been replaced with that statement.
- Confirm any historical Codex model identifiers or additional AI tools not
  covered by the supplied model label. The statement reports the current
  information gap rather than inventing versions.
- Generation dates/provider snapshots are not established; the paper says so.
- Authors must verify submission registration, title/abstract, author list,
  reviewer obligations, approvals and the final uploaded PDF themselves.
- No new generative LLM judge, recruitment, reviewer study, deployment or
  controlled chatbot-design experiment was claimed or performed.

## Reproduction

The cached-score extension needs the source project and the private follow-up
frame, but does not send text to any model provider. The computational command
is documented in the project README. The first measured 2,000-draw run took
8.85 seconds; rendering, validation and packaging add time. Original scores and
new aggregate outputs have manifests. The Overleaf ZIP excludes private study
records and local input paths.
