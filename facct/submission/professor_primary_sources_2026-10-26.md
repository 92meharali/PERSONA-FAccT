# Professor feedback: bounded primary-source memo

Checked 26 October 2026. Scope: source verification and proposed wording only; no manuscript, bibliography, score, or submission changes. No messages sent. Static code inspection is not a reproduction of historical scoring runs.

## 1. HumT: correct explanation and implementation qualification

**Published definition.** Cheng, Yu, and Jurafsky's ACL 2025 paper, Section 3.1, Eq. 1, p. 25985, uses GPT-2 with `D+ = {He said, She said}` and `D- = {It said}`. In its notation:

```text
TD(s) = log(P_D+(s) / P_D-(s))
P_D(s) = (1/n) sum_i sum_{w in D} P_i(w + s[:300]), n = 100.
```

Thus, "She said versus It said" is an illustrative shorthand, not the complete scoring specification: **both He and She belong in the human-side comparison**. The paper explicitly specifies 300 **characters**, not tokens; this is not a local invention. It evaluates prefixed text probabilities, not a prompt asking a model to judge humanness. [Official paper](https://aclanthology.org/2025.acl-long.1261.pdf).

**Released code versus local code.** The paper links the authors' [repository](https://github.com/myracheng/humtdumt). Inspected revision: `cd677776eff1cc47eadb1d9d4b4be6454a9d52ca`. Its [scorer](https://github.com/myracheng/humtdumt/blob/cd677776eff1cc47eadb1d9d4b4be6454a9d52ca/compute_humt_sociot.py#L25) and the local scorer share the relevant computation. Local anchors:

| Operation | Local evidence |
|---|---|
| Human set He/She, nonhuman set It | [compute_humt_sociot_colab.py:100](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:100) |
| GPT-2; train mode keeps dropout active | [compute_humt_sociot_colab.py:121](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:121) |
| Exact nonempty-text template: `He said, "<text>"`, likewise She/It | [compute_humt_sociot_colab.py:149](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:149) |
| 100 forward passes per candidate set; mean and SEM | [compute_humt_sociot_colab.py:144](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:144) |
| First 300 characters, then human-set score minus It score | [compute_humt_sociot_colab.py:195](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:195) |

**Important implementation discrepancy, inferred from code.** Both scorers pass the complete token sequences as labels, take `-outputs.loss`, and apply `torch.logsumexp` to that scalar. Hugging Face's GPT-2 implementation flattens shifted tokens across the batch and uses `CrossEntropyLoss()`; PyTorch defaults to mean reduction. Thus this is a token/batch-averaged log-likelihood contrast, not the paper's literal sum of sequence probabilities. Applying log-sum-exp to a scalar does not recover candidate-specific probabilities. The code also averages negative losses across stochastic passes, rather than taking a log after averaging probabilities. Prefix targets are not masked out. [Transformers 4.43.4 source](https://github.com/huggingface/transformers/blob/v4.43.4/src/transformers/models/gpt2/modeling_gpt2.py#L1217), [PyTorch 2.6 source](https://github.com/pytorch/pytorch/blob/v2.6.0/torch/nn/modules/loss.py#L1281), [local loss computation](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/compute_humt_sociot_colab.py:136). These library versions are those listed in the authors' README, not authenticated versions of the historical local run.

**Ready wording:** "HumT operationalizes human-like tone through a GPT-2 likelihood contrast between text framed as speech by a human speaker (He/She) and by an inanimate source (It). The available scorer evaluates the first 300 characters using the released implementation's mean-loss contrast over 100 dropout-active passes per prefix set." Cite Cheng et al. and the implementation. Do not describe the computed score as a calibrated probability of humanness, deception, harm, or reviewworthiness.

**Provenance boundary.** Say "the available scorer" unless run records establish that it generated every retained value. The existing [provenance consolidation](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/facct/submission/provenance_consolidation.md:16) explicitly distinguishes available code from historical invocation evidence and reports some mismatches between recorded score-input prefixes and rated texts. This memo does not resolve them or recommend silently recomputing scores.

## 2. Actual review practices: two bounded examples

**Facebook, 2020: automated action plus ranked human review.** King and Gotimer describe automated handling of sufficiently certain violations and prioritization of less-certain cases for reviewers using virality, severity, and likelihood of violation, rather than chronology. This supports the existence of automated review allocation in online-content moderation. It is a first-party operational account, not independent evidence of effectiveness or a guarantee of unchanged 2026 practice. It does **not** establish keyword-first filtering, HumT deployment, or clinical AI review. [How We Review Content](https://about.fb.com/news/2020/08/how-we-review-content/), 11 August 2020; page also displays 18 August 2020.

**Wikimedia, 2017: score-based filters and highlights for patrollers.** A released edit-review beta used ORES damaging predictions to filter edits into quality bands and highlight concerning edits. Reviewers could filter broadly while highlighting more concerning cases. This documents deployed assistance for directing human attention, not proof of a single numerical top-k queue or any benefit of HumT. [Matazzoni, Powerful new search tools help edit patrollers find their targets](https://diff.wikimedia.org/2017/05/10/new-filters-edit-review/), 10 May 2017.

**Ready discussion wording:** "Automated signals already help allocate human attention in online-content review: Facebook has described risk-based review prioritization, while Wikimedia has deployed score-based edit filters and highlights. These precedents motivate studying review allocation, not assuming that a human-likeness score is useful for it. A possible workflow would handle explicit policy triggers through rules and rank remaining cases for contextual review. We treat this as a design possibility, not an observed deployment of HumT or an evaluated two-stage workflow."

**Analytical implication, not a source claim:** Whole-corpus comparisons of rules and rankings do not establish incremental benefit *after* a rule filter. That would require a residual-queue analysis with the first-stage rule, remaining budget, and missed cases explicitly reported.

### Citation entries

HumT metadata matches the [ACL record](https://aclanthology.org/2025.acl-long.1261/). The two web entries identify their actual named authors; these are operational sources, not peer-reviewed evaluations.

```bibtex
@inproceedings{cheng2025humtdumt,
  author = {Cheng, Myra and Yu, Sunny and Jurafsky, Dan},
  title = {{HumT DumT}: Measuring and controlling human-like language in {LLMs}},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year = {2025},
  pages = {25983--26008},
  address = {Vienna, Austria},
  publisher = {Association for Computational Linguistics},
  doi = {10.18653/v1/2025.acl-long.1261},
  url = {https://aclanthology.org/2025.acl-long.1261/}
}

@misc{kingGotimer2020review,
  author = {King, Jeff and Gotimer, Kate},
  title = {How We Review Content},
  year = {2020},
  month = aug,
  howpublished = {Facebook Newsroom},
  url = {https://about.fb.com/news/2020/08/how-we-review-content/},
  note = {Published 11 August 2020; accessed 26 October 2026}
}

@misc{matazzoni2017editreview,
  author = {Matazzoni, Joe},
  title = {Powerful new search tools help edit patrollers find their targets},
  year = {2017},
  month = may,
  howpublished = {Wikimedia Foundation Blog, archived on Diff},
  url = {https://diff.wikimedia.org/2017/05/10/new-filters-edit-review/},
  note = {Published 10 May 2017; accessed 26 October 2026}
}
```

## 3. FAccT 2027: format, anonymity, and overlap

Use the **2027** rules for this submission cycle, not remembered 2026 requirements.

- **Initial format:** at most 14 single-column content pages including figures/tables; unlimited references. LaTeX: `\documentclass[manuscript,screen,review,anonymous]{acmart}`. One extra page may contain endmatter only. Appendices are unlimited, in the same PDF, and need not be read. Revisions and accepted papers may have 15 content pages. A Generative AI Usage Statement is required even if no AI was used. [Author Guide, Formatting Instructions and FAQs](https://facctconference.org/2027/authorguide.html).
- **Anonymity:** remove author names/affiliations and identifying acknowledgements, positionality, and competing-interest statements; cite prior work in the third person. Noncompliance can cause desk rejection. [CFP, Anonymity Policy](https://facctconference.org/2027/cfp.html).
- **Actual prohibition:** the CFP excludes identical or substantially similar papers concurrently reviewed elsewhere, already published, or accepted. It does not prohibit every distinct paper by the same team or every reuse of a corpus. [CFP, Concurrent/Dual Submission Policy](https://facctconference.org/2027/cfp.html).
- **CHI FAQ:** an abstract for a paper awaiting another conference's decision may be registered, but that paper must be withdrawn from FAccT before full submission if accepted or still under review then. Read this with the similarity prohibition, not as a ban on unrelated manuscripts. [Author Guide, CHI FAQ](https://facctconference.org/2027/authorguide.html).
- **Exceptions:** preprints, specified workshop/short-paper extensions, and non-archival conference-length versions of journal manuscripts are addressed separately. The journal exception is not permission to dual-submit the same CHI conference paper. [Author Guide, Concurrent and Dual Submission Policy](https://facctconference.org/2027/authorguide.html).

The [15 October official clarification](https://facct-blog.github.io/2026-10-15/preparation) explicitly explains, for a journal example, that shared content alone does not establish an impermissible dual submission when the papers are substantially different. Applying the CFP's same similarity test to distinct conference manuscripts is an interpretation of its general wording, not individual clearance for PERSONA.

**Ready correction to the earlier advice:** "A pending CHI paper does not itself bar a distinct FAccT submission. The prohibition concerns identical or substantially similar work. Whether this companion is sufficiently distinct requires comparing the substantive contributions and overlap, not merely its title or venue. This source check establishes neither eligibility nor chair approval; CHI's own rules also remain applicable."

The CFP lists abstract/full deadlines of **27 October / 3 November 2026, 11:59 PM AoE**, respectively. [Official dates](https://facctconference.org/2027/cfp.html). No chair contact was made.

## 4. Corpus prompt-source references and endpoint wording

The four entries below are copied unchanged from [paper/ref.bib](/Users/meharali/Documents/Codex/2026-08-10/ok/work/PERSONA-FAccT/paper/ref.bib:94). Primary-record checks:

- **CounselBench2025:** the key is historical; its entry correctly says **2026**, not 2025. The [official ICLR proceedings](https://proceedings.iclr.cc/paper_files/paper/2026/hash/99946cb64d51ead9d3969db0af65ca2e-Abstract-Conference.html) confirm the title, author identities, and ICLR 2026 venue. The [first author's publication page](https://www.yahan-li.com/research/) confirms the expanded author names used locally. The OpenReview URL encountered a browser-verification page, so verification used these primary alternatives. Do not conflate the 2026 proceedings title with the differently titled 2025 preprint.
- **bridge2024:** author order, title, venue, year, pages, and DOI agree with the [ACL Anthology record](https://aclanthology.org/2024.naacl-long.120/); local `Novice--Expert` is a typographic variant.
- **mathdial2023:** author order, title, venue, year, pages, and DOI agree with the [ACL Anthology record](https://aclanthology.org/2023.findings-emnlp.372/).
- **healthbench2025:** author order, title, year, arXiv identifier, subject class, and DOI agree with the [author-deposited arXiv record](https://arxiv.org/abs/2505.08775). Retain the preprint entry type; no journal venue is implied.

Bibliographic verification does not authenticate which source items were sampled, transformed, or used in the local corpus. It also does not transfer the original benchmarks' participant populations or evaluation procedures to this study.

**Ready source sentence, conditional on the corpus manifest:** "Prompt sources were CounselBench for mental-health questions, Bridge and MathDial for educational material, and HealthBench for general-health material (\cite{CounselBench2025,bridge2024,mathdial2023,healthbench2025}). These are source datasets, not new participant samples collected for the present analysis." Preserve the manuscript's actual adaptation/sampling description rather than implying complete benchmark reuse.

**Ready endpoint sentence, using the user's supplied record labels:** "The source records label the three generation endpoints as `gpt-5.6-sol`, `anthropic/claude-opus-4.8`, and `z-ai/glm-5.2`. We report these identifiers as recorded, without independently authenticating the underlying model deployments or snapshots." This memo does not independently verify those labels against raw calls.

### Copied corpus BibTeX

```bibtex
@inproceedings{CounselBench2025,
  author = {Li, Yahan and Yao, Jifan and Bunyi, John Bosco S. and Frank, Adam C. and Hwang, Angel Hsing-Chi and Liu, Ruishan},
  title = {CounselBench: A Large-Scale Expert Evaluation and Adversarial Benchmarking of Large Language Models in Mental Health Question Answering},
  booktitle = {The Fourteenth International Conference on Learning Representations},
  year = {2026},
  url = {https://openreview.net/forum?id=8MBYRZHVWT}
}

@inproceedings{bridge2024,
  author = {Wang, Rose and Zhang, Qingyang and Robinson, Carly and Loeb, Susanna and Demszky, Dorottya},
  title = {Bridging the Novice--Expert Gap via Models of Decision-Making: A Case Study on Remediating Math Mistakes},
  booktitle = {Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)},
  year = {2024},
  pages = {2174--2199},
  address = {Mexico City, Mexico},
  publisher = {Association for Computational Linguistics},
  doi = {10.18653/v1/2024.naacl-long.120}
}

@inproceedings{mathdial2023,
  author = {Macina, Jakub and Daheim, Nico and Chowdhury, Sankalan and Sinha, Tanmay and Kapur, Manu and Gurevych, Iryna and Sachan, Mrinmaya},
  title = {{MathDial}: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2023},
  year = {2023},
  pages = {5602--5621},
  publisher = {Association for Computational Linguistics},
  doi = {10.18653/v1/2023.findings-emnlp.372}
}

@misc{healthbench2025,
  author = {Arora, Rahul K. and Wei, Jason and Hicks, Rebecca Soskin and Bowman, Preston and Qui{\~n}onero-Candela, Joaquin and Tsimpourlas, Foivos and Sharman, Michael and Shah, Meghan and Vallone, Andrea and Beutel, Alex and Heidecke, Johannes and Singhal, Karan},
  title = {{HealthBench}: Evaluating Large Language Models Towards Improved Human Health},
  year = {2025},
  eprint = {2505.08775},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.2505.08775}
}
```
