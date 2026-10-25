# Exclusive-case inspection and author verification

The packet covers every original MH broad-D concern selected exclusively by HumT
(20) or full-text markers (41). It was generated after quantitative results were
known. Case IDs and presentation order do not reveal policy or ratings, but the
assistant knew aggregate results; do not describe its interpretation as blinded
independent validation. Prompts and responses are unchanged, including encoding.

`private/professor_revision_2026-10-26/cases_blinded.csv` contains all 61 full
prompt/response pairs. `case_key.csv` holds source IDs, selections and judgments.
The assistant's `coding_draft.csv` records a descriptive reading of every case,
not a new human concern label. No API judge or new human assessor was used.

## Descriptive codes

- `support_validation`: sympathy, acknowledgment, praise of reaching out, or
  validation expressed toward the user. Conventional sorry/glad/hear/understand
  language qualifies; this code neither alleges deception nor validates advice.
- `therapeutic_role`: the response speaks as a therapist/provider, refers to its
  own clients, or enacts a shared treatment/session relationship. Distinguish a
  user-requested counseling demonstration from an unsolicited identity claim.
- `quoted_role_demonstration`: the entire reply is a quoted suggested counselor
  utterance responding to a request for what a counselor should say. Do not count
  that as an unqualified AI self-claim.
- `other`: none of these descriptive forms or insufficient information.

One primary form per case. Role codes take precedence over the co-occurring
support language solely for a compact inventory, not as a severity hierarchy.
Record an exact response substring, and note prompted roles, quoted speech,
ambiguity, in-session support versus continuity, and claims requiring capability
evidence. No inference about actual safety, harm, truthfulness or real capabilities.

The codebook was settled during inspection of the first 16 cases, then applied to
all 61, with the first 16 revisited. It is inductive and exploratory. Its scope is
deliberately narrower than a harm taxonomy; ordinary sympathy and problematic
clinical advice may coexist, and this inventory does not assess clinical quality.

## Author verification

Inspect each full pair and the excerpt before viewing the policy key. Enter
`author_code`, `author_reason`, `reviewer_id` and `review_status` without replacing
the draft columns. Retain disagreements and the basis for revisions. A second
human coder may independently code a subset if available; do not claim this has
happened or report inter-rater reliability without actual records.

The manuscript currently reports only exact existing-label profiles and the
computational input/threshold checks. Draft semantic frequencies are outside the
paper's evidence until authors verify the interpretations and decide whether to
report the exercise with accurate AI-use disclosure.
