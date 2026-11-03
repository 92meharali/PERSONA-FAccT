import numpy as np
import pandas as pd
import pytest

from analysis.followup_semantic import checked_join, interval


def fixture():
    corpus = pd.DataFrame(dict(domain=["mental_health"]*2, annotation_item_id=["a","b"],
                               H=[.1,.2], prompt_id=["p","p"], prompt=["x","x"], response=["one","two"]))
    frame = pd.DataFrame(dict(annotation_item_id=["b","a"], study_id=["s2","s1"],
                             humt_score=[.2,.1], prompt_id=["p","p"], prompt=["x","x"], response=["two","one"]))
    labels = pd.DataFrame(dict(study_id=["s2","s1"], resolved=[0,1]))
    return corpus,frame,labels


def test_join_is_by_id_not_row_order():
    mh, ids, y = checked_join(*fixture())
    assert ids.tolist()==["s1","s2"] and y.tolist()==[True,False]


@pytest.mark.parametrize("kind", ["duplicate","missing","score","text","unresolved"])
def test_join_rejects_invalid_inputs(kind):
    c,f,l=fixture()
    if kind=="duplicate": f.loc[1,"annotation_item_id"]="b"
    if kind=="missing": l=l.iloc[:1]
    if kind=="score": f.loc[0,"humt_score"]=.9
    if kind=="text": f.loc[0,"response"]="changed"
    if kind=="unresolved": l.loc[0,"resolved"]=-1
    with pytest.raises(ValueError): checked_join(c,f,l)


def test_degenerate_draws_are_counted_not_zeroed():
    lo,hi,n=interval([np.nan, .2, .4])
    assert n==2 and lo>.19 and hi<.41
    lo,hi,n=interval([np.nan])
    assert n==0 and np.isnan(lo) and np.isnan(hi)
