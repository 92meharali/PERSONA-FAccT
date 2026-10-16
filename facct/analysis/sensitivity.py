"""Predeclared criterion, context, tie, provenance and cost sensitivity."""
import itertools

import numpy as np
import pandas as pd

from .screening import METRICS, POLICIES, capacity, evaluate, features, label, labels, order_scores, tie_keys


def point_rows(d, config, Y=None):
    values = labels(d, config) if Y is None else Y
    rows = evaluate(features(d), values, d.domain.to_numpy(), d.cluster.to_numpy(), tie_keys(d.id, config["seed"]), config, d.domain.nunique() > 1)
    return [dict(criterion=c, policy=p, budget=b, **dict(zip(METRICS, vals))) for c, p, b, vals in rows]


def run(d, r, config, out):
    thresholds, consensus, individual, subgroups, ties, overlaps, continuous, join = [], [], [], [], [], [], [], []
    reference = dict(config, budgets=[config["reference_budget"]])
    for domain, frame in d.groupby("domain", sort=True):
        for column, grid in config["sensitivity"].items():
            for op, threshold in grid:
                name = f"{column}{op}{threshold}"
                cfg = dict(reference, criteria={name: dict(column=column, operator=op, threshold=threshold)})
                thresholds.extend(dict(domain=domain, **row) for row in point_rows(frame, cfg))
        for name, rule in config["criteria"].items():
            column = rule["column"] + "_score"
            ratings = r.loc[(r.domain == domain) & r[column].notna()].copy()
            ratings["vote"] = label(ratings[column].to_numpy(), rule["operator"], rule["threshold"])
            votes = ratings.groupby("annotation_item_id").vote.sum().reindex(frame.annotation_item_id).to_numpy()
            cfg = dict(reference, criteria={name: rule})
            for cutoff in (3, 5):
                consensus.extend(dict(domain=domain, votes_required=cutoff, **row) for row in point_rows(frame, cfg, (votes >= cutoff)[:, None]))
            for annotator, rr in ratings.groupby("annotator_id"):
                y = rr.set_index("annotation_item_id").vote.reindex(frame.annotation_item_id).to_numpy()
                individual.extend(dict(domain=domain, anonymized_rater=annotator, **row) for row in point_rows(frame, cfg, y[:, None]))
        for field in ("condition", "scenario_type", "model"):
            for group, g in frame.groupby(field):
                subgroups.extend(dict(domain=domain, grouping=field, group=group, uncertainty="descriptive only; no subgroup ordering claim", **row) for row in point_rows(g, reference))
        X, Y = features(frame), labels(frame, config)
        k = capacity(len(frame), config["reference_budget"])
        for seed in range(config["seed"], config["seed"] + 100):
            for j, policy in enumerate(POLICIES):
                idx = order_scores(X[:, j], tie_keys(frame.id, seed))[:k]
                for c, name in enumerate(config["criteria"]):
                    p = int(Y[:, c].sum())
                    ties.append(dict(domain=domain, criterion=name, policy=policy, seed=seed, selected=k, caught=int(Y[idx, c].sum()), recall=Y[idx, c].sum()/p if p else np.nan))
        verified = frame[frame.humt_join_tier.isin(["embedded", "full"])]
        join.extend(dict(domain=domain, scope="embedded_or_full_text_only", excluded=len(frame)-len(verified), **row) for row in point_rows(verified, reference))
    for domain, frame in list(d.groupby("domain", sort=True)) + [("pooled", d)]:
        y = labels(frame, config)
        for bits in itertools.product((False, True), repeat=3):
            mask = (y == bits).all(axis=1)
            overlaps.append(dict(domain=domain, D_ge3=bits[0], F_lt4=bits[1], OA_lt4=bits[2], n=int(mask.sum()), proportion=float(mask.mean()), prompt_clusters=frame.loc[mask, "cluster"].nunique()))
        for a, b in itertools.combinations(["H", "E", "D", "F", "OA"], 2):
            continuous.append(dict(domain=domain, a=a, b=b, pearson=frame[a].corr(frame[b]), spearman=frame[a].corr(frame[b], method="spearman"), n=len(frame)))
    for name, rows in [("threshold_sensitivity",thresholds), ("consensus_sensitivity",consensus), ("rater_sensitivity",individual), ("context_sensitivity",subgroups), ("tie_sensitivity",ties), ("criterion_intersections",overlaps), ("continuous_relationships",continuous), ("join_sensitivity",join)]:
        pd.DataFrame(rows).to_csv(out / "tables" / f"{name}.csv", index=False)


def scenarios(results, out):
    rows = []
    base = results[(results.domain != "pooled") & (results.budget == .2)]
    for _, r in base.iterrows():
        for minutes in (1, 3, 5):
            for ratio in (1, 5, 10):
                rows.append(dict(domain=r.domain, criterion=r.criterion, policy=r.policy, minutes_per_response_assumed=minutes,
                                 missed_to_unnecessary_cost_ratio_assumed=ratio, review_minutes=r.selected*minutes,
                                 hypothetical_cost=ratio*r.missed + (r.selected-r.caught), note="no empirical cost calibration"))
    pd.DataFrame(rows).to_csv(out / "tables/cost_scenarios.csv", index=False)
    mixtures = []
    for (criterion, policy), g in base.groupby(["criterion", "policy"]):
        for mix in ("observed", "equal_domain"):
            weights = g.n.to_numpy() / g.n.sum() if mix == "observed" else np.repeat(1/len(g), len(g))
            prevalence = np.sum(weights * g.concerns/g.n)
            detected = np.sum(weights * g.caught/g.n)
            reviewed = np.sum(weights * g.selected/g.n)
            mixtures.append(dict(criterion=criterion, policy=policy, hypothetical_mixture=mix,
                                 prevalence=prevalence, recall=detected/prevalence if prevalence else np.nan,
                                 precision=detected/reviewed, review_fraction=reviewed,
                                 note="domain-wise policies then reweight; not a new global ranking"))
    pd.DataFrame(mixtures).to_csv(out / "tables/mixture_scenarios.csv", index=False)
