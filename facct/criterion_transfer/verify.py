"""Independently reconstruct all operating points from prior OOF predictions."""
import itertools
import json
import math

import numpy as np
import pandas as pd

from facct.analysis.screening import tie_keys
from facct.analysis.validate_inputs import sha
from .run import HERE, ROOT, TRAIN, MODELS, followup


def verify():
    out=HERE/"outputs"
    manifest=json.loads((out/"manifest.json").read_text())
    assert manifest["status"] == "final" and manifest["config"]["replicates"] >= 2000
    for name,digest in manifest["frozen_hashes"].items():
        assert sha(ROOT/name)==digest, name
    for name,digest in manifest["outputs"].items():
        assert sha(out/name)==digest, name
    for name,digest in manifest["code_and_plan"].items():
        assert sha(ROOT/name)==digest, name
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    mh=d[d.domain=="mental_health"].copy()
    extra,_=followup(mh)
    review=dict(zip(mh.id,extra))
    d=d.set_index("id")
    old=pd.read_csv(ROOT/"facct/conditional/outputs/oof_predictions.csv")
    perf=pd.read_csv(out/"performance.csv")
    chosen=pd.read_csv(out/"selections.csv")
    contrasts=pd.read_csv(out/"contrasts.csv")
    arrays={domain:np.load(out/f"bootstrap_{domain}.npz") for domain in manifest["evaluation_targets"]}
    checks=0
    for r in perf.itertuples():
        frame=old[(old.domain==r.domain)&(old.criterion==r.train_target)].copy()
        frame["tie"]=tie_keys(frame.id,manifest["config"]["seed"])
        score="reduced_lr" if r.model==MODELS[0] else "extended_lr"
        selected=[]
        for _,batch in frame.groupby("fold"):
            ranked=batch.sort_values([score,"tie"],ascending=[False,True])
            selected.extend(ranked.head(math.floor(len(batch)*r.budget+1e-12)).id)
        all_ids=frame.id.tolist()
        if r.evaluation_target=="contextual_reviewworthiness":
            y=pd.Series({i:review[i] for i in all_ids})
        else:
            col, op, cutoff={"D_ge3":("D", "ge",3), "F_lt4":("F","lt",4), "OA_lt4":("OA","lt",4)}[r.evaluation_target]
            values=d.loc[all_ids,col]
            y=values.ge(cutoff) if op=="ge" else values.lt(cutoff)
        p,k,c=int(y.sum()),len(selected),int(y.loc[selected].sum())
        assert (r.concerns,r.selected,r.caught)==(p,k,c)
        np.testing.assert_allclose([r.recall,r.precision,r.missed,r.unselected_prevalence],
            [c/p if p else np.nan,c/k if k else np.nan,p-c,(p-c)/(len(y)-k) if k<len(y) else np.nan],equal_nan=True)
        saved=chosen[(chosen.domain==r.domain)&(chosen.model==r.model)&(chosen.train_target==r.train_target)&(chosen.budget==r.budget)]
        assert set(saved.id)==set(selected) and len(saved)==k
        if r.budget==.2:
            e=manifest["evaluation_targets"][r.domain].index(r.evaluation_target)
            a=arrays[r.domain]["values"][:,TRAIN.index(r.train_target),MODELS.index(r.model),e,1]
            valid=a[np.isfinite(a)]
            np.testing.assert_allclose(np.quantile(valid,[.025,.975]),[r.recall_lo,r.recall_hi])
            assert r.recall_valid==len(valid)
        checks+=1
    for r in contrasts[contrasts.budget==.2].itertuples():
        a=arrays[r.domain]["values"]
        e=manifest["evaluation_targets"][r.domain].index(r.evaluation_target)
        v=a[:,TRAIN.index(r.left_target),MODELS.index(r.model),e,1]-a[:,TRAIN.index(r.right_target),MODELS.index(r.model),e,1]
        valid=v[np.isfinite(v)]
        assert len(valid)==r.valid_replicates
        np.testing.assert_allclose(np.quantile(valid,[.025,.975]),[r.lo,r.hi])
    assert checks==240 and len(contrasts[contrasts.budget==.2])==60
    # Every pair's difference is between immutable queues, not independently
    # reranked endpoint-specific selections.
    overlaps=pd.read_csv(out/"queue_overlap.csv")
    for r in overlaps.itertuples():
        base=chosen[(chosen.domain==r.domain)&(chosen.model==r.model)&(chosen.budget==r.budget)]
        a=set(base[base.train_target==r.left_target].id)
        b=set(base[base.train_target==r.right_target].id)
        assert len(a&b)==r.intersection and len(a^b)==r.symmetric_difference
        assert len(a|b)==r.union
    result=dict(operating_points=checks, reference_paired_intervals=60, queue_pairs=len(overlaps),
        prior_predictions_used=True, immutable_sources_verified=True,
        analysis_manifest_sha256=sha(out/"manifest.json"))
    (out/"verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    return result


if __name__=="__main__":
    verify()
