"""Systematic illustrative sample; not AI coding or human evidence."""
import hashlib

import numpy as np
import pandas as pd

from .screening import POLICIES, capacity, features, labels, order_scores, tie_keys


def run(d, config, out):
    strata = []
    for domain, g in d.groupby("domain", sort=True):
        X, Y = features(g), labels(g, config)
        k = capacity(len(g), config["reference_budget"])
        for i, policy in enumerate(POLICIES):
            selected = np.zeros(len(g), dtype=bool)
            selected[order_scores(X[:,i], tie_keys(g.id, config["seed"]))[:k]] = True
            for j, criterion in enumerate(config["criteria"]):
                for status, mask in (("selected_concern", selected & Y[:,j]), ("unreviewed_concern", ~selected & Y[:,j]), ("selected_outside_criterion", selected & ~Y[:,j])):
                    choices = g.iloc[np.flatnonzero(mask)].copy()
                    choices["sample_key"] = tie_keys(choices.id, config["seed"] + 901)
                    chosen = choices.sort_values("sample_key").head(1)
                    if not len(chosen):
                        strata.append(dict(domain=domain, policy=policy, criterion=criterion, status=status, available=0, id=""))
                    else:
                        strata.append(dict(domain=domain, policy=policy, criterion=criterion, status=status, available=len(choices), id=chosen.iloc[0].id))
    registry = pd.DataFrame(strata)
    registry.to_csv(out / "tables/case_sampling_register.csv", index=False)
    sample = d[d.id.isin(registry.id)].copy()
    sample["case_id"] = sample.id.map(lambda s: hashlib.sha256(("blind|"+s).encode()).hexdigest()[:12])
    sample = sample.sort_values("case_id")
    sample[["case_id","domain","prompt","response"]].to_csv(out / "tables/cases_blinded.csv", index=False)
    sample[["case_id","id","model","H","E","D","F","OA","condition","scenario_type"]].to_csv(out / "tables/cases_answer_key.csv", index=False)
    template = sample[["case_id"]].copy()
    for col in ("coder_id", "review_warranted", "attributable_cue", "contextual_reason", "possible_other_concern", "uncertainty", "notes"):
        template[col] = ""
    template.to_csv(out / "tables/human_coding_template.csv", index=False)
