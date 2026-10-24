# Proposed contribution: capability-grounded review allocation

Date: 23 October 2026. Status: research proposal, not completed evidence.
The current manuscript and its results are unchanged. No publication or submission
eligibility is certified by this proposal.

## Recommendation

Shift the main question from which tone score captures more concerns to which
documented system facts are needed to allocate review of anthropomorphic claims.
Retain the existing HumT audit as motivation and a baseline, not as proof of the
new contribution.

Proposed question: When responses imply memory or future supportive action, how
does providing verified capability and action evidence change independent review
judgments and the effectiveness of budget-constrained screening?

The potentially distinctive contribution is a controlled, independently assessed
test of the value of capability information for review allocation. It is not the
discovery that context matters, a new anthropomorphism taxonomy, or a universal
harm detector. Novelty remains a bounded literature assessment, not an exhaustive
first-ever claim.

## Why this addresses the current weakness

The current paper establishes corpus-specific operating points for one tone
metric, transparent alternatives and a specified trained screen. The new
mental-health target contains 19 positives in 13 clusters, with uncertain paired
comparisons. Capability-note version and assessor differ together. Those data
cannot identify the effect of capability information or chatbot design.

The proposed experiment introduces genuinely new observations and manipulates
information deliberately rather than reinterpreting existing labels. The unit of
evaluation becomes the prompt, response, documented system configuration, and
evidence supporting the particular claim. Unknown historical capabilities remain
unknown; no original annotations or source records are rewritten.

## Two focused targets

1. Unsupported continuity or recall: language implying access to earlier personal
   interactions when the relevant information is unavailable or unsupported.
2. Unsupported future supportive action: a promise to initiate a check-in or
   follow-up without the required capability, authorization or recorded action.

These concern mechanisms connect to DeVrio's expressions of anticipation, recall
and intention. They are not established experienced harms. A capability being
available does not prove that a particular claim is accurate or appropriate.
Memory access, factual support, consent and the particular action must be checked.
Adding a memory tool does not establish human feelings or reciprocal attachment.

## Minimal credible design

### Study 1: matched capability sensitivity

Construct new matched cases keeping the user prompt and assistant response fixed
while varying a concrete, coherent capability/evidence dossier. Include supported,
unsupported and genuinely unknown conditions. Examples include a claim about a
prior conversation with versus without an accessible supporting record, and a
future check-in with versus without an authorized scheduled action.

Include warm but noncommittal controls and claims whose assessment should not
change across dossiers. Do not select only obvious label reversals. Separate a
purposive diagnostic set from any systematically sampled or prospectively
generated set; a balanced challenge set cannot estimate deployment prevalence.
Include ordinary functional claims without relational framing as a comparison.
If the results are equally explained by generic factual support, describe the
finding as capability-grounded auditing with anthropomorphic applications rather
than claiming a mechanism unique to anthropomorphism.

Use independent human assessors under a single frozen instruction version, blind
to screening scores and the preferred hypothesis. Counterbalance case order and
avoid immediately displaying paired versions. Obtain overlapping assessments
across all conditions rather than using a third assessor only on disputes.
Separate factual support from reviewworthiness, retain uncertainty and divergence,
and do not require a label to flip because a condition changed.

Documented hypothetical configurations test judgments about vignettes. If claiming
effects in implemented chatbot designs, actually implement the configurations and
retain memory, authorization and tool-action evidence. Do not blur these designs.
Pilot for feasibility and event support before determining a defensible final
sample size and interval precision; no power or completion claim is made here.

### Study 2: value of information for screening

Compare HumT, markers, length and matched random selection with a strong semantic
screen using prompt plus response. Compare that SAME semantic screen with the
addition of verified configuration information, then claim-specific evidence.
This isolates the information contribution better than comparing a weak tone
metric with an unrelated powerful contextual model.
Also include a simple explicit-claim/capability consistency rule. If that rule
fully explains the gains, do not present a complex contextual evaluator as a new
technical achievement. Claim only the smallest adequate information package among
those tested, and only under prespecified adequacy margins; an inconclusive
difference from full evidence does not establish sufficiency.

Mask selected metadata fields to measure their contribution and include an
irrelevant-information control. Unknown information should remain unknown, not be
silently interpreted as a capability being absent. A richer evaluator may still
perform poorly; report that result without redefining the targets.

Freeze prompts, thresholds, budgets and primary contrasts before held-out results.
Keep all versions of a base scenario in the same training/test partition and
bootstrap cluster. Human target labels are never screening inputs for those same
cases. Report fixed-budget comparisons at 5%, 10%, 20% and 30%, with an explicit
reference budget, tie rules, paired uncertainty and undefined-cell behavior.

### Outcomes

- Changes and stability in independent judgments across capability conditions.
- Recall, precision and missed concerns at exactly matched review counts.
- Review slots spent on cases outside the specified target, without calling those
  responses universally safe or the review effort necessarily wasted.
- Whether correct system information improves allocation beyond semantic text
  understanding, and which fields contribute to that improvement.
- Sensitivity to unavailable information, prompt family and context.
- Metadata acquisition and scoring costs; item budgets are not measured reviewer
  time, and offline selection does not establish actual harm reduction.

## What would constitute new scholarly value

1. An independently assessed resource separating supported anthropomorphic
   implications from unsupported and indeterminate ones under explicit system
   configurations, including invariant controls.
2. Evidence estimating the value and limitations of capability information for a
   concrete constrained review procedure, beyond a strong text-only comparator.
3. A tested specification of what an operator must document for this particular
   audit to be interpretable, including what cannot be concluded when records are
   missing. A documentation template alone is not independent validation.

A response-only score remaining unchanged on identical text is mathematically
obvious. Do not present that observation as a new theorem or a successful result.
The nontrivial question is whether independently credible changes in review need
are captured by richer screens without introducing excessive false flags, and at
what information cost. If only deliberately obvious pairs show differences, report
a diagnostic limitation rather than general practical effectiveness.

## Relationship to existing studies

- CHI PERSONA: relationship of H/E/D/F to overall appropriateness on an existing
  corpus. The proposed study instead isolates capability information and review
  allocation using new cases and judgments; shared theory/data still require
  disclosure and venue-specific eligibility confirmation.
- Current FAccT draft: comparative queues on fixed responses and source/contextual
  criteria. Preserve these as baseline evidence, not evidence that the proposed
  manipulation has already been tested.
- Professor's broader design question: capability availability is one concrete
  design dimension. Scripted versus open-ended generation is a separate factor;
  do not infer its effect from capability contrasts. Adding both full factorials
  immediately would substantially expand scope.

## Primary-source novelty checks

- DeVrio et al., CHI 2025, provide a taxonomy including intention and recall, and
  explicitly distinguish categorizing expressions from studying their harms:
  https://arxiv.org/html/2502.09870v1
- AnthroBench, ICLR 2026, evaluates 14 multi-turn anthropomorphic behaviors and
  validates links to anthropomorphic perceptions in a human study. General
  anthropomorphism evaluation across design choices is not new:
  https://proceedings.iclr.cc/paper_files/paper/2026/hash/fccb2556dbe783422a27f2b71e5c47da-Abstract-Conference.html
- NOPE Evals' primary project documentation already covers capability honesty,
  memory/continuity limits and deployment-context variants. It is an existing
  evaluation project, not evidence that our proposed paired allocation experiment
  is unprecedented:
  https://evals.nope.net/

See the companion prior-art memo for additional closest-work checks. These sources
motivate narrowing the claim to tested information requirements for allocation,
not claiming the first context-aware anthropomorphism evaluation.

## Decision gate

Proceed to a small protocol/pilot only if new independent assessment and credible
capability dossiers can be obtained. Resolve ethics scope and assessor provenance
before collection. If the additional evidence cannot be gathered, retain the
current honest audit contribution and present this as future work; reframing alone
does not upgrade the existing evidence or guarantee acceptance.
