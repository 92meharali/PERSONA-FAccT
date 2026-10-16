import json

import numpy as np
import pandas as pd
import pytest

from facct.allocation.run import ROOT, POLICIES, evaluate, membership
from facct.analysis.screening import tie_keys
from facct.analysis.validate_inputs import sha


def toy():
    X=np.array([[10,10,.9],[9,9,.8],[2,2,.2],[1,1,.1]],float)
    Y=np.array([[True],[False],[True],[False]])
    G=np.array([[1,0],[1,0],[0,1],[0,1]],float)
    return X,Y,G,tie_keys(list("abcd"),3)


def test_common_queue_not_separate_subgroup_quotas():
    X,Y,G,keys=toy()
    v,s=evaluate(X,Y,G,keys,.5)
    assert v[0,0,0,0]==2 and v[1,0,0,0]==0
    assert s[:,0].sum()==2
    assert v[0,0,0,2]==1 and v[1,0,0,2]==0
    assert v[0,0,0,7]==1 and v[1,0,0,7]==-1
    assert np.isnan(v[1,0,0,3])


def test_random_uses_full_batch_expectation():
    X,Y,G,keys=toy()
    v,_=evaluate(X,Y,G,keys,.25)
    assert np.allclose(v[:,0,4,0],[.5,.5])
    assert np.allclose(v[:,0,4,1],[.25,.25])
    assert np.allclose(v[:,0,4,2],.25)
    assert np.allclose(v[:,0,4,8],0)


def test_fixed_selection_invariant_to_labels():
    X,Y,G,keys=toy()
    _,s=evaluate(X,Y,G,keys,.5)
    _,other=evaluate(X,~Y,G,keys,.5)
    assert np.array_equal(s,other)


def test_empty_category_and_no_concerns():
    X,Y,G,keys=toy()
    G=np.column_stack((G,np.zeros(4)))
    v,_=evaluate(X,np.zeros_like(Y),G,keys,.5)
    assert np.isnan(v[...,2]).all()
    assert np.isnan(v[2,...,3]).all()
    assert np.isnan(v[2,...,6]).all()
    assert (v[2,...,0]==0).all()


def test_ties_deterministic_and_exact():
    X,Y,G,keys=toy(); X[:]=0
    a,s=evaluate(X,Y,G,keys,.5)
    b,t=evaluate(X,Y,G,keys,.5)
    assert np.array_equal(s,t)
    assert np.all(s[:,:4].sum(axis=0)==2)
    assert np.allclose(a,b,equal_nan=True)


def test_membership_covers_missing_and_partition_conservation():
    d=pd.DataFrame(dict(condition=["natural",None],model=["a","b"],scenario_type=["x","x"]))
    names,G=membership(d)
    assert ("condition","<missing>") in names
    for key in ("condition","model","scenario_type"):
        assert np.all(G[:,[i for i,p in enumerate(names) if p[0]==key]].sum(axis=1)==1)


def test_final_source_integrity_and_original_reconstruction():
    out=ROOT/"facct/allocation/outputs"
    if not (out/"manifest.json").exists():
        pytest.skip("Final run pending")
    m=json.loads((out/"manifest.json").read_text())
    assert m["config"]["replicates"]>=2000
    for section in ("frozen_hashes","code_and_plan"):
        for path,digest in m[section].items():
            assert sha(ROOT/path)==digest,path
    for name,digest in m["outputs"].items():
        assert sha(out/name)==digest,name
    d=pd.read_csv(out/"category_coverage.csv")
    old=pd.read_csv(ROOT/"facct/outputs/tables/screening.csv")
    old=old[old.budget.eq(.2)&old.domain.ne("pooled")]
    fusion=pd.read_csv(ROOT/"facct/revision/outputs/complementarity.csv")
    for (domain,criterion,grouping,policy),g in d.groupby(["domain","criterion","grouping","policy"]):
        assert g.n.sum()==g.domain_n.iloc[0]
        assert g.selected.sum()==pytest.approx(g.domain_selected.iloc[0])
        if policy=="rank_fusion":
            r=fusion[fusion.domain.eq(domain)&fusion.criterion.eq(criterion)&fusion.budget.eq(.2)].iloc[0]
            assert g.caught.sum()==r.caught_fusion
        else:
            r=old[old.domain.eq(domain)&old.criterion.eq(criterion)&old.policy.eq(policy)].iloc[0]
            assert g.caught.sum()==pytest.approx(r.caught)
            assert g.concerns.sum()==r.concerns
    register=pd.read_csv(out/"selection_register.csv")
    assert len(register)==1490 and not register.id.duplicated().any()
    assert set(d.policy)==set(POLICIES)
