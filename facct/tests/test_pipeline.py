import json
from pathlib import Path

import pandas as pd

from facct.analysis import model_comparisons, sample_cases, sensitivity
from facct.analysis.uncertainty import bootstrap
from facct.analysis.validate_inputs import sha

ROOT=Path(__file__).resolve().parents[2]


def inputs():
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    r=pd.read_csv(ROOT/"analysis/processed/persona_ratings_long.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    d["cluster"]=d.domain+":"+d.prompt_id
    config=json.loads((ROOT/"facct/protocol/criteria.yaml").read_text())
    return d,r,config


def test_sensitivity_and_materials(tmp_path):
    d,r,c=inputs()
    (tmp_path/"tables").mkdir()
    before=sha(ROOT/"analysis/processed/persona_all.csv")
    sensitivity.run(d,r,c,tmp_path)
    model_comparisons.run(d,c,5,tmp_path)
    sample_cases.run(d,c,tmp_path)
    assert sha(ROOT/"analysis/processed/persona_all.csv")==before
    overlap=pd.read_csv(tmp_path/"tables/criterion_intersections.csv")
    assert overlap[overlap.domain=="pooled"].n.sum()==1490
    blind=pd.read_csv(tmp_path/"tables/cases_blinded.csv")
    assert not {"H","D","F","OA","model"}.intersection(blind.columns)
    codes=pd.read_csv(tmp_path/"tables/human_coding_template.csv")
    assert codes.drop(columns="case_id").isna().all().all()


def test_bootstrap_reproducibility():
    d,_,c=inputs()
    small=d[(d.domain=="education") & d.prompt_id.isin(d[d.domain=="education"].prompt_id.unique()[:4])]
    a=bootstrap(small,c,5)
    b=bootstrap(small,c,5)
    pd.testing.assert_frame_equal(a,b)
    assert a.attrs==b.attrs or len(a.attrs["criterion_comparisons"])==36


def test_released_input_identity():
    for name in ("persona_all.csv","persona_ratings_long.csv"):
        assert sha(ROOT/"analysis/processed"/name)==sha(ROOT/"submission/chi2027_supplement/analysis/processed"/name)
