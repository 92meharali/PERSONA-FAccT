# Semantic judge work

**No API calls or API-judge results.** The API runner remains preparation only.
This compares one later-approved semantic judge with existing queues; it does not
run the deferred capability study. See [plan](plan.md) before model selection.

## Separate in-chat pilot

The author subsequently requested LLM assessment in the current chat, not new
human evaluation. [The separate amendment](chat_pilot_plan.md) records the change.
Twenty-four hash-selected mental-health responses were fully read and scored by
the assistant. All received priority 0 for this narrow anthropomorphic target;
that is neither an accuracy result nor a general-safety judgment. The remaining
636 responses had not yet been assessed in that pilot. No labels or scores were
displayed in the item view, but prior study results were visible in the conversation.

Private inputs, item-specific rationales and validation hashes are preserved in
`private/llm_judge/chat_pilot_v1/`. The assistant did not use keyword rules to
generate judgments. This is not a version-pinned API run, a fully blinded judge,
or a completed comparison; it has not been inserted into the paper.

```bash
.venv/bin/python -m facct.llm_judge.chat_pilot validate \
  --directory private/llm_judge/chat_pilot_v1
```

## Complete in-chat exploratory pass

The assistant subsequently assessed all 660 items in a separate pass, including
reassessing the pilot items. The full pass and its matched-budget calculations
are documented in [chat_full_report.md](chat_full_report.md). It is **not** a
blinded, version-pinned API comparison and is excluded from the paper's headline
evidence. The API runner remains prepared but uncalled.

```bash
.venv/bin/python -m facct.llm_judge.evaluate_chat \
  --packet private/llm_judge/followup_v1 \
  --judgments private/llm_judge/in_chat_full_v2/judgments.tsv \
  --output private/llm_judge/in_chat_full_v2/results --replicates 2000
```

## Prepare locally

From the repository root:

```bash
.venv/bin/python -m facct.llm_judge.run prepare \
  --output private/llm_judge/followup_v1
.venv/bin/python -m pytest facct/llm_judge/test_judge.py -q
```

This writes 660 blinded requests, a private source-ID mapping, input hashes and a
disabled settings template. No labels or scores enter requests. Default scope is
the entire mental-health follow-up. Optional `--tasks followup source_D source_F
source_OA` prepares 5,130 requests across the full three-domain source corpus.
Keep requests, raw API responses and rationale text private; they contain corpus
text. Do not upload them to GitHub or include them in an anonymous typesetting ZIP.

## After explicit model and budget approval

Choose the provider and exact snapshot, establish permitted transmission and
retention terms, set output limits, pricing record, decoding and conservative
per-request cost ceiling, and freeze settings. Develop the provider adapter
against that provider's current official API specification. No live adapter or
credentials are bundled; an existing CLI subscription token is not assumed usable.

An adapter is a local function `adapter(messages, settings)` returning a JSON-safe
dictionary with `model`, `response_id`, `usage`, `cost_usd`, and `output` (the raw
judge JSON or parsed object). It must enforce the declared output/cost ceiling,
disable implicit retries and not send metadata beyond the supplied messages.
Authentication belongs in the approved environment, never the settings file.

```bash
.venv/bin/python -m facct.llm_judge.run score \
  --packet private/llm_judge/followup_v1 \
  --settings private/llm_judge/approved_settings.json \
  --adapter approved_provider_adapter:judge \
  --log private/llm_judge/followup_v1/responses.jsonl
.venv/bin/python -m facct.llm_judge.evaluate \
  --packet private/llm_judge/followup_v1 \
  --log private/llm_judge/followup_v1/responses.jsonl \
  --output private/llm_judge/followup_v1/analysis --replicates 2000
```

These later commands are templates, not runnable with today's disabled settings.
The scorer resumes without repeating logged requests, reserves costs before calls,
and refuses changed inputs/settings. An in-flight marker blocks unsafe retries
after interruption. Failed outputs remain in exact-budget queues, with declared
fallback sensitivity. Do not edit raw logs to fix scores or disguise failures.

The evaluator verifies the unchanged corpus and follow-up labels, requires complete
request coverage, reconstructs original fixed baselines, and exports all budgets,
paired uncertainty, selected IDs, tie seeds and failure sensitivities. It never
modifies source annotations, earlier outputs or the manuscript. Model results
should enter the paper only after actual scoring, verification and interpretation.
The private source frame is required only to authenticate the follow-up ID mapping.
The protocol uses original corpus encoding; no silent correction is performed.

## Completion boundary

Implemented: request preparation, output validation, provider-neutral guarded
orchestration, complete-log evaluation, and synthetic unit tests. Still to do:
approved provider integration, real calls, billing reconciliation, outcome analysis,
scientific interpretation and generated manuscript table. Passing tests supplies
no empirical evidence about judge quality or human-review effectiveness.
