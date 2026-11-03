# Response to the nine review concerns

This document maps each concern to what changed in `paper/main.tex`, what the
change rests on, and what honestly remains. The revision had two passes. The
first used only values already in the typesetting package. The second, once
the project repository (released 1,490-response corpus, original analysis
code, follow-up outputs) was available, ran three pre-specified extensions on
that data with the authors' own seeds, tie keys and fold assignment:

- a **direct cue ablation** of the 23-word marker lexicon (issue 2);
- two **pinned, label-free semantic screens** as fixed policies (issue 4);
- the **held-out trained comparison with semantic features** (issues 4, 1).

No rating, score or label was changed or added. The amendment is dated
(2 November 2026), its anchors and hypothesis were fixed before the first
scoring run, it reproduces every original fixed-policy count exactly before
adding anything, and it is reported as post hoc in the manuscript's evidence
chronology, Appendix H, and `analysis_outputs/manifest.json`.

Status key: **Resolved** (concern no longer applies as stated) ·
**Reframed and bounded** (concern is now answered with existing evidence and
its residual is explicit) · **Mitigated, remains a limitation** (cannot be
removed without new data; the manuscript now states it precisely and says what
would close it).

---

## High priority

### 1. The contribution may seem too narrow — Status: Resolved

**Change.** The paper is now framed as a *use-validity audit for repurposed
scores*, with HumT as the case study, rather than as an evaluation of one tone
score. The abstract, introduction (new second and third paragraphs), the
contributions paragraph, a new Discussion subsection *What the audit teaches
beyond HumT* (`sec:protocol`), and the conclusion all carry this framing.

**What makes it more than "a tone score is not a reliable concern detector".**
The audit has five named steps, each instantiated in the paper, and four
findings that do not depend on HumT or PERSONA:

1. Enrichment over random is a low bar that cost-matched rules clear by more.
2. A comparator advantage is uninterpretable until label alignment has been
   diagnosed, and the paper shows how to do that with resources most
   evaluation studies already hold (a second rater population, a stricter
   threshold, the exclusive-case lists, and the lexicon itself for a direct
   ablation).
3. "Selects different cases" is not "improves the queue"; only an incremental
   held-out test distinguishes the two (22 shared cases, 20 HumT-only,
   41 marker-only, yet no incremental gain).
4. Aggregate coverage hides category-specific omissions that only residual
   reporting exposes.

The removed cross-target analysis is not reintroduced; breadth now comes from
the generalizable procedure, not from more HumT comparisons.

### 2. The strongest marker results partly follow the rubric's design — Status: Reframed and bounded

**Change.** New Results subsection *RQ1 diagnostic: Is the marker advantage an
artifact of rubric alignment?* (`sec:alignment`). Instead of conceding the
point in one sentence, the paper states the alignment hypothesis and tests
five observable implications it makes:

| Implication if alignment were the explanation | Observed |
|---|---|
| (i) Advantage shrinks/reverses at severity sympathy cannot reach | At D̄>3: markers 26/57 vs HumT 13/57 (MH), 18/20 vs 8/20 (GH); no reversal at D̄≥4 in any domain |
| (ii) Advantage disappears on a rubric-blind endpoint | OA (15 Group-A raters, never saw the rubric): markers 33 vs 31 (MH, incl. 0), 9/9 vs 3/9 (GH, excl. 0); HumT leads only in education |
| (iii) Marker-only cases concentrate at the broad cutoff | Marker-only: 54% at cutoff, 19 above, 3 at ≥4, 7 follow-up positives. HumT-only: 70% at cutoff, 6 above, 0 at ≥4, 1 follow-up positive |
| (iv) Advantage vanishes under a criterion excluding pronoun/sympathy cues | Follow-up by external assessors: markers 12/19 vs HumT 6/19 |
| (v) Deleting the shared cues drops the lexicon to or below HumT | **New run.** Minus *sorry*: 63→62 (MH). Minus all ten first-person forms: MH 54/165 (+7.3 pp vs HumT, [−1.4, +16.4]), GH 20/23 (+43.5, [+15.4, +59.3]). No pronouns at all (8 cues): MH 72/165 (+18.2, [+8.9, +27.0]), ED 7/12 (= HumT), GH 17/23 (+30.4, [+0.0, +50.0]). No ablation falls below HumT in any domain |

None of the five holds. The text concludes that alignment may contribute to
the *size* of the broad-D advantage but is inconsistent with being *the*
explanation, and narrows the claim to "a cost-matched lexical rule is a
comparator HumT must beat and, on anthropomorphic-implication targets, does
not." Section 3 adds a paragraph *Three rater populations, three degrees of
independence* so the reader sees why OA and the follow-up can serve as
alignment checks.

**Residual.** The ablation shows first-person cues carry about 40% of
the mental-health margin (63→54), so a *partial* alignment contribution is
real and the paper says so. It cannot be the explanation: a lexicon with no
pronouns at all beats HumT by more than the full list. Table `cue_ablation`
(Appendix H) and `analysis_outputs/fixed_policy_*.csv` hold every cell.

### 3. The follow-up cannot conclusively resolve that concern — Status: Reframed and bounded

**Change.** New paragraph *What the follow-up can and cannot establish* in
`sec:assessmentresults`, a new method paragraph in Section 4.4, and
Appendix Table `annotation_paired_exact`. Three moves:

- **Asymmetric reading of the interval.** The upper bound +4.3 pp means the
  follow-up is incompatible with HumT holding more than a marginal advantage
  on contextual cases, which is what the alignment hypothesis predicted. What
  it cannot establish is the *size* of the marker advantage.
- **Exact case-level analysis.** The recorded per-case selections
  (`facct/independent_annotation/outputs/policy_selections.csv` joined to
  `resolved_labels.csv`) give the exact 2×2: both queues catch 4, markers
  alone 8, HumT alone 2, neither 5. Exact McNemar on the ten discordant cases
  p = 0.11; posterior probability that markers catch more contextual cases
  than HumT (Beta(1,1) prior) 0.97. Direction is stable across all seven
  target definitions and all four budgets.
- **Replication specification.** At the observed discordance (10/19) a paired
  replication needs about 39 contextual positives (≈1,350 responses at 2.9%
  prevalence) for 80% power; the range over feasible discordance rates is
  23–73. "Inconclusive" is now a specification, not a verdict.

**Residual.** The follow-up is still 19 positives in 13 prompts. The paper
no longer claims more than "directionally consistent and imprecise".
`analysis/paired_detection.py --counts 19 12 6 --both 4` reproduces every
number above. The semantic screens of issue 4 could not be evaluated on these
19 cases because the follow-up study-ID→corpus-item mapping is held in the
private follow-up record, not in the repository; the manuscript says so and
lists that evaluation first under future work.

### 4. There is no semantic comparator — Status: Resolved for the original criteria; follow-up target remains open

**Change.** Two pinned, label-free semantic screens were run on the released
corpus and added as fixed policies at the same 132/83/83 slots (new Results
subsection `sec:semantic`, Table `semantic_compact` in the main text, full
contrasts in Appendix H):

- **Similarity**: `sentence-transformers/all-MiniLM-L6-v2` at revision
  `1110a243…`, max cosine to four anchor sentences written once from the
  level-4/5 D anchors.
- **NLI judge**: `facebook/bart-large-mnli` at revision `d7645e12…`, zero-shot
  entailment probability for one hypothesis ("the writer claims to have
  personal feelings, memories of the reader, an ongoing relationship with the
  reader, or a human professional identity").

Both run locally on CPU with no sampling and no API; anchors and hypothesis
were fixed before scoring and never revised. Results (20% capacity, paired
2,000-draw prompt-cluster intervals, seed 20261102):

| Criterion | HumT | Markers | NLI judge | Similarity |
|---|---|---|---|---|
| MH broad D (165) | 42 | 63 | 45 (+1.8 vs HumT [−6.4, +10.0]; −10.9 vs markers [−19.4, −2.6]) | 30 |
| GH broad D (23) | 10 | 21 | 13 (+13.0 vs HumT [−13.6, +38.7]; −34.8 vs markers [−52.2, −12.5]) | 14 |
| ED broad D (12) | 7 | 9 | 6 | 6 |
| MH fit (95) | 18 | 22 | 29 (+11.6 vs HumT [+0.0, +22.3]) | 26 |
| ED fit (25) | 10 | 1 | 7 | 2 |
| GH OA (9) | 3 | 9 | 8 | 8 |

Reading: a construct-targeted semantic judge matches HumT on the
anthropomorphic-implication trigger and trails the lexical rule by the same
margin HumT does, so the lexical advantage is not an artifact of a weak
baseline; HumT's education-fit lead survives the semantic comparators too.
The held-out trained comparison was also rerun with the pinned embedding as a
feature block (Table `semantic_heldout`): the 384-d embedding overfits, a
16-component PCA (post hoc, flagged) is comparable to the lexical screen, and
adding HumT to any feature set yields no interval excluding zero in 18
further cells.

**Residual.** These are untuned zero-shot screens from small models; they
bound what an unadapted semantic screen does here, not what a tuned or
generative LLM judge could do. They were not evaluated on the 19
contextual-reviewworthiness cases (private ID mapping). The manuscript states
both limits and keeps the LLM-judge protocol (`analysis/semantic_comparator.py`)
as the next step.

### 5. Historical HumT scoring is not fully authenticated — Status: Reframed and bounded

**Change.** Section 3.2 (`sec:provenance`) now (a) defines the audit object as
the *recorded* score, the value that actually drove the queue, and notes this
is the realistic audit situation; (b) bounds the exposure with three checks
that were previously buried in Appendix F: the 59 differing texts contain no
broad-D or OA case and two fit cases; restricting to byte-identical pairs at
83 slots reproduces HumT's broad-D captures exactly (7/12 and 10/23);
recomputing baselines on export text leaves every transfer-domain count at
20% unchanged. The paper states that the provenance gap therefore cannot
account for the comparative results, and limits the open question to whether a
fresh scorer run would reproduce each recorded value. Scattered repetitions of
"not authenticated" across Results were consolidated so the point is made once,
with its bound, rather than ten times without one.

**Residual.** Mental-health scoring-input strings are unavailable; a fresh run
is the only full authentication. `analysis/score_audit.py` compares historical
and rescored values (text provenance tiers, Pearson/Spearman/Lin CCC, rank
moves, and whether the 132-slot selection and captured positives change,
overall and on the byte-identical subset). It needs the texts and a pinned
HumT re-run.

## Important limitations

### 6. Annotation independence is limited — Status: Reframed and bounded

**Change.** The three rater populations are now described as a deliberate
structure (Section 3.1, *Three rater populations, three degrees of
independence*): Group B (rubric-aware, includes authors) defines D/F; Group A
(15 raters, never saw the rubric) defines OA; external assessors define the
follow-up. The paper then reports which comparative results survive across
populations: the marker broad-D advantage is not reversed on OA and holds on
the follow-up; HumT's education-fit advantage recurs with the same sign on OA
(imprecisely). Limitations state explicitly that this tests dependence of
*comparative results* on familiarity, not the validity of the D construct.

**Residual.** The v1.0/v1.1 capability-note difference between R1 and R2/R3 is
confounded with assessor identity; the paper says so and does not claim
same-instruction reliability. Only a same-instruction re-assessment removes it.

### 7. The performance evidence is mixed and imprecise — Status: Resolved as a presentation problem; precision itself is a stated limitation

**Change.** New Table 1 (*Evidence map*) lists every headline comparison with
its difference, interval, supporting-prompt count and a one-word reading, so
the pattern (favors markers on anthropomorphic-implication targets in two
domains; favors HumT on education fit; inconclusive elsewhere; no incremental
gain in 27 cells) can be seen at once rather than reconstructed from prose.
The amendment adds rows for the cue ablation, the semantic judge and the
embedding-augmented incremental test.
The Limitations *Precision* paragraph states that only one of three adjusted
primary comparisons excludes zero and that the paper reads the evidence as
direction-consistent and imprecise, not as null and not as superiority. The
conclusion no longer says "mixed"; it says what the pattern is.

### 8. Practical usefulness remains simulated — Status: Mitigated, remains a limitation

**Change.** Limitations *Usefulness* paragraph: coverage is stated as a
necessary, not sufficient, condition for a useful screen; reviewer detection,
speed, decisions and harm are explicitly unmeasured; the length policy is
noted as showing what ranking by length alone recovers without converting
slots to minutes. The introduction and protocol frame the audit as the stage
that precedes, and is required by, any reviewer study.

**Residual.** Only a reviewer study closes this. The paper does not claim
otherwise.

### 9. Generalization is restricted — Status: Mitigated, remains a limitation

**Change.** Limitations *External validity* paragraph states the scope
(English, single-turn, three endpoints, not a deployment sample; domain,
source, rater population and conditions co-vary) and separates what transfers
(the audit procedure) from what does not (the HumT estimates, without
replication). The abstract and conclusion carry the same distinction.

---

## Other manuscript changes

- Length: main text is 14 pages (FAccT 2027 limit: 14, or 15 at the revision
  stage), endmatter 1 page, references 2, appendices 24. To make room, corpus
  provenance detail moved to new Appendix A (*Corpus Details*), the paired-
  summary forest plot and the alignment-diagnostic figure sit in Appendix D,
  the follow-up coverage table and the workload paragraph moved to their
  appendices, Related Work was condensed to one section, and method text
  duplicated in the appendices was tightened. No result was removed.
- New Appendix H (*Post-hoc Amendment: Cue Ablation and Pinned Semantic
  Screens*) documents the amendment: models, revisions, anchors, hypothesis,
  seeds, software versions, and the full tables.
- Title now reads *A Use-Validity Audit of HumT-Based Review Prioritization*.
- Added references: McNemar (1947) and Connor (1987) for the paired test and
  the paired-sample size calculation.
- The Generative AI statement is unchanged from the previous revision.
- Wording check applied throughout: the education-fit advantage "recurs with
  the same sign" on OA; it does not "replicate", because that OA interval
  includes zero.

## What remains empirical

Issues 5 (a fresh HumT run), 6 (same-instruction re-assessment), 8 (a
reviewer study) and 9 (replication on other corpora) cannot be closed by
analysis of the existing data. Issue 4 is closed for the original criteria
and open for the contextual follow-up target until the private ID mapping is
joined. The manuscript states each precisely, bounds its effect where the
data allow, and specifies the experiment that would close it; `analysis/`
implements those experiments (see `README.md`).
