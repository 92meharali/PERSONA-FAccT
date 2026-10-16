"""Paired comparisons on complete prompt blocks, without model-family claims."""
import itertools

import numpy as np
import pandas as pd

from .screening import labels
from .uncertainty import summarize


def run(d, config, replicates, out):
    differences, rates, scopes = [], [], []
    for domain, frame in d.groupby("domain", sort=True):
        models = sorted(frame.model.unique())
        counts = frame.groupby("cluster").model.nunique()
        complete = frame[frame.cluster.isin(counts[counts == 3].index)].copy()
        incomplete = frame[~frame.cluster.isin(complete.cluster)]
        scopes.append(dict(domain=domain, complete_prompts=complete.cluster.nunique(), complete_responses=len(complete), incomplete_prompts=incomplete.cluster.nunique(), incomplete_responses=len(incomplete)))
        for scope, g in (("complete_prompts",complete), ("incomplete_only_descriptive",incomplete), ("all_descriptive",frame)):
            if not len(g):
                continue
            yy = labels(g, config)
            for j, criterion in enumerate(config["criteria"]):
                for model in models:
                    mask = g.model.to_numpy() == model
                    rates.append(dict(domain=domain, scope=scope, criterion=criterion, model=model, n=int(mask.sum()), concerns=int(yy[mask,j].sum()), rate=yy[mask,j].mean() if mask.any() else np.nan))
        rng = np.random.default_rng(config["seed"])
        ids = np.sort(complete.cluster.unique())
        draws = rng.integers(0, len(ids), (replicates, len(ids)))
        for j, criterion in enumerate(config["criteria"]):
            complete["case"] = labels(complete, config)[:,j].astype(float)
            matrix = complete.pivot(index="cluster", columns="model", values="case").loc[ids,models].to_numpy()
            boot = matrix[draws].mean(axis=1)
            for a, b in itertools.combinations(range(3), 2):
                lo, hi, valid = summarize(boot[:,a]-boot[:,b])
                differences.append(dict(domain=domain, criterion=criterion, model_a=models[a], model_b=models[b], paired_prompts=len(ids), rate_a=matrix[:,a].mean(), rate_b=matrix[:,b].mean(), difference=matrix[:,a].mean()-matrix[:,b].mean(), lo=lo, hi=hi, valid_replicates=valid, interpretation="pointwise descriptive; not general model-family ranking"))
    pd.DataFrame(differences).to_csv(out / "tables/model_paired_differences.csv", index=False)
    pd.DataFrame(rates).to_csv(out / "tables/model_rates.csv", index=False)
    pd.DataFrame(scopes).to_csv(out / "tables/model_completeness.csv", index=False)
