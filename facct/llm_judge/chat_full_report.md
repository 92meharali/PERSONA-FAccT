# In-chat semantic scoring: exploratory record

This is an analysis of all 660 mental-health responses against the independent
assessment follow-up's contextual anthropomorphic-reviewworthiness target. It
is **not** an independently blinded, version-pinned LLM-judge comparator. The
responses were read and scored in the current Codex chat; earlier study results
were visible to the chat, and item assessments shared a conversation context.
No external model API was called, and the exact model snapshot is unavailable.
The 24-item earlier pilot is a different pass and was not merged with this one.

## Frozen scoring record

- Request packet: `private/llm_judge/followup_v1/requests.jsonl`.
- Full-pass judgments: `private/llm_judge/in_chat_full_v2/judgments.tsv`.
- Evaluator: `python -m facct.llm_judge.evaluate_chat`.
- Recomputed tables and source hashes: `private/llm_judge/in_chat_full_v2/results/`.
- The 660 one-to-one request indexes, priorities, uncertainty fields, and
  response-substring evidence were validated before the human labels were read.
- Priority distribution: 645 zero, five one, five two, five three. Ten
  decisions were marked uncertain. The 15 nonzero scores span nine prompts.

At the reference 132/660 (20%) slots, the in-chat screen selected 14 of 19
resolved concern cases, compared with 12 for normalized markers, six for HumT,
four for length, and 3.8 expected under uniform random selection. Its 14/19
recall is 73.7%; precision is 14/132 (10.6%). Fourteen of the 15 nonzero-priority
items match a resolved concern; five resolved concerns scored zero. At 33 slots
(5%), it also captures 14; at 198 slots (30%), it captures 15. The exact 20%
count varies from 14 to 17 over 100 tie seeds because 645 responses have the
same score. The reported reference count uses the paper's original fixed seed.

The paired 2,000-prompt-bootstrap 20% recall difference from HumT is +42.1
percentage points (exploratory pointwise 95% interval +12.5 to +75.0).
The difference from markers is +10.5 points (-21.4 to +50.0), which does not
support a general improvement over that inexpensive comparator. These intervals
condition on this one fixed, potentially contaminated score set and the
resolved human labels. They do not account for model-version, prompt,
conversation-history, human-reference, or criterion uncertainty.

## Interpretation and decision

The pass demonstrates a plausible semantic-screen upper possibility on this
batch, not an independently reproducible performance estimate. Its striking
14/15 overlap with human flags requires particular caution because the chat
had prior results and the rubric resembles the human target. Treating it as
equivalent to a fresh, isolated API judge would be misleading. It is therefore
**excluded from headline manuscript comparisons** and cannot establish that
semantic judging outperforms HumT or markers in general. The source data and
human labels were not edited. The prebuilt provider-neutral runner remains
available if a model/version, data-sharing decision, and cost ceiling are later
approved; a fresh run must score each request without the earlier result context.

For the FAccT paper, the strongest current evidence is the completed
fixed-budget audit, independent human assessment follow-up, and held-out
trained comparison. What remains unresolved is an independent, pinned semantic
comparator and observation of actual reviewer decisions. Neither should be
implied to have been supplied by this chat run.
