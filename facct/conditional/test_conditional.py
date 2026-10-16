import json

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from facct.analysis.screening import capacity, tie_keys
from facct.analysis.validate_inputs import sha
from facct.conditional.analysis import (POLICIES, crossfit, evaluate, fit_predict, group_folds,
                                        model_inputs, resample_within_folds)
from facct.conditional.run import ROOT


@pytest.fixture
def config():
    return json.loads((ROOT/"facct/conditional/config.json").read_text())


def toy():
    rng=np.random.default_rng(9)
    X=np.column_stack((rng.normal(size=30),rng.integers(1,100,size=30),rng.uniform(size=30)))
    Y=(np.arange(30)%3==0)[:,None]
    clusters=np.repeat([f"p{i}" for i in range(10)],3)
    return X,Y,clusters


def test_folds_group_integrity_and_order_invariance():
    _,_,clusters=toy()
    f=group_folds(clusters,4)
    for c in np.unique(clusters):
        assert len(np.unique(f[clusters==c]))==1
    assert np.array_equal(f[::-1],group_folds(clusters[::-1],4))
    assert set(f)==set(range(5))


def test_bootstrap_copies_preserve_original_folds():
    _,_,clusters=toy()
    folds=group_folds(clusters,4)
    idx,copies=resample_within_folds(folds,clusters,np.random.default_rng(6))
    for c in np.unique(clusters[idx]):
        assert len(np.unique(folds[idx][clusters[idx]==c]))==1
    for copy in np.unique(copies):
        assert sum(copies==copy)==3
    assert len(idx)==len(clusters)


def test_training_only_scaler_and_reference_pipeline(config):
    X,Y,_=toy()
    pred,audit=fit_predict(X[:20],Y[:20,0],X[20:],True,config)
    expected=model_inputs(X[:20],True).mean(axis=0)
    assert np.allclose(audit["scaler_mean"],expected)
    pipeline=make_pipeline(StandardScaler(),LogisticRegression(**config["logistic"],class_weight=None,fit_intercept=True))
    pipeline.fit(model_inputs(X[:20],True),Y[:20,0])
    assert np.allclose(pred,pipeline.predict_proba(model_inputs(X[20:],True))[:,1])
    changed=X[20:].copy(); changed[0]=[9999,999999,.99]
    changed_pred,changed_audit=fit_predict(X[:20],Y[:20,0],changed,True,config)
    assert changed_audit==audit
    assert np.allclose(changed_pred[1:],pred[1:])


def test_own_fold_labels_cannot_change_own_predictions(config):
    X,Y,clusters=toy(); f=group_folds(clusters,4)
    s,_,_=crossfit(X,Y,f,clusters,config)
    changed=Y.copy(); changed[f==0]=~changed[f==0]
    s2,_,_=crossfit(X,changed,f,clusters,config)
    assert np.array_equal(s[f==0],s2[f==0])


def test_crossfit_rejects_group_leakage(config):
    X,Y,clusters=toy(); f=group_folds(clusters,4)
    f[0]=(f[1]+1)%5
    with pytest.raises(ValueError,match="prompt occurs"):
        crossfit(X,Y,f,clusters,config)


def test_single_class_fallback_explicit(config):
    X,_,_=toy()
    for outcome in (0,1):
        pred,audit=fit_predict(X[:20],np.full(20,outcome),X[20:],False,config)
        assert np.array_equal(pred,np.full(10,outcome))
        assert audit["single_class_fallback"] and audit["coefficients"] is None


def test_exact_batch_budget_micro_counts_and_random():
    Y=np.array([[True],[False],[False],[False],[False]])
    f=np.array([0,0,0,1,1]); scores=np.zeros((5,1,6)); scores[0]=2
    values,records=evaluate(scores,Y,f,tie_keys(list("abcde"),3),[.5])
    assert np.allclose(values[0,0,0],[1,1,.5,0,0])
    assert values[0,0,6,0]==pytest.approx(1/3)
    assert sum(r["selected"] for r in records if r["policy"]=="high_H")==2
    assert all(r["selected"]==capacity(r["n"],.5) for r in records)


def test_zero_positives_and_zero_capacity():
    scores=np.zeros((5,1,6)); f=np.arange(5); keys=tie_keys(list("abcde"),2)
    values,_=evaluate(scores,np.zeros((5,1),dtype=bool),f,keys,[.2])
    assert np.isnan(values[...,1]).all() and np.isnan(values[...,2]).all()
    assert (values[...,0]==0).all()


def test_all_positive_is_defined():
    scores=np.zeros((10,1,6)); f=np.repeat(np.arange(5),2); keys=tie_keys(np.arange(10),2)
    v,_=evaluate(scores,np.ones((10,1),dtype=bool),f,keys,[.5])
    assert np.allclose(v[...,1],.5) and np.allclose(v[...,2],1)


def test_invalid_feature_values():
    with pytest.raises(ValueError):
        model_inputs(np.array([[np.nan,1,1]]),True)
    with pytest.raises(ValueError):
        model_inputs(np.array([[0,-1,1]]),False)


def test_final_completeness_and_traceability():
    out=ROOT/"facct/conditional/outputs"
    if not (out/"manifest.json").exists():
        pytest.skip("Final trained analysis has not run")
    manifest=json.loads((out/"manifest.json").read_text())
    assert manifest["status"]=="final" and manifest["config"]["replicates"]>=2000
    for group in ("frozen_hashes","code_and_plan"):
        for name,digest in manifest[group].items():
            assert sha(ROOT/name)==digest,name
    for name,digest in manifest["outputs"].items():
        assert sha(out/name)==digest,name
    rows=pd.read_csv(out/"performance.csv")
    assert len(rows)==252 and len(rows[rows.budget==.2])==63
    assert not rows.duplicated(["domain","criterion","budget","policy"]).any()
    assert (rows.groupby(["domain","criterion","budget"]).selected.nunique()==1).all()
    assert set(rows.policy)==set(POLICIES)
    assert (rows.caught<=rows.selected+1e-9).all()
    pred=pd.read_csv(out/"oof_predictions.csv")
    assert len(pred)==1490*3
    assert not pred.duplicated(["id","criterion"]).any()
    assert (pred.groupby("cluster").fold.nunique()==1).all()
    audit=pd.read_csv(out/"fit_audit.csv")
    assert len(audit)==90
    assert (audit.underlying_training_ratings==5*audit.training_responses).all()
    pairs=pd.read_csv(out/"conditional_lift.csv")
    reps=pd.read_csv(out/"bootstrap_differences.csv")
    for row in pairs[pairs.budget==.2].itertuples():
        d=reps[(reps.domain==row.domain)&(reps.criterion==row.criterion)].conditional_lift.dropna()
        assert len(d)==row.valid_replicates
        assert np.allclose(np.quantile(d,[.025,.975]),[row.lo,row.hi])
        assert row.conditional_lift==pytest.approx(row.extended_recall-row.reduced_recall)
