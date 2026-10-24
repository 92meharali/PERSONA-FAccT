# In-chat LLM assessment amendment, 24 October 2026

The author requests LLM judging here, not a new human evaluation or paid external
API calls. This is separate from the version-pinned API protocol. No provider
adapter is used, no billing or model identifier is invented, and source human
ratings remain unchanged.

Initial scope: 24 existing mental-health responses, selected by ascending SHA256
of `chat-pilot-20261024-v1|request_id` from the complete 660-request packet. Sampling
does not access labels, scores, source model or condition. Freeze the packet before
reading its items; no replacement of difficult or uneventful cases. Preserve full
prompt/response strings and assess the existing follow-up criterion using the
same 0-3 priority anchors and v1.1 capability assumptions. The assistant supplies
each priority, quoted evidence, rationale and uncertainty flag by reading the text;
no keyword rule generates these judgments.

The assistant has seen aggregate study results in this conversation. Withholding
item metadata now does not remove that exposure or make this a fully blinded,
independent, fresh-context or snapshot-reproducible model experiment. Items share
conversation context. The earlier instruction's statement about no expected
prevalence describes the API design, not this chat; no prevalence quota is imposed.

Save original item-level judgments privately and validate completeness, IDs, score
range and verbatim evidence. Never fabricate API response IDs, usage, timestamps
or model snapshots. No human-reference comparison is performed for this pilot,
and it is not inserted into the paper as a completed judge benchmark. Completion
of 24 assessments does not mean all 660 are scored. Any full-corpus extension must
preserve this record and disclose context/version differences across sessions.
