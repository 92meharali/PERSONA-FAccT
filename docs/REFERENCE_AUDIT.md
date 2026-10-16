# Reference Audit

Audit date: 2026-09-06

## Scope and method

All 35 entries in `paper/ref.bib` were checked against authoritative publication records and compared with the 35 entries in the author-supplied bibliography. DOI-bearing works were checked against their DOI registrations and publisher records; ACL papers against ACL Anthology; preprints against current arXiv records and, for HealthBench, OpenAI's publication page; legal materials against EUR-Lex; and books or law-review articles against publisher or journal repositories.

## Bottom line

- **Fabricated or nonexistent references: none found.** Every work in the current bibliography corresponds to a real publication.
- **Wrong-work substitutions in the supplied bibliography: two.** `turkle2011` describes a 2025 review of two books rather than Turkle's book, and `EUAIAct2024` describes a 2025 *International Legal Materials* reproduction rather than the official 2024 EU regulation. Both substituted records are real, but they are not the works the manuscript intends to cite.
- **Current bibliography entries identified for correction or completion: eight.** All eight corrections were applied after verification. The other 27 entries already matched their authoritative records in all core fields.

## Corrections applied after the audit

| Key | Finding | Authoritative evidence |
|---|---|---|
| `cheng2025` | Added the final ACL DOI and publisher. | [ACL Anthology](https://aclanthology.org/2025.acl-long.1261/) |
| `waytz2010` | Added DOI `10.1177/1745691610369336`. | [SAGE journal record](https://journals.sagepub.com/doi/10.1177/1745691610369336) |
| `araujo2018` | Added DOI `10.1016/j.chb.2018.03.051`. | [DOI record](https://doi.org/10.1016/j.chb.2018.03.051) |
| `EUAIAct2024` | Restored the official full title, institutional authorship, and EUR-Lex URL. | [Official EUR-Lex text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en) |
| `kaminski2017` | Corrected Matthew Rueben's surname and added issue `4`. | [Maryland Law Review repository](https://digitalcommons.law.umaryland.edu/mlr/vol76/iss4/5/) |
| `Weidinger2022Risks` | Corrected Amelia Glaese's given name. | [DOI/ACM record](https://doi.org/10.1145/3531146.3533088) |
| `Bucinca2021CognitiveForcing` | Corrected the publication type to `@article` and added pages `1--21` and article number 188. | [DOI/ACM record](https://doi.org/10.1145/3449287) |
| `aristotle2009` | Added the revised-edition information, W. D. Ross's initials, and the OUP DOI. | [Oxford University Press](https://doi.org/10.1093/actrade/9780199213610.book.1) |

These findings concern citation metadata, not the manuscript's empirical results or interpretation.

## Material problems in the supplied bibliography

The rebuild corrected many real problems in the author-supplied bibliography; the eight remaining issues were then corrected following this audit:

| Key | Supplied-file problem | Current-file result |
|---|---|---|
| `abercrombie2023` | Invalid `@unknown` type, missing Verena Rieser, and preprint DOI used instead of the final EMNLP record. | Correct final paper metadata. |
| `araujo2018` | Author and pages absent. | Author and pages restored; DOI still needs adding. |
| `ayers2023` | Several initials were lost and Davey M. Smith was listed as “David Smith.” | Correct author names and publication details. |
| `cheng2025` | Preprint rather than the final ACL paper. | Final venue and pages restored; final DOI and publisher still need adding. |
| `EUAIAct2024` | Cited a real 2025 journal reproduction by Nathalie Smuha, not the official 2024 legal act. | Correct legal instrument, but official title and institutional authorship remain incomplete. |
| `go2019` | Page range absent. | Corrected. |
| `kaminski2017` | Generic `colorado.edu` URL rather than the article record. | Article metadata restored, but “Rueben” was inadvertently changed to the incorrect “Ruben,” and issue 4 remains absent. |
| `CounselBench2025` | Year was given as 2026 although arXiv records initial publication in 2025. | Corrected. The current title is also correct for arXiv v4; older indexed pages show the earlier “Mental Health Counseling” title. |
| `mathdial2023` | Final venue absent and surname spelling did not match the authoritative ACL record (“Macina”). | Corrected final ACL metadata. |
| `nass1994` | Pointed to the one-page CHI companion record (DOI `10.1145/259963.260288`, page 204, Ellen Siminoff) rather than the canonical six-page paper (DOI `10.1145/191666.191703`, pages 72--78, Ellen R. Tauber). | Correct canonical paper metadata. |
| `nass20000` | Citation key had an extra zero. | Corrected to `nass2000`, matching the manuscript citation. |
| `nissenbaum2004` | Issue and pages absent. | Corrected. |
| `reeves1996` | Misclassified as an article, title truncated, and repository listed as a journal. | Correctly represented as the 1996 Cambridge University Press book. |
| `sharkey2021` | Used online-first pages `1--8` rather than final issue pages `309--316`. | Corrected. |
| `sharma2020` | Final venue absent. | Corrected. |
| `turkle2011` | Wrong work: a 2025 review by Daniel German was placed under a key intended for Sherry Turkle's 2011 book. | Correctly cites Turkle's real 2011 book. |
| `bridge2024` | Cited only the arXiv preprint rather than the final NAACL paper. | Correct final venue, pages, and DOI. |
| `Weidinger2022Risks` | Julia Haas and Sean Legassick were omitted from the author list. | Both restored, but Amelia Glaese's given name is currently wrong. |

Invalid `@unknown` entry types in the supplied file (`abercrombie2023` and `healthbench2025`) were also replaced with valid BibTeX types. This was a structural correction rather than evidence that either work was invented.

## Complete entry ledger

“Verified” means the current entry's core identity fields (work, authors, title, year, venue, volume/issue/pages where applicable) agree with the authoritative record. “Verified after correction” identifies the eight records corrected after this audit.

| Key | Status | Primary record |
|---|---|---|
| `cheng2025` | Verified after correction | [ACL Anthology](https://aclanthology.org/2025.acl-long.1261/) |
| `devrio2025` | Verified | [ACM DOI record](https://doi.org/10.1145/3706598.3714038) |
| `abercrombie2023` | Verified | [ACL Anthology](https://aclanthology.org/2023.emnlp-main.290/) |
| `epley2007` | Verified | [APA DOI record](https://doi.org/10.1037/0033-295X.114.4.864) |
| `waytz2010` | Verified after correction | [SAGE journal record](https://journals.sagepub.com/doi/10.1177/1745691610369336) |
| `epley2008` | Verified | [DOI record](https://doi.org/10.1521/soco.2008.26.2.143) |
| `sharma2020` | Verified | [ACL Anthology](https://aclanthology.org/2020.emnlp-main.425/) |
| `leong2019` | Verified | [ACM DOI record](https://doi.org/10.1145/3287560.3287591) |
| `CounselBench2025` | Verified against current v4 | [arXiv](https://arxiv.org/abs/2506.08584v4) |
| `EUAIAct2024` | Verified after correction | [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj?locale=en) |
| `nass1994` | Verified | [ACM DOI record](https://doi.org/10.1145/191666.191703) |
| `reeves1996` | Verified | [Cambridge University Press catalogue evidence](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/D56680C854C9E122727BAAF9E65FE6F6/S0890060400001876a.pdf/aie_volume_11_issue_2_cover_and_back_matter.pdf) |
| `nass2000` | Verified | [Wiley DOI record](https://doi.org/10.1111/0022-4537.00153) |
| `bickmore2005` | Verified | [ACM DOI record](https://doi.org/10.1145/1067860.1067867) |
| `araujo2018` | Verified after correction | [Elsevier DOI record](https://doi.org/10.1016/j.chb.2018.03.051) |
| `feine2019` | Verified | [Elsevier DOI record](https://doi.org/10.1016/j.ijhcs.2019.07.009) |
| `go2019` | Verified | [Elsevier DOI record](https://doi.org/10.1016/j.chb.2019.01.020) |
| `lee2004` | Verified | [SAGE DOI record](https://doi.org/10.1518/hfes.46.1.50_30392) |
| `nissenbaum2004` | Verified | [Washington Law Review repository](https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/) |
| `ayers2023` | Verified | [JAMA DOI record](https://doi.org/10.1001/jamainternmed.2023.1838) |
| `sharma2021` | Verified | [ACM DOI record](https://doi.org/10.1145/3442381.3450097) |
| `kaminski2017` | Verified after correction | [Maryland Law Review repository](https://digitalcommons.law.umaryland.edu/mlr/vol76/iss4/5/) |
| `sharkey2021` | Verified | [Springer DOI record](https://doi.org/10.1007/s10676-020-09573-9) |
| `Weidinger2022Risks` | Verified after correction | [ACM DOI record](https://doi.org/10.1145/3531146.3533088) |
| `bender2024` | Verified | [SAGE DOI record](https://doi.org/10.1177/09637214231217286) |
| `Shanahan2024Talking` | Verified | [ACM DOI record](https://doi.org/10.1145/3624724) |
| `Bucinca2021CognitiveForcing` | Verified after correction | [ACM DOI record](https://doi.org/10.1145/3449287) |
| `weizenbaum1966` | Verified | [ACM DOI record](https://doi.org/10.1145/365153.365168) |
| `turkle2011` | Verified | [Basic Books/Hachette publisher record](https://www.hachettebookgroup.com/titles/sherry-turkle/alone-together/9780465093656/) |
| `aristotle2009` | Verified after correction | [Oxford University Press](https://doi.org/10.1093/actrade/9780199213610.book.1) |
| `dey2001` | Verified | [Springer DOI record](https://doi.org/10.1007/s007790170019) |
| `dourish2004` | Verified | [Springer DOI record](https://doi.org/10.1007/s00779-003-0253-8) |
| `healthbench2025` | Verified | [OpenAI publication](https://openai.com/index/healthbench/) and [arXiv](https://arxiv.org/abs/2505.08775) |
| `mathdial2023` | Verified | [ACL Anthology](https://aclanthology.org/2023.findings-emnlp.372/) |
| `bridge2024` | Verified | [ACL Anthology](https://aclanthology.org/2024.naacl-long.120/) |

## Conclusion

No reference should be deleted as fabricated because no fabricated or nonexistent work was found. The eight metadata corrections identified by the audit have been applied without changing the manuscript's reference set.
