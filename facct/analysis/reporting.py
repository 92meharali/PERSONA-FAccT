"""Generate numerical cards and supporting interpretation from computed tables."""
import pandas as pd


def write(table, out):
    base = table[(table.policy=="high_H") & (table.budget==.2) & (table.domain!="pooled")]
    card = ["# Proposed audit-use card v1.0 (not externally evaluated)", "",
            "## Intended use and owner", "",
            "A model-evaluation lead proposes which responses in a fixed batch receive manual review. HumT measures linguistic human-like tone, not harm probability. Selection creates an opportunity for a qualified reviewer to inspect the original prompt/response; achieved detection and successful escalation have not been measured. Non-selection means unreviewed, never cleared or safe.", "",
            "## Rule and criterion provenance", "",
            "Rank descending H; select floor(0.20*n). SHA256(seed|domain:item ID) breaks ties deterministically, without exceeding capacity. Seed 20261002. No human ratings enter the ranking. D >= 3, F < 4 and OA < 4 use existing five-rater means; D/E/F were supplied by framework-familiar authors/interns, OA by separate domain pools. D >= 3 includes simulated affect/understanding, not only serious relationship claims. Thresholds are contestable review triggers. Ratings are not established harm outcomes.", "",
            "## Reference-budget evidence", "",
            "| Domain | Criterion | Review slots | Caught / total concerns | Precision | Recall (95% CI) | Unreviewed concerns | Concern rate among unreviewed |", "|---|---|---:|---:|---:|---|---:|---:|"]
    for r in base.itertuples():
        card.append(f"| {r.domain} | {r.criterion} | {int(r.selected)}/{int(r.n)} | {int(r.caught)}/{int(r.concerns)} | {r.precision:.3f} | {r.recall:.3f} [{r.recall_lo:.3f}, {r.recall_hi:.3f}] | {int(r.missed)} | {r.unselected_prevalence:.3f} |")
    card += ["", "Matched uniform-random expected recall is 0.20 here. Compare paired differences and all simple policies in screening.csv, not just this card. The marker baseline is competitive and sometimes substantially better for D; lexical overlap with D's rubric limits interpretation as independent risk detection. Intervals above are pointwise 95% from 2,000 paired prompt-cluster resamples; the primary three-comparison family has wider adjusted intervals in results.md.", "",
             "## Unsupported inferences", "",
             "No safety clearance, experienced deception, reliance change, causal benefit, universal model ranking or demonstrated audit effectiveness. Domain, source and rater distributions vary together. Education D and health OA have only seven concern-bearing prompt clusters each. Prefix/fuzzy joins, thresholds and rater aggregation are separately examined. Different review times could change comparisons based on equal response counts.", "",
             "## Proposed contestation and escalation", "",
             "The evaluation lead owns the criterion/version, not the tone metric author. A reviewer sees original text, source identifier, policy rationale, criterion definition and the possibility of unrelated concerns. A reviewer, domain specialist or affected stakeholder may challenge a criterion, selected case or non-selection through a logged request. A separate domain reviewer examines the rationale; disagreements are retained. Escalation authority, response time and appeal contact are institution-specific placeholders, not established procedures. Version changes preserve the prior results and trigger re-evaluation of all affected cases. Affected-user involvement must be designed rather than assumed.", "",
             "The card is a design proposal. Whether people interpret it correctly and can use the challenge procedure remains pending human evaluation. Do not use non-selection to block complaints or urgent escalation."]
    (out / "reports/audit_use_card.md").write_text("\n".join(card)+"\n")
    thresholds = pd.read_csv(out/"tables/threshold_sensitivity.csv")
    consensus = pd.read_csv(out/"tables/consensus_sensitivity.csv")
    joins = pd.read_csv(out/"tables/join_sensitivity.csv")
    ties = pd.read_csv(out/"tables/tie_sensitivity.csv")
    models = pd.read_csv(out/"tables/model_paired_differences.csv")
    text = ["# Supporting sensitivity and workload findings", "", "All sensitivities are exploratory and were specified before this pipeline's final run, on already explored data. Unless stated otherwise, sensitivity tables give point estimates without bootstrap intervals; do not treat their ordering as robust significance.", "", "## Stronger D trigger at the same 20% capacity", ""]
    for r in thresholds[(thresholds.policy=="high_H")&(thresholds.criterion=="D>=4")].itertuples():
        text.append(f"- {r.domain}: {int(r.concerns)} cases in {int(r.concern_clusters)} concern-bearing prompts, {int(r.caught)} selected, recall {r.recall:.3f}. Sparse strong-trigger cases prevent a confident comparative claim.")
    text += ["", "This shows why D >= 3 enrichment must not be generalized to every severity threshold. Zero captured cases in a small severe-label cell is reported, not evidence that all severe cases are missed in deployment.", "", "## Rater-consensus changes (D)", ""]
    for r in consensus[(consensus.policy=="high_H")&(consensus.criterion=="D_ge3")].itertuples():
        text.append(f"- {r.domain}, at least {r.votes_required}/5 votes: {int(r.caught)}/{int(r.concerns)} selected concern cases; recall {r.recall:.3f}.")
    text += ["", "## Full-text/embedded join sensitivity (D)", ""]
    for r in joins[(joins.policy=="high_H")&(joins.criterion=="D_ge3")].itertuples():
        text.append(f"- {r.domain}: exclude {r.excluded} prefix/fuzzy rows for this sensitivity only; {int(r.selected)}/{int(r.n)} reviewed; {int(r.caught)}/{int(r.concerns)} concerns selected, recall {r.recall:.3f}.")
    text += ["", "The main analysis keeps all released rows. Exact-text joins are not independently authenticated IDs, and this sensitivity changes the batch rather than proving excluded joins incorrect.", "", "## Tie sensitivity", ""]
    for (domain,criterion,policy), g in ties.groupby(["domain","criterion","policy"]):
        if g.caught.min()!=g.caught.max():
            text.append(f"- {domain}, {criterion}, {policy}: caught counts range {g.caught.min()}-{g.caught.max()} across 100 seeded tie resolutions.")
    text += ["", "Cells not listed above had identical caught counts across the 100 tested seeds; this is not an exhaustive enumeration of all possible ties.", "", "## Review workload to reach 80% of D-trigger cases", "", "Fractions below describe this corpus with its known labels; they are retrospective evaluation, not a deployable calibrated stopping rule.", ""]
    for r in table[(table.domain!="pooled")&(table.criterion=="D_ge3")&(table.budget==.2)].itertuples():
        text.append(f"- {r.domain}, {r.policy}: {r.workload_80:.3f} of batch [{r.workload_80_lo:.3f}, {r.workload_80_hi:.3f}] pointwise 95%. Random is expected order-statistic workload, not a guaranteed realized requirement.")
    text += ["", "## Model ordering is criterion-dependent but mostly uncertain", "", "Use model_rates.csv and paired intervals, not rankings inferred from separate means. The exploratory general-health GLM versus GPT comparison illustrates the distinction:", ""]
    for r in models[(models.domain=="health")&(models.model_a=="glm")&(models.model_b=="gpt_5_6")].itertuples():
        text.append(f"- {r.criterion}: concern-rate difference GLM minus GPT = {r.difference:+.3f} [{r.lo:+.3f}, {r.hi:+.3f}], {r.paired_prompts} complete prompts.")
    text += ["", "An apparent rate-order reversal for F is not strong evidence of a stable reversal when its interval spans zero. Mental-health comparisons are bounded to these endpoints and prompts. Incomplete sets are separately labeled, never silently mixed into pairings.", "", "## Degenerate resamples", ""]
    for r in base.itertuples():
        text.append(f"- {r.domain}, {r.criterion}: {int(r.recall_valid)}/2000 finite recall replicates. Undefined zero-positive draws remain missing; intervals are conditional on finite draws.")
    text += ["", "## Criterion overlap and continuous structure", "", "criterion_intersections.csv enumerates all eight intersections, including no-trigger responses. continuous_relationships.csv includes E as well as H/D/F/OA. Paired criterion recall differences are in criterion_recall_differences.csv. Different prevalence and cut points can generate low overlap; these tables do not by themselves establish normative disagreement."]
    (out / "reports/sensitivity_findings.md").write_text("\n".join(text)+"\n")
