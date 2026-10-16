# Response to the Computational-Draft Critique

Updated 2 October 2026. Actual revisions and remaining limits, not a promise of acceptance or a chair decision.

**Later amendment:** the trained comparison and complete policy-cell reporting are now implemented. See [the four-comment response](conditional_response.md). The first-amendment results below remain intact; the current manuscript incorporates both stages.

| Concern | Implemented response | Boundary |
|---|---|---|
| Hypothetical workflow lacks grounding | Added verified triage and expert-deferral literature, contrasted with our fixed-batch simulation | Supports allocation research, not real HumT adoption |
| Cue-aligned marker comparison | Reported fit/OA comparisons, selected-set complementarity, and one fixed equal-weight rank fusion | No universal marker superiority or outcome-tuned weights |
| Abstract overstates primary evidence | States two adjusted comparisons include zero and the third only narrowly excludes it; education marker difference uncertain | Original primary family unchanged |
| Recall ignores capacity ceiling | Added oracle ceiling, achieved fraction, and lift alongside ordinary recall | Oracle is an unavailable-label upper bound |
| HumT may find different cases | Intersections and exclusive case counts at all four budgets; fusion at the same budget | Larger union is not a same-capacity improvement |
| Reliability/cutoff behavior missing | All source D/F/OA/E ICC and alpha estimates, reconstructed ICC points, mean distributions, cutoff neighborhoods, trigger votes | Source CIs are response-bootstrap; alpha not independently re-estimated; agreement is not validity |
| Scored text uncertain | Replayed joins, verified H/source/tier, hashed text pairs; same-batch export-text lexical scores and fixed-capacity subset checks | 59 strings differ after normalization; scorer invocations and join correctness are not authenticated |
| Workload differences lack paired inference | Added direct differences with 2,000 paired prompt-cluster draws | Exploratory intervals; comparator point rankings are not reliable differences by themselves |
| Multiplicity and sparsity | Explicit exploratory labels, sparse flags, finite counts; retained primary family | No post-hoc switch to the most favorable primary outcome |
| Unevaluated card | Reduced main-text role to supporting documentation; example in appendix | No fabricated external validation or participant evidence |
| Overlap framing | Concise statement of shared inputs and new allocation evidence | Reuse is not automatic duplication; different RQ is not automatic clearance |
| Presentation | Retitled Evaluating, split figures, moved diagnostics to appendix, removed main-text GLM/GPT example | Original outputs retained |
| Intern non-participation | Added assurance that declining/withdrawal would not affect role, pay, supervision, or evaluation | Author confirmed the consent/recruitment records explicitly state this in the current conversation; private documents not independently inspected |

## New computational findings

See generated [findings](../revision/outputs/findings.md), [paired comparisons](../revision/outputs/paired_comparisons.csv), and [complementarity](../revision/outputs/complementarity.csv). Source data and original outputs remain unchanged. The revision plan was written after the first results and before these additions ran.

## Remaining boundaries

- The first amendment used untuned label-free fusion. A later, separately specified logistic comparison now supplies prompt-group-held-out evaluation, refitted uncertainty, and training-label accounting. No LLM judge was added. Its nine incremental-recall intervals all include zero, so distinct selected cases are not presented as proven combined-screen improvement.
- External evaluation remains deferred at the author's request; internal experts and AI agents are not independent participants.
- The cause and historical scorer inputs of non-identical text pairs remain unauthenticated. Representation checks narrow, but do not erase, this uncertainty.
- The author handles chair contact. Policies concern identical/substantially similar work, not a blanket ban on shared datasets; submission eligibility is not self-certified here.
- Full-project compilation and page count remain unverified. The latest native single-document compiler loaded an ACM class but could not access `tables/numbers.tex`; the actual table file is included and verified in the ZIP. Use a complete multi-file Overleaf build.
