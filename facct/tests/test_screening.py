import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import average_precision_score, roc_auc_score

from facct.analysis.screening import allocation, capacity, evaluate, features, order_scores, rank_metrics, tie_keys
from facct.analysis.uncertainty import draw_indices, summarize


@pytest.mark.parametrize("n,b,k",[(415,.2,83),(660,.05,33),(3,.2,0),(0,.2,0),(19,.1,1),(1490,.3,447)])
def test_exact_budget(n,b,k):
    assert capacity(n,b)==k
    assert len(order_scores(np.ones(n),tie_keys(map(str,range(n)),7))[:k])==k


def test_direction_and_tie_determinism():
    scores=np.array([1,3,3,2])
    ids=np.array(["a","b","c","d"])
    a=order_scores(scores,tie_keys(ids,5))
    perm=np.array([3,1,0,2])
    b=perm[order_scores(scores[perm],tie_keys(ids[perm],5))]
    assert np.array_equal(a,b)
    assert set(a[:2])=={1,2}


@pytest.mark.parametrize("y,s",[([1,0,1,0],[4,3,2,1]),([1,0,1,0],[1,1,0,0]),([1,1,1],[2,2,1]),([1,0],[1,1])])
def test_metrics_against_sklearn(y,s):
    order=order_scores(s,tie_keys(map(str,range(len(y))),1))
    ap,auc,_=rank_metrics(y,s,order)
    assert ap==pytest.approx(average_precision_score(y,s))
    if len(set(y))==2: assert auc==pytest.approx(roc_auc_score(y,s))
    else: assert np.isnan(auc)


def test_hand_example():
    ap,auc,w=rank_metrics([1,0,1,0],[4,3,2,1],np.arange(4))
    assert ap==pytest.approx((1+2/3)/2)
    assert auc==.75
    assert w==[.25,.75,.75,.75]


def test_random_tie_block_metrics():
    rng=np.random.default_rng(9)
    for _ in range(50):
        y=rng.integers(0,2,100)
        s=rng.integers(0,5,100)
        ap,auc,_=rank_metrics(y,s,order_scores(s,tie_keys(map(str,range(100)),1)))
        assert ap==pytest.approx(average_precision_score(y,s))
        assert auc==pytest.approx(roc_auc_score(y,s))


def test_zero_positive_and_missing():
    ap,auc,w=rank_metrics([0,0],[2,1],np.arange(2))
    assert np.isnan(ap) and np.isnan(auc) and np.isnan(w).all()
    with pytest.raises(ValueError): order_scores([1,np.nan],[1,2])
    assert summarize([np.nan,np.nan])[2]==0


def test_single_positive():
    ap,auc,w=rank_metrics([1],[1],np.array([0]))
    assert ap==1 and np.isnan(auc) and w==[1,1,1,1]


def test_label_leakage_excluded():
    f=pd.DataFrame({"response":["I am sorry", "technical answer"],"H":[.1,.2],"D":[1,5],"OA":[5,1]})
    a=features(f)
    f[["D","OA"]]=999
    assert np.array_equal(a,features(f))
    assert a[0,2]==pytest.approx(2/3)


def test_cluster_integrity_and_pairing():
    domains=np.array(["a","a","a","b","b"])
    clusters=np.array(["a1","a1","a2","b1","b1"])
    idx,copies=draw_indices(domains,clusters,np.random.default_rng(1))
    idx2,copies2=draw_indices(domains,clusters,np.random.default_rng(1))
    assert np.array_equal(idx,idx2) and np.array_equal(copies,copies2)
    for c in np.unique(copies):
        group=idx[copies==c]
        assert len(np.unique(clusters[group]))==1
        assert set(group)==set(np.flatnonzero(clusters==clusters[group[0]]))


def test_allocation_and_random_expectation():
    domains=np.array(["a"]*3+["b"]*2)
    assert allocation(domains,2)=={"a":1,"b":1}
    cfg={"criteria":{"risk":{}},"budgets":[.4]}
    X=np.column_stack([np.arange(5)]*3)
    Y=np.array([0,0,0,1,1],bool)[:,None]
    rows=evaluate(X,Y,domains,np.arange(5),tie_keys(map(str,range(5)),1),cfg,True)
    uniform=next(r[3] for r in rows if r[1]=="uniform_random")
    strat=next(r[3] for r in rows if r[1]=="stratified_random")
    assert uniform[4]==pytest.approx(.8)
    assert uniform[5]==pytest.approx(.4)
    assert strat[4]==1
