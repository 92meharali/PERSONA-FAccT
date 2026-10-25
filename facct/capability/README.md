# Capability-grounded review allocation

## Current status: future work only, updated 26 October 2026

The author chose **no new experiments for this deadline**, superseding the
October 23 capability-study direction. This folder is retained as future-work
preparation, not the current paper's empirical contribution or a study promised
before submission. Do not start recruitment, annotation, capability experiments,
or semantic-judge API runs under the earlier implementation approval.

The active paper is restored to *When Tone Scores Allocate Attention: Auditing
HumT-Based Review Prioritization*: RQ1 enrichment, RQ2 comparative allocation,
RQ3 incremental benefit, and RQ4 shared-queue coverage. Its existing 1,490-response audit and
660-response assessment follow-up remain unchanged. No new capability-conditioned
human judgments or semantic-screen results have been collected. Passing synthetic
software tests does not establish an empirical result.

The October 23 prospective manuscript remains in Git revision `a9d1800`;
it is not the [active source](../paper/overleaf/main.tex).
The current [layout audit](../paper/qa/2026-10-26/layout_report.json) records 14
content pages, one endmatter, two references and 14 appendix pages (31 total).
See the [latest package](../releases/PERSONA_FAccT_Overleaf_2026-10-26_professor.zip).
These production facts do not supply evidence for the proposed capability study.
The protocol and commands below record the retained October 23
preparation. They are not instructions to execute now. Any later study requires
renewed authorization, a frozen specification, verified evidence, recruitment,
and an institutional determination explicitly covering that study. Meanwhile,
existing-audit assessor reporting and CHI-eligibility gates remain author tasks.

## Historical preparation: 23 October 2026

Status at preparation: prospective implementation, **not completed research**.

## Materials

- [Protocol](study/protocol.md): targets, assignment, comparisons and decision gates.
- [Assessor guide](study/assessor_guide.md): support and reviewworthiness are separate.
- [Evidence dossier](study/evidence_dossier_template.md): record facts, not label answers.
- [Screening prompts](study/screening_prompts.md): frozen semantic information ablations.
- [Readiness](study/readiness.md): approval, recruitment and evidence checks still needed.
- [Proposal](../submission/proposed_new_contribution_2026-10-23.md) and
  [prior-art check](../submission/capability_contribution_prior_art_2026-10-23.md).

## Preparation already performed

`preparation/relevance_sample_2026-10-23/` contains 60 existing mental-health
responses from 60 prompts, chosen deterministically without inspecting ratings or
screen scores. `candidates.csv` exposes only neutral IDs and prompt/response text;
`source_map.csv` is for internal provenance, not assessors. The manifest records
source/output/code hashes, seed and software. This is an unenriched relevance
sample, not the proposed purposive 60-base-case diagnostic pilot. It may contain
few relevant claims. Do not substitute it for new independent judgments or claim
that it represents deployment prevalence. Do not give it to assessors until the
protocol, evidence dossiers, consent and coverage checks are complete.

Reproduce into a fresh directory from the repository root:

```bash
.venv/bin/python -m facct.capability.prepare --output facct/capability/preparation/reproduction
.venv/bin/python -m pytest facct/capability/test_capability.py -q
```

Preparation takes approximately one second locally; unit tests approximately
three seconds. No API call, new approval, recruitment or human response is generated.

## Analysis scaffold

`evaluate.py` accepts supplied cases, scores and hashed evidence artifacts. It
checks fixed text within base cases, matched conditions, full policy coverage,
finite scores, capability evidence hashes and frozen text-only predictions. It
uses exact floor budgets, policy-paired ties, analytical random expectations,
tie-aware sklearn AP/AUC and paired cluster resampling. It does not fit classifiers,
run a semantic judge, infer human labels or authenticate an ethics approval.

Cases CSV columns:

```text
instance_id,base_id,cluster_id,condition,target_family,prompt,response,review_label,evidence_ref,evidence_sha256
```

Use `memory` for the primary family; `future_action` for the secondary. Every base
has at least two conditions and identical prompt/response text. `cluster_id`
groups related scenarios and all their variants. `review_label` is `0`, `1`, or
`U`, derived under the documented human assessment rule, never a model's own label.
Evidence references resolve under a separately supplied evidence root; keep
identifying human records outside public artifacts.

Scores CSV columns: `instance_id,policy,score`, with higher values prioritizing
review. Required comparison policies are `semantic_text` and
`semantic_full_evidence`; use the same frozen judge and rubric. Additional names
may include `semantic_summary`, `semantic_missing`, `semantic_irrelevant`,
`claim_capability_rule`, `high_H`, `markers`, and `length`. No ground-truth oracle
is supplied. Every policy must score the same full instance set. Record actual
judgment costs and split history, even for zero-shot policies.

The run-record JSON requires nonempty `protocol_version`, `protocol_freeze_record`,
`ethics_scope_record`, `assessment_provenance_record`, `judge_model_version`,
`judge_prompt_hashes`, `evidence_cost_record`, `screening_cost_record`, and
`split_record`. These are author-supplied provenance references, not machine-verified
permission. Do not insert fictitious references just to satisfy validation.

After real evidence and assessments exist, run:

```bash
.venv/bin/python -m facct.capability.evaluate \
  --cases /absolute/path/to/cases.csv \
  --scores /absolute/path/to/scores.csv \
  --evidence-root /absolute/path/to/evidence \
  --run-record /absolute/path/to/run_record.json \
  --output facct/capability/results/final --replicates 2000
```

This command is deliberately not executable from current study inputs: no valid
new case labels or semantic scores have been collected. Runtime at final study
size is unmeasured. Test-only synthetic fixtures are not included in result files.

## Interpretation and remaining implementation

The primary contrast is full-evidence minus text-only semantic recall at 20% in
the mixed memory diagnostic queue; configuration-specific queues and other
families are exploratory. Cluster resampling re-ranks each drawn batch. Unknown
labels stay in every queue: output includes unknown counts, definite-case recall,
precision and recall identification bounds. AP/AUC are explicitly definite-subset
diagnostics. Primary-contrast output with unknown labels is marked descriptive,
not a complete-label confirmatory finding. Undefined replicates are counted.
The interval conditions on labels; it is not uncertainty over rater populations.

`pair_changes.csv` reports all condition-pair label transitions, including stable
and unresolved pairs, without assigning desired directions. Within-condition
queues share base-case tie keys; mixed queues use label-blind condition-aware
keys. The same tie scheme is used across policies in every bootstrap draw.

This is an initial tested analysis scaffold, not the entire final analysis plan.
Still pending are a verified capability harness, candidate dossier construction,
balanced assessor assignment, frozen rubric and consensus rule, rater uncertainty,
rater-level change/stability inference, cost measurement, full sensitivity reports,
judge API integration, adequate final sample sizing and any adequacy-margin test.
No smallest-package or safety-effectiveness conclusion is currently supported.
