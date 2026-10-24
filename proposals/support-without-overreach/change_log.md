# Proposal revision record

## 22 October 2026

- Preserved the 21 October proposal, Word document and builder under `history/2026-10-21/`.
- Changed the proposal from an auditor-first study to a design-first experiment followed by an auditor evaluation.
- Made the framing by expressiveness comparison central, rather than an optional secondary extension.
- Rewrote the three RQs to cover design effects, PERSONA evaluation and design-specific intervention tradeoffs.
- Checked GitHub CHI main at `94d8016cf5b94822fe453f7c561d24571b864d18`; distinguished the PERSONA framework from chatbot persona framing and simulated-user personas.
- Specified new validation for history-aware E/D/F and separate OA judgments. Did not claim the original single-turn framework already validates this use.
- Used DeVrio for expression categories following the author's clarification. Did not substitute it for a harm taxonomy or claim access to Fatima's taxonomy.
- Retained two proposed failure criteria with benign controls and capability-dependent interpretation; flagged D/B conceptual overlap.
- Added constraint compliance, same substantive rules, same disclosure, compute matching, and preservation of the design condition during auditing.
- Added a staged execution plan, proposed pilot workload, factorial contrasts, multiple-testing planning, dependencies and the next-meeting package.
- Left all earlier manuscript, source data and analysis files unchanged. No new experiments, new annotation, commit or push.

## Clarification of meeting numbers

The meeting summary juxtaposed results from two distinct domains and endpoints. The counts do not imply an arithmetic error in the analyses; the shortened wording omitted the distinction.

| Result | Population and endpoint | Source |
| --- | --- | --- |
| HumT 6, markers 12, length 4, random expected 3.8 | Mental-health follow-up; 19 resolved concern cases across 660 responses; 132 review slots | `facct/paper/overleaf/tables/annotation_coverage.tex` |
| HumT 8, markers 4 | General-health natural prompts; 74 fit concerns; selections projected from the full general-health queue of 83 slots, not separate natural-prompt quotas | `facct/paper/overleaf/tables/common_queue_conditions.tex`, `common_queue_slots.tex`, and `main.tex` |

Suggested corrected sentence: "In the mental-health follow-up, HumT selected 6 of 19 resolved concerns, compared with 12 for markers. Separately, among 74 general-health fit concerns in natural prompts, HumT selected 8 and markers 4; that contrast was uncertain."

The general-health natural-prompt recall contrast is +5.4 percentage points for HumT, with the reported interval [-1.3, +13.0]. These are prior exploratory results, not findings from the new design study. The archive's denominator and uncertainty qualifications remain applicable.
