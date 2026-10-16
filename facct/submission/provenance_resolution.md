# Provenance resolution: documented reporting basis

Checked 2 October 2026. The author requested confirmation through GitHub. A fresh fetch confirms origin/main at `7605174f76fc912f3dadb219d93c037f7da27d44`, the same source revision used for the computation. No source dataset or CHI file was modified.

## Findings

| Question | Evidence and conclusion | Verification level |
|---|---|---|
| Final rater design | Final supplement records 20 people: three separate Group A pools of five OA raters, and one separate five-person Group B rating E/D/F across domains. No person in both groups. | Explicit final repository documentation, consistent with submitted PDF pp. 7-8 and released table structure; not an independent identity audit |
| Same-rater phase wording | PROTOCOL_APPLICATION_NOTE explicitly states that phases refer to instruments and that the same-rater fallback was not used. The mental-health rubric presents separate pools as preferred and same-rater work as an alternative. | Apparent documentary contradiction resolved; earlier audit overlooked this application note |
| Compensation | Final ETHICS_AND_PARTICIPANT_PROTECTIONS states compensation through existing grant-supported research roles rather than per-response payment. Submitted PDF p. 8 reports existing paid research roles. | Consistent final reported account; no payroll records, rates or per-person payment history inspected |
| Voluntary participation | Older provenance notes say participation was voluntary and contributions would be acknowledged. | Voluntary participation does not imply absence of compensation; these statements are not inherently contradictory |
| Group B independence | Final documents identify author-team members/interns and rubric-development involvement; raters worked independently. | Distinguish independent scoring from independence of the research team; do not claim external validation |
| Consent and ethics | Final records report consent, withdrawal rights and parent-project institutional approval dated 12 February 2026. PERSONA is documented as a sub-study, not separately named on the approval letter. | Reuse the documented scope; this check is not a new institutional determination or consent audit |
| Current corpus and supplement | Both processed CSVs match the unpacked supplement, and all 69 files in the repository ZIP match the corresponding unpacked files byte-for-byte. | Verified computationally |
| Exact portal-uploaded archive | Author response: "yes i guess". No upload receipt or portal-downloaded archive supplied. | Tentative recollection, not verified identity; retain this narrow caveat |

## Authoritative record links

- [Final protocol application note at the verified revision](https://github.com/92meharali/PERSONA-MH-CHI/blob/7605174f76fc912f3dadb219d93c037f7da27d44/submission/chi2027_supplement/PROTOCOL_APPLICATION_NOTE.md)
- [Final ethics/participant record at that revision](https://github.com/92meharali/PERSONA-MH-CHI/blob/7605174f76fc912f3dadb219d93c037f7da27d44/submission/chi2027_supplement/ETHICS_AND_PARTICIPANT_PROTECTIONS.md)
- [Supplement overview at that revision](https://github.com/92meharali/PERSONA-MH-CHI/blob/7605174f76fc912f3dadb219d93c037f7da27d44/submission/chi2027_supplement/README.md)

The supplement was introduced in commit `ab4d6149ac169b030bd7e93b948f7db184990c9d` (10 September 2026). A Git commit and a repository ZIP are not proof of a conference upload.

## Artifact fingerprints

- Repository `submission/chi2027_supplement.zip`: SHA256 `6e5af8d4099f464c5c1c6d908179d208221d7c96fa1f3a77d6979fb720a8fad6`.
- User-supplied submitted CHI PDF: SHA256 `9c3d8cda415745d3709200ea445bc1f4b02ca0e4fea49b92a53dfad5e132a8aa`.
- Counts, rating reconstruction, processed-file hashes and existing headline checks remain in the unchanged computational manifest.

## Reporting decision

Use the final supplement's explicit implemented-design account as the reporting source, qualified as documentation of the reused resource. Do not keep describing the phase wording as an unresolved contradiction. Do not infer unrecorded licenses, compensation amounts, individually verified payment, or broader ethics coverage.

The methods can state: "The source study documents 20 raters in non-overlapping pools: three domain-specific five-person OA pools and a separate five-person E/D/F pool comprising authors and research interns. The phase labels distinguish instruments rather than shared personnel. Its records report informed consent and compensation through existing research roles, not a separate per-response scheme. Group B's familiarity with the framework remains a limitation."

If authors later identify factual corrections, amend transparently and consider whether the CHI record needs correction through its official process. Never rewrite the already-submitted artifact or source ratings to conceal a discrepancy.

## Effect on earlier audit

This note supersedes the interpretation of phase/compensation uncertainty in the initial facct input-audit narrative, frozen decisions log and earlier review drafts. Those historical files and their hashes remain unchanged. The current draft/readiness record link to this resolution; the underlying numerical analyses do not require rerunning because no data or estimator changed.
