# Professor revision: verified sources

Checked 2026-11-03. Scope: `paper/references.bib` and this note only; no manuscript or supplement edits and no paper compilation. Keys below match the requested drafting keys. Existing keys are preserved.

## Verification method

Used live official conference/publisher pages, author/institution-hosted papers, and publisher-deposited Crossref records. Search results from secondary aggregators were not used as evidence. Statements below are limited to the source portions actually read. A verified bibliographic record is not evidence that the full paper was read. Applicability cautions are our interpretation, not reported experimental results.

## Citation-ready claims and boundaries

| Key | Safe source-supported claim | Reading/provenance and boundary |
| --- | --- | --- |
| `coston2023validity` | Validity considerations can inform whether a predictive task is justified and whether its data are suitable, rather than merely how to improve an existing predictor. | Read the [IEEE abstract](https://ieeexplore.ieee.org/abstract/document/10136159) and the abstract/introduction of the [author-posted paper](https://arxiv.org/pdf/2206.14983). The citation is the **2023 SaTML publication**, not a 2022 preprint citation. This is a conceptual justification framework, not empirical validation of our detector. |
| `lai2022moderation` | Conditional delegation lets people specify regions where a model should be used; the paper studies interfaces for constructing those rules in content moderation, including in- and out-of-distribution conditions. | Read the abstract/introduction in the [author-hosted paper](https://shcarton.github.io/assets/pdf/Lai%20et%20al.%20-%202022%20-%20Human-AI%20Collaboration%20via%20Conditional%20Delegation.pdf). Supports a delegation/workflow precedent, not a blanket claim that every human-AI workflow improves outcomes. |
| `cohen2006review` | Screening evaluation can measure review effort saved at a specified high recall, with a baseline correction for random sampling. | Read the [author-hosted published paper](https://dmice.ohsu.edu/hersh/jamia-06-sysrev.pdf), especially p. 212, equations (4)-(5), and pp. 213-214. Its WSS is `(TN + FN)/N - (1 - R)`; at recall 0.95, subtract 0.05. Thus raw unreviewed fraction and WSS are **not interchangeable**. The measure assumes roughly equal average review effort per document; it is not directly measured elapsed labor time. |
| `lees2022perspective` | The paper presents a multilingual, character/byte-level Charformer-based toxicity classifier for a new generation of Perspective API, with robustness and deployment evaluations. | Read the [Google Research abstract and its linked author paper](https://research.google/pubs/a-new-generation-of-perspective-api-efficient-multilingual-character-level-transformers/). Use for toxicity-screening provenance, not anthropomorphism detection, and not as proof of which model version the API serves today. |
| `abercrombie2023anthropomorphism` | Linguistic design choices can encourage personification of dialogue systems; the paper discusses potential harms, including over-reliance and reinforced stereotypes, and recommends attention to these cues throughout development and release. | Read the abstract/introduction in the [official EMNLP paper](https://aclanthology.org/2023.emnlp-main.290.pdf); [metadata](https://aclanthology.org/2023.emnlp-main.290/). This is not evidence that any single detected cue necessarily causes harm. |
| `akbulut2024anthropomorphism` | Anthropomorphic features can be benign but can also introduce risks involving emotional connection, over-reliance, privacy, and autonomy; the authors propose research directions for evaluation and mitigation. | Read the [publisher abstract](https://doi.org/10.1609%2Faies.v7i1.31613) and its publisher-deposited Crossref abstract. Do not present it as an experimental estimate of harm frequency or of detector effectiveness. Full publisher PDF access was blocked; title discrepancy recorded below. |
| `wallach2025measurement` | Evaluating generative AI is framed as a social-science measurement problem; a four-level framework is proposed to support conceptual and operational scrutiny of validity. | Read the [official PMLR abstract and citation export](https://proceedings.mlr.press/v267/wallach25a.html). Cite as a **position paper**, not as an empirical validation study. Do not infer that high agreement with labels establishes all downstream uses. |
| `cheng2024anthroscore` | AnthroScore uses masked-language-model probabilities to measure implicit anthropomorphic framing of non-human entities in context; the authors report correspondence with human judgments and study research/news discourse. | Read the abstract/introduction in the [official EACL paper](https://aclanthology.org/2024.eacl-long.49.pdf); [metadata](https://aclanthology.org/2024.eacl-long.49/). Treat it as a measurement comparator, not automatically a harmfulness score or a validated dialogue-triage policy. |
| `messick1995validity` | **Metadata verified; no new substantive interpretation approved from this retrieval.** | [ETS's original institutional article record](https://www.ets.org/research/policy_research_reports/publications/article/1995/buwh.html) confirms title, year, journal, volume, issue, and pages; [APA's Crossref deposit](https://api.crossref.org/works/10.1037/0003-066X.50.9.741) confirms DOI and author. The 1995 journal text was not accessible through the publisher route. ETS also has a **1994 research report** with the same title; do not silently substitute that version. Use the directly read Kane source for the interpretation/use distinction until the journal text is checked. |
| `kane2013validation` | Validation evaluates the inferences and assumptions supporting proposed score interpretations and uses. Evidence for an interpretation does not by itself validate a use, and stronger claims require stronger support. | Read the [publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1111/jedm.12000), which explicitly states these distinctions. Safe motivation for a bounded interpretation/use argument; not evidence that our specific deployment is justified. |

## Verified bibliographic metadata

All requested new entries include complete author lists from the primary records, not `et al.` placeholders. No DOI was invented for Wallach.

| Key | Verified venue, year, pages | Metadata source |
| --- | --- | --- |
| `coston2023validity` | IEEE SaTML 2023, 690-704 | [IEEE-deposited record](https://api.crossref.org/works/10.1109/SaTML54575.2023.00050) |
| `lai2022moderation` | CHI Conference on Human Factors in Computing Systems, 2022, 1-18 | [ACM-deposited record](https://api.crossref.org/works/10.1145/3491102.3501999); 18-page author PDF above |
| `cohen2006review` | JAMIA 13(2), 2006, 206-219 | [Publisher-deposited record](https://api.crossref.org/works/10.1197/jamia.M1929); published PDF above |
| `lees2022perspective` | 28th ACM SIGKDD, 2022, 3197-3207 | [ACM-deposited record](https://api.crossref.org/works/10.1145/3534678.3539147) |
| `abercrombie2023anthropomorphism` | EMNLP 2023, 4776-4790 | [ACL record and BibTeX](https://aclanthology.org/2023.emnlp-main.290/) |
| `akbulut2024anthropomorphism` | Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society 7(1), 2024, 13-26 | [Official citation export](https://ojs.aaai.org/index.php/AIES/citationstylelanguage/get/associacao-brasileira-de-normas-tecnicas?publicationId=29897&submissionId=31613); [publisher deposit](https://api.crossref.org/works/10.1609/aies.v7i1.31613) |
| `wallach2025measurement` | ICML 2025, PMLR 267, 82232-82251 | [Official PMLR record and BibTeX](https://proceedings.mlr.press/v267/wallach25a.html) |
| `cheng2024anthroscore` | EACL 2024, Volume 1: Long Papers, 807-825 | [ACL record and BibTeX](https://aclanthology.org/2024.eacl-long.49/) |
| `messick1995validity` | American Psychologist 50(9), 1995, 741-749 | ETS and APA-deposited records linked above |
| `kane2013validation` | Journal of Educational Measurement 50(1), 2013, 1-73 | [Publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1111/jedm.12000) |

## Existing-entry fixes and metadata cautions

- `passi2019formulation`: added pages 39-48, confirmed by the [author's publication list](https://www.samirpassi.com/publications/) and [ACM deposit](https://api.crossref.org/works/10.1145/3287560.3287567).
- `devrio2025taxonomy`: added pages 1-18 from the [ACM deposit](https://api.crossref.org/works/10.1145/3706598.3714038). [Microsoft Research](https://www.microsoft.com/en-us/research/publication/a-taxonomy-of-linguistic-expressions-that-contribute-to-anthropomorphism-of-language-technologies/) independently confirms author order, title, and CHI 2025 venue.
- `basoah2025hunty`: corrected Mark's surname to `D{\'i}az`, verified in the [official conference-hosted paper](https://facctconference.org/static/docs/facct2025-206archivalpdfs/facct2025-final239-acmpaginated.pdf) and [ACM deposit](https://api.crossref.org/works/10.1145/3715275.3732045). Retained deposited pages 710-745. Caution: the conference-hosted PDF begins at printed page 691, so its local pagination disagrees with the ACM deposit; do not silently mix the two.
- `gebru2021datasheets`: the existing `Daum{\'e}, III, Hal` already uses correct BibTeX `Last, Jr, First` syntax, so it was preserved. The [author-posted record](https://arxiv.org/abs/1803.09010) gives Hal Daume III (with an acute accent on the final e). Caution: the [ACM Crossref deposit](https://api.crossref.org/works/10.1145/3458723) incorrectly splits the name into given `Hal Daume` and family `III`; do not import that split.
- `ibrahim2026anthrobench`: official [proceedings record](https://proceedings.iclr.cc/paper_files/paper/2026/hash/fccb2556dbe783422a27f2b71e5c47da-Abstract-Conference.html) and [BibTeX export](https://proceedings.iclr.cc/paper_files/paper/9264-/bibtex) specify `International Conference on Learning Representations`, year 2026, and pages **156130-156160**. Added that verified range; the PDF has 31 pages.
- `CounselBench2025`: retained this existing key to avoid breaking citations, but kept publication year **2026**, standardized the venue to the same ICLR string, and added pages **95178-95214** from its [official BibTeX export](https://proceedings.iclr.cc/paper_files/paper/10024-/bibtex). Replaced the OpenReview URL with the [official proceedings record](https://proceedings.iclr.cc/paper_files/paper/2026/hash/99946cb64d51ead9d3969db0af65ca2e-Abstract-Conference.html). The [published 37-page PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/99946cb64d51ead9d3969db0af65ca2e-Paper-Conference.pdf) confirms the fuller author names already in our bibliography, although the export abbreviates them. These large ICLR ranges are official proceedings metadata, not numbers extrapolated from PDF length.
- `akbulut2024anthropomorphism`: publisher landing/citation/deposit title uses singular **Risk**; the indexed official PDF heading uses plural **Risks**. Bibliography follows the registered title, with this discrepancy explicit. Journal-style proceedings entry preserves the official volume/issue.
- `lees2022perspective`: the Google author profiles expand some given names, while the paper and ACM deposit use Alyssa Lees and Jeffrey Sorensen; retained the paper's forms. The Google-linked download is an author preprint, not the source of the final proceedings pagination.
- `wallach2025measurement`: retained the PMLR author forms and the `Position:` title prefix. The official publisher record, not a preprint date, establishes the ICML 2025 citation.

## FAccT 2027: live submission requirements

Read the [official 2027 CFP](https://facctconference.org/2027/cfp.html) and [official Author Guide](https://facctconference.org/2027/authorguide.html), the latter marked updated October 2026. These are live rules, not prior-year guidance.

### Length and deadlines (CFP)

- Initial submission: at most **14 pages excluding references**; the CFP permits an additional page for ethics, adverse impacts, and other endmatter statements. Revision-stage and accepted papers may have **15 content pages excluding references**.
- Abstract deadline: **October 27, 2026**. Full-paper deadline: **November 3, 2026, 11:59 PM Anywhere on Earth**. Derived timezone conversion: **November 4, 2026, 4:59 PM Pakistan time (UTC+5)**. Abstract registration is required; the guide rules out late abstracts or full-paper uploads without registration.

### Disclosure and anonymity (Author Guide)

- A **Generative AI Usage Statement is mandatory at submission**, even to report no use. If used, identify the tool/version and tasks supported; authors remain accountable for accuracy, citations, and integrity. Failure to disclose can cause desk rejection. Do not infer a product/version from the user-provided informal label; no personal-use investigation was performed.
- Anonymize names, affiliations, identifying statements, and external repository/material links. Cite prior work in the third person. Omit identifying contributions, acknowledgements, competing interests, and positionality material from the anonymous submission.
- Endmatter does not count toward the page limit; methodological limitations belong in the main text. Appendices are outside the limit, but reviewers need not read them. Conservative formatting choice: keep endmatter to the CFP's stated additional page rather than assuming unlimited endmatter.

## Drafting synthesis (our inference, not a reported result)

Use `kane2013validation`, `coston2023validity`, and `wallach2025measurement` to motivate an explicit, bounded argument connecting labels, scores, and the proposed review workflow. Use `lai2022moderation` and `cohen2006review` as workflow/evaluation precedents. Use the anthropomorphism sources to distinguish linguistic signals, perceived humanness, and downstream harms rather than treating them as the same construct. None of these sources alone verifies this study's detector, chosen threshold, annotation policy, or deployment safety.

## Follow-up: CCS IDs and pinned model limits

Verified 2026-11-03; only this note changed for the follow-up.

### Official ACM CCS data

Retrieved the [official ACM CCS 2012 SKOS XML](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml) directly from ACM and inspected the `rdf:about`, `skos:prefLabel`, and `skos:broader` fields. The web reader/tool page returned 403, but direct retrieval of this official XML succeeded. No third-party taxonomy was used to establish the mappings.

- **Confirmed:** `10010147.10010178` has preferred label `Artificial intelligence` and broader concept `10010147`, whose label is `Computing methodologies`. The requested descriptor `Computing methodologies~Artificial intelligence` is correct.
- **Confirmed:** `10003120.10003121.10003124` has preferred label `Interaction paradigms`, parent `10003120.10003121` (`Human computer interaction (HCI)`), and root `10003120` (`Human-centered computing`). The requested descriptor `Human-centered computing~Interaction paradigms` is correct; the full taxonomy path includes the intermediate HCI level.

### Official model repositories at the project's pinned revisions

Revision hashes were read from `analysis/extension_run.py`; the following JSON files were retrieved directly from the model owners' Hugging Face repositories, not from mutable `main` URLs or third-party copies.

| Model and revision | Field confirmed | Official immutable source |
| --- | --- | --- |
| `facebook/bart-large-mnli` at `d7645e127eaf1aefc7862fd59a17a5aa8558b8ce` | `max_position_embeddings: 1024` | [Pinned config.json](https://huggingface.co/facebook/bart-large-mnli/resolve/d7645e127eaf1aefc7862fd59a17a5aa8558b8ce/config.json) |
| `sentence-transformers/all-MiniLM-L6-v2` at `1110a243fdf4706b3f48f1d95db1a4f5529b4d41` | `max_seq_length: 256` | [Pinned sentence_bert_config.json](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/sentence_bert_config.json) |

Distinguish model capacity from actual screening settings: `nli_scores` currently calls the BART tokenizer with `max_length=512` and `truncation="only_first"` on response/hypothesis pairs. Therefore **1024 is the model's configured positional capacity, not this experiment's input limit**. MiniLM's 256 is its Sentence Transformers sequence-length setting; its underlying [pinned transformer config](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/1110a243fdf4706b3f48f1d95db1a4f5529b4d41/config.json) separately has `max_position_embeddings: 512`. Neither limit is a word count. No inference rerun or code change was performed.
