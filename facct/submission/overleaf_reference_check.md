# Overleaf reference check

Verified 2026-10-02. Six additional primary references for the existing computational-only study; no new experiments or completed human-review claims. Entries below are minimal BibTeX transcriptions of publisher exports, publisher-deposited DOI records, or author-submitted papers. Citation keys and TeX escaping are normalized. Suggested uses are editorial recommendations, not new study findings.

## 1. Saito and Rehmsmeier (2015): imbalanced outcomes

**Supported claim/use:** Precision-recall reporting exposes the fraction of correct positive predictions under class imbalance; ROC alone can obscure this interpretation. The PR baseline depends on positive prevalence. Useful rationale for interpreting existing ranking metrics, not evidence that a rubric trigger measures experienced harm or that ROC is universally invalid. [Primary article, theoretical-background sections](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432).

Metadata checked against the [PLOS BibTeX export](https://journals.plos.org/plosone/article/citation/bibtex?id=10.1371/journal.pone.0118432). The article's canonical citation uses e0118432; the export instead supplies internal pages 1-21. The entry uses the canonical article identifier.

```bibtex
@article{saito2015precision,
  author = {Saito, Takaya and Rehmsmeier, Marc},
  title = {The Precision-Recall Plot Is More Informative than the {ROC} Plot When Evaluating Binary Classifiers on Imbalanced Datasets},
  journal = {PLOS ONE},
  year = {2015},
  volume = {10},
  number = {3},
  pages = {e0118432},
  doi = {10.1371/journal.pone.0118432},
  url = {https://doi.org/10.1371/journal.pone.0118432}
}
```

## 2. Pedregosa et al. (2011): software attribution

**Supported claim/use:** scikit-learn is a Python machine-learning library with a consistent API. Cite for software attribution where used, including the existing metric cross-check, not as proof of study validity. [JMLR publication record](https://jmlr.org/papers/v12/pedregosa11a.html).

All 16 authors follow the [official JMLR BibTeX](https://jmlr.org/papers/v12/pedregosa11a.bib), not the expanded later arXiv author list. No DOI is supplied by that publisher record; omit rather than invent one. For the specific AP implementation, the [official function documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html) defines recall-increment-weighted, non-interpolated AP, distinct from trapezoidal PR area. Do not attribute that modern implementation detail to the 2011 article alone; record the actually used software version separately.

```bibtex
@article{pedregosa2011scikit,
  author = {Fabian Pedregosa and Ga{\"e}l Varoquaux and Alexandre Gramfort and Vincent Michel and Bertrand Thirion and Olivier Grisel and Mathieu Blondel and Peter Prettenhofer and Ron Weiss and Vincent Dubourg and Jake Vanderplas and Alexandre Passos and David Cournapeau and Matthieu Brucher and Matthieu Perrot and {\'E}douard Duchesnay},
  title = {{Scikit-learn}: Machine Learning in {Python}},
  journal = {Journal of Machine Learning Research},
  year = {2011},
  volume = {12},
  number = {85},
  pages = {2825--2830},
  url = {https://jmlr.org/papers/v12/pedregosa11a.html}
}
```

## 3. Mitchell et al. (2019): reporting-card precedent

**Supported claim/use:** Model cards propose documenting intended uses, evaluation procedures, and performance under relevant conditions. This supports a documentation-design precedent for the proposed reporting card, not evidence that this study's card was evaluated, adopted, or improved decisions. [Author-submitted paper](https://arxiv.org/abs/1810.03993).

Authors checked against that paper; 2019 proceedings fields checked against [ACM-deposited Crossref BibTeX](https://api.crossref.org/works/10.1145/3287560.3287596/transform/application/x-bibtex). ACM's article page returned HTTP 403. Cite the 2019 proceedings publication, not the 2018 initial preprint date.

```bibtex
@inproceedings{mitchell2019modelcards,
  author = {Mitchell, Margaret and Wu, Simone and Zaldivar, Andrew and Barnes, Parker and Vasserman, Lucy and Hutchinson, Ben and Spitzer, Elena and Raji, Inioluwa Deborah and Gebru, Timnit},
  title = {Model Cards for Model Reporting},
  booktitle = {Proceedings of the Conference on Fairness, Accountability, and Transparency},
  year = {2019},
  pages = {220--229},
  publisher = {ACM},
  doi = {10.1145/3287560.3287596},
  url = {https://doi.org/10.1145/3287560.3287596}
}
```

## 4. Gebru et al. (2021): provenance documentation

**Supported claim/use:** Datasheets propose recording dataset motivation, composition, collection, processing, uses, distribution, and maintenance. Useful for organizing existing source/reuse disclosures; documentation alone does not establish consent, independent auditing, or suitability for deployment. [Author manuscript, section 3](https://arxiv.org/html/1803.09010v8).

Publication fields checked against [ACM-deposited Crossref BibTeX](https://api.crossref.org/works/10.1145/3458723/transform/application/x-bibtex); all seven authors checked against the [author record](https://arxiv.org/abs/1803.09010). Crossref incorrectly parses the suffix as `III, Hal Daume`; the entry below encodes the primary paper's name, Hal Daume III, with the accent and suffix preserved. ACM's article page returned HTTP 403. Use 2021 for CACM, not the initial 2018 preprint.

```bibtex
@article{gebru2021datasheets,
  author = {Gebru, Timnit and Morgenstern, Jamie and Vecchione, Briana and Vaughan, Jennifer Wortman and Wallach, Hanna and Daum{\'e}, III, Hal and Crawford, Kate},
  title = {Datasheets for Datasets},
  journal = {Communications of the ACM},
  year = {2021},
  volume = {64},
  number = {12},
  pages = {86--92},
  doi = {10.1145/3458723},
  url = {https://doi.org/10.1145/3458723}
}
```

## 5. Arora et al. (2025): HealthBench source

**Supported claim/use:** HealthBench introduces 5,000 multi-turn health conversations with conversation-specific rubrics developed by physicians. Cite as upstream dataset context only where the local provenance identifies HealthBench-derived material. Its physician involvement is not evidence of physician review of this study's responses or clinical effectiveness. Title, all 12 authors, year, and arXiv DOI verified from the [author-submitted record](https://arxiv.org/abs/2505.08775). This is a preprint citation, not an asserted peer-reviewed venue.

```bibtex
@misc{arora2025healthbench,
  author = {Rahul K. Arora and Jason Wei and Rebecca Soskin Hicks and Preston Bowman and Joaquin Qui{\~n}onero-Candela and Foivos Tsimpourlas and Michael Sharman and Meghan Shah and Andrea Vallone and Alex Beutel and Johannes Heidecke and Karan Singhal},
  title = {{HealthBench}: Evaluating Large Language Models Towards Improved Human Health},
  year = {2025},
  eprint = {2505.08775},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.2505.08775},
  url = {https://arxiv.org/abs/2505.08775}
}
```

## 6. Macina et al. (2023): MathDial source

**Supported claim/use:** MathDial collects tutoring dialogues between human teachers and an LLM simulating student errors, grounded in multi-step mathematics problems. Cite for upstream data construction, not as evidence that this study observed real students, learning gains, or a new human evaluation. [ACL primary record and abstract](https://aclanthology.org/2023.findings-emnlp.372/). All seven authors and publication fields follow the [official BibTeX export](https://aclanthology.org/2023.findings-emnlp.372.bib).

```bibtex
@inproceedings{macina2023mathdial,
  author = {Macina, Jakub and Daheim, Nico and Chowdhury, Sankalan and Sinha, Tanmay and Kapur, Manu and Gurevych, Iryna and Sachan, Mrinmaya},
  title = {{MathDial}: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2023},
  year = {2023},
  pages = {5602--5621},
  publisher = {Association for Computational Linguistics},
  doi = {10.18653/v1/2023.findings-emnlp.372},
  url = {https://aclanthology.org/2023.findings-emnlp.372/}
}
```

## Official acmart distribution

- [CTAN package record](https://ctan.org/pkg/acmart): version **2.20, dated 2026-08-16**, maintained by Boris Veytsman; independently corroborated by the [2026-08-18 release announcement](https://ctan.org/ctan-ann/id/aoP8PCQewRm5rgje@prptp).
- Production download: [CTAN acmart ZIP](https://mirrors.ctan.org/macros/latex/contrib/acmart.zip); [distribution directory](https://mirrors.ctan.org/macros/latex/contrib/acmart/). The download URL was obtained from CTAN; no package was installed or compiled.
- The [distributed README](https://www.ctan.org/tex-archive/macros/latex/contrib/acmart) distinguishes CTAN/ACM production releases from GitHub development versions. Its 2.20 changelog says `2028-08-16`, inconsistent with both the catalogue and release announcement; use the corroborated 2026 date, not that apparent typo. The [ACM template page](https://www.acm.org/publications/proceedings-template) returned HTTP 403, so no ACM-hosted ZIP version was verified.
- This is distribution metadata, not confirmation of the local/Overleaf class version, successful compilation, or venue compliance. Manuscript, bibliography, package assembly, and any local version pin remain the parent's responsibility.
