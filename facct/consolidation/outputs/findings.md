# Provenance consolidation

No new screening experiment or score correction.
All 48 existing byte-identical-subset operating points reproduce from an explicit equality mask.
The stored full-join tier coincides with byte equality in these files; this was tested, not assumed.
No historical scorer invocation is authenticated by this check.

| Domain | Batch | Responses | D cases | F cases | OA cases |
|---|---|---:|---:|---:|---:|
| education | byte_identical | 359 | 12 | 23 | 18 |
| education | different_text | 56 | 0 | 2 | 0 |
| education | full | 415 | 12 | 25 | 18 |
| health | byte_identical | 412 | 23 | 120 | 9 |
| health | different_text | 3 | 0 | 0 | 0 |
| health | full | 415 | 23 | 120 | 9 |
| mental_health | embedded_only | 660 | 165 | 95 | 133 |
| mental_health | full | 660 | 165 | 95 | 133 |

Complete condition/model/scenario composition is in subset_composition.csv.
Subset comparisons alter the batch and sometimes its quota; they do not isolate join error.
Missing invocation records cannot be repaired with a fresh score or deterministic join.
Mental health retains embedded scores but has no independent scorer-input string.

## Recorded truncated strings

The available scorer implementation truncates text to its first 300 characters.
The export also records text_trunc. Checking that field is additional provenance evidence,
not proof that this implementation/version generated the historical score.
- education: 415/415 recorded truncations equal the export's first 300 characters; 369/415 equal the rated text's first 300. Of the differing full-text pairs, 10 have matching recorded/rated prefixes.
- health: 415/415 recorded truncations equal the export's first 300 characters; 414/415 equal the rated text's first 300. Of the differing full-text pairs, 2 have matching recorded/rated prefixes.
