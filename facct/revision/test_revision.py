import json

import numpy as np
import pandas as pd
import pytest

from facct.revision.run import ROOT, allocation_values, complementarity, fusion_scores, policy_orders
from facct.analysis.screening import tie_keys
from facct.analysis.validate_inputs import sha


def test_fusion_is_label_free_and_tie_aware():
    X=np.array([[1,9,.5],[2,0,.2],[2,4,.5]],dtype=float)
    expected=(np.array([1,2.5,2.5])+np.array([2.5,1,2.5]))/6
    assert np.allclose(fusion_scores(X),expected)
    changed=X.copy(); changed[:,1]=1000
    assert np.array_equal(fusion_scores(X),fusion_scores(changed))


def test_exact_capacity_and_complementarity():
    X=np.array([[4,1,0],[3,1,1],[2,1,2],[1,1,3]],dtype=float)
    Y=np.array([[True],[False],[True],[False]])
    keys=tie_keys(["a","b","c","d"],42)
    config={"budgets":[.5],"criteria":{"D_ge3":{}}}
    r=complementarity(X,Y,keys,config,"test")[0]
    assert r["selected"]==2 and r["selected_overlap"]==0
    assert r["caught_h_only"]==r["caught_markers_only"]==1
    assert r["union_size"]==4 and r["union_is_not_a_policy"]
    orders,_=policy_orders(X,keys)
    assert all(len(set(order[:2]))==2 for order in orders)
    assert np.array_equal(orders[3],policy_orders(X,keys)[0][3])


def test_paired_workload_difference_hand_example():
    X=np.array([[4,4,4],[3,3,3],[2,2,2],[1,1,1]],dtype=float)
    Y=np.array([[True],[True],[False],[False]])
    values=allocation_values(X,Y,tie_keys(list("abcd"),42),budget=.5)[0]
    # Two cases are both needed for 80% recall: observed 2/4, expected random 10/12.
    assert np.allclose(values,[1,0,0,.5-10/12,0,0])


def test_zero_positive_stays_undefined():
    X=np.array([[1,2,3],[2,3,4]],dtype=float)
    assert np.isnan(allocation_values(X,np.zeros((2,1),dtype=bool),tie_keys(["a","b"],0))).all()


def test_all_positive_and_zero_budget():
    X=np.ones((5,3))
    values=allocation_values(X,np.ones((5,1),dtype=bool),tie_keys(list("abcde"),0),budget=0)[0]
    assert np.allclose(values,[0,0,0,0,0,0])


def test_nonfinite_scores_rejected():
    with pytest.raises(ValueError):
        policy_orders(np.array([[np.nan,1,2]]),tie_keys(["x"],0))


def test_final_revision_integrity():
    path=ROOT/"facct/revision/outputs/manifest.json"
    if not path.exists():
        pytest.skip("Final analysis has not run yet")
    manifest=json.loads(path.read_text())
    assert manifest["status"]=="final" and manifest["replicates"]>=2000
    for group in ("source_hashes","frozen_output_hashes","revision_sources"):
        for name,digest in manifest[group].items():
            assert sha(ROOT/name)==digest,name
    for name,digest in manifest["outputs"].items():
        assert sha(path.parent/name)==digest,name
    pairs=pd.read_csv(path.parent/"paired_comparisons.csv")
    assert len(pairs)==54
    assert pairs.valid_replicates.le(pairs.replicates).all()
    frozen=pd.read_csv(ROOT/"facct/outputs/tables/screening.csv")
    for row in pairs[pairs.metric=="H_minus_markers_recall"].itertuples():
        original=frozen[(frozen.domain==row.domain)&(frozen.criterion==row.criterion)&(frozen.policy=="high_H")&(frozen.budget==.2)].iloc[0]
        assert np.allclose([row.estimate,row.lo,row.hi],original[["delta_markers","delta_markers_lo","delta_markers_hi"]].to_numpy(float))
    comps=pd.read_csv(path.parent/"complementarity.csv")
    assert (comps.caught_both+comps.caught_h_only==comps.caught_h).all()
    assert (comps.caught_both+comps.caught_markers_only==comps.caught_markers).all()
    assert (comps.caught_fusion<=comps.selected).all()
    audit=pd.read_csv(path.parent/"text_provenance.csv")
    assert len(audit)==1490 and not audit.id.duplicated().any()
