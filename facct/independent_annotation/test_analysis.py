import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import cohen_kappa_score

from facct.independent_annotation.run import (
    agreement, binary, bootstrap, expected_random, keyed, metric, resolve,
)
from facct.analysis.screening import features, capacity, order_scores, tie_keys
from facct.analysis.uncertainty import draw_indices


@pytest.mark.parametrize("rating,expected", [("0",0),("1",0),("2",1),("3",1),("U",-1),("",-1)])
def test_rating_mapping(rating, expected):
    assert binary(rating) == expected


@pytest.mark.parametrize("rating", ["2.0", "4", "nan", "yes"])
def test_reject_invalid_ratings(rating):
    with pytest.raises(ValueError):
        binary(rating)


@pytest.mark.parametrize("a,b,c,want", [(0,0,None,0),(1,1,None,1),(1,0,0,0),
    (1,0,1,1),(1,0,-1,-1),(-1,1,1,1),(-1,0,0,0),(-1,-1,1,-1),(0,-1,None,-1)])
def test_majority_and_unresolved(a,b,c,want):
    assert resolve(a,b,c)[0] == want


def test_agreement_orientation_and_independent_estimator():
    a = np.array([1]*17 + [0]*629 + [1]*12 + [0]*2)
    b = np.array([1]*17 + [0]*629 + [0]*12 + [1]*2)
    result = agreement(a,b)
    assert result["A_yes_B_no"] == 12
    assert result["A_no_B_yes"] == 2
    assert result["positive_agreement"] == pytest.approx(34/48)
    assert result["kappa"] == pytest.approx(cohen_kappa_score(a,b))


def test_agreement_undefined_not_filled_with_zero():
    assert agreement(np.zeros(5),np.zeros(5))["kappa"] is None
    assert agreement(np.array([-1]),np.array([1]))["raw_agreement"] is None


def test_metrics_and_random_hand_example():
    y = np.array([1,0,1,0,0])
    mask = np.array([1,1,0,0,0],bool)
    m = metric(y,mask,np.arange(5))
    assert (m["caught"],m["missed"]) == (1,1)
    assert m["recall"] == .5 and m["precision"] == .5
    r = expected_random(y,2,np.arange(5))
    assert r["caught"] == .8 and r["recall"] == .4


def test_missing_and_no_positives():
    m = metric(np.array([1,-1,0]),np.array([1,0,0],bool),np.arange(3))
    assert np.isnan(m["recall"]) and np.isnan(m["precision"])
    assert m["recall_lower"] == .5 and m["recall_upper"] == 1
    z = metric(np.zeros(3),np.zeros(3,bool),np.arange(3))
    assert np.isnan(z["recall"]) and np.isnan(z["precision"])
    assert np.isnan(expected_random(np.zeros(3),1,np.arange(3))["recall"])


def test_all_positive_and_zero_budget():
    y=np.ones(5)
    m=metric(y,np.array([1,1,0,0,0],bool),np.arange(5))
    assert m["recall"] == .4 and m["precision"] == 1
    z=metric(y,np.zeros(5,bool),np.arange(5))
    assert z["recall"] == 0 and np.isnan(z["precision"])


def test_unresolved_only_recall_bounds_condition_on_positive_exists():
    m=metric(np.array([-1,0]),np.array([1,0],bool),np.arange(2))
    assert m["recall_lower"] == 1 and m["recall_upper"] == 1
    m=metric(np.array([-1,0]),np.array([0,1],bool),np.arange(2))
    assert m["recall_lower"] == 0 and m["recall_upper"] == 0
    assert np.isnan(m["recall"])


def test_ids_reject_duplicates():
    with pytest.raises(ValueError):
        keyed(pd.DataFrame({"study_id":["x","x"]}),"example")


def toy_frame():
    return pd.DataFrame({"id":[f"id{i}" for i in range(12)],
        "domain":["mental_health"]*12,"cluster":np.repeat(["a","b","c","d"],3),
        "H":np.arange(12)/12,"response":["I am sorry", "technical", "please you"]*4})


def test_features_exact_budget_and_no_label_leakage():
    d=toy_frame()
    x=features(d)
    d["rating_A"]=1
    d["resolved"]=999
    assert np.array_equal(features(d),x)
    assert x[0,1] == 3 and x[0,2] == pytest.approx(2/3)
    o=order_scores(x[:,2],tie_keys(d.id,20261002))
    assert len(o[:capacity(len(d),.2)]) == 2


def test_whole_cluster_draws():
    d=toy_frame()
    idx,copies=draw_indices(d.domain.to_numpy(),d.cluster.to_numpy(),np.random.default_rng(17))
    for copy in np.unique(copies):
        members=idx[copies == copy]
        assert len(members) == 3
        assert d.iloc[members].cluster.nunique() == 1


def test_paired_reproducible_bootstrap_and_degeneracy():
    d=toy_frame()
    y=np.array([1,0,0]*4)
    args=(d,{"A":y,"B":y,"zero":np.zeros(12,dtype=int)}, {"seed":20261002},30,17)
    first=bootstrap(*args)
    pd.testing.assert_frame_equal(first,bootstrap(*args))
    pd.testing.assert_frame_equal(first[first.target=="A"].drop(columns="target").reset_index(drop=True),
                                  first[first.target=="B"].drop(columns="target").reset_index(drop=True))
    assert first[first.target=="zero"].effective.eq(0).all()
    assert first[first.target=="zero"].lo.isna().all()
