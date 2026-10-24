# Evidence audit for the current FAccT draft

This note separates work completed now from evidence still missing. It does not
change the manuscript's frozen source labels or claim that a chat-run score is
an independent LLM benchmark.

## Completed

- Assessed all 660 mental-health prompt-response pairs in this chat under the
  narrow contextual-anthropomorphism screen; saved 660 individual priorities,
  uncertainty flags, rationales, and exact positive evidence substrings.
- Verified full coverage and mapped the frozen decisions to the resolved human
  target only after scoring. Recomputed exact-budget comparison at 5%, 10%, 20%,
  and 30%, with 2,000 paired prompt-cluster bootstrap replicates.
- Preserved the earlier 24-item pilot as a distinct run and made no paid API
  calls or alterations to human labels or source responses.
- Recorded all methodological limitations of this chat pass in
  `facct/llm_judge/chat_full_report.md`. It is not promoted into the paper's
  headline evidence.
- Rechecked the FAccT 2027 guide: up to 14 single-column main-content pages;
  one optional page for endmatter statements; references and appendices follow
  separately. The existing rendered source has 14 main pages and one endmatter
  page. A required generative-AI-use statement is already in the manuscript.

## Highest-value remaining evidence

1. **Independent semantic comparator.** A fresh run of the prepared runner
   with a named/versioned model, isolated requests, documented prompt and
   permitted data transfer would directly test a realistic modern alternative.
   The in-chat pass cannot substitute for this because the chat saw prior
   results, shared context across items, and lacks a pinned model snapshot.
2. **Actual review decisions.** The current endpoint is selection against
   concern judgments, not a study showing what reviewers find, escalate or
   resolve after receiving the queue. This limits an effectiveness claim.
3. **Criterion validity beyond one rating population.** The resolved human
   follow-up has only 19 positive cases and one domain. It supports a narrow
   contextual target, not all anthropomorphic concerns or experienced harm.
4. **Chatbot design variation.** The present paper varies the review screen
   and budget, not matched persona, memory or boundedness settings. Design
   effects remain a prospective study and must not be inferred from model or
   natural/adversarial labels.

Given the remaining time, the sound submission move is to preserve the
paper's narrower decision-audit contribution and its complete numeric record,
not inflate the claims with an unreplicable comparator or an unevaluated
intervention. The exploratory chat score can guide a future isolated run and
the report makes that next experiment concrete.
