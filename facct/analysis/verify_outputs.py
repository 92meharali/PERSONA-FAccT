"""Independent point-estimate checks and optional full rerun comparison."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from .screening import POLICIES, capacity, features, labels, order_scores, tie_keys
from .validate_inputs import sha, source_hashes

ROOT=Path(__file__).resolve().parents[2]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--compare",type=Path)
    args=parser.parse_args()
    out=ROOT/"facct/outputs"
    manifest=json.loads((out/"manifest.json").read_text())
    assert source_hashes(ROOT)==manifest["source_hashes"], "Source changed since final run"
    for name,expected in manifest["code_and_protocol_hashes"].items():
        assert sha(ROOT/name)==expected, f"Code/protocol changed: {name}"
    for name,expected in manifest["output_hashes"].items():
        assert sha(out/name)==expected, f"Output changed: {name}"
    config=json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    table=pd.read_csv(out/"tables/screening.csv")
    checked=0
    for domain,g in list(d.groupby("domain"))+[("pooled",d)]:
        X,Y=features(g),labels(g,config)
        for j,criterion in enumerate(config["criteria"]):
            y=Y[:,j]
            for i,policy in enumerate(POLICIES):
                scores=X[:,i]
                order=order_scores(scores,tie_keys(g.id,config["seed"]))
                for budget in config["budgets"]:
                    row=table[(table.domain==domain)&(table.criterion==criterion)&(table.policy==policy)&(table.budget==budget)].iloc[0]
                    k=capacity(len(g),budget)
                    caught=y[order[:k]].sum()
                    assert row.selected==k and row.caught==caught
                    assert np.isclose(row.recall,caught/y.sum())
                    assert np.isclose(row.precision,caught/k)
                    assert np.isclose(row.ap,average_precision_score(y,scores))
                    assert np.isclose(row.auc,roc_auc_score(y,scores))
                    assert np.isclose(row.missed,y.sum()-caught)
                    assert np.isclose(row.unselected_prevalence,(y.sum()-caught)/(len(g)-k))
                    checked+=1
    compared=[]
    if args.compare:
        other=args.compare.resolve()
        for path in sorted((out/"tables").glob("*.csv")):
            assert sha(path)==sha(other/"tables"/path.name), f"Non-reproducible table: {path.name}"
            compared.append(path.name)
        for path in sorted((out/"figures").glob("*")):
            assert sha(path)==sha(other/"figures"/path.name), f"Non-reproducible figure: {path.name}"
            compared.append(path.name)
    report={"status":"passed","checked_ranked_operating_points":checked,"independent_ranking_reference":"scikit-learn average_precision_score and roc_auc_score", "source_hashes_unchanged":True,"code_and_output_hashes_verified":True,"byte_identical_rerun_files":compared,"manifest_sha256":sha(out/"manifest.json")}
    (out/"verification.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
