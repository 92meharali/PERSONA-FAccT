import json

import pandas as pd

from .prepare_materials import ROOT, choose_cases, prepare


def test_orientation_ignores_labels_and_diagnostic_invariant():
    d=pd.read_csv(ROOT/"analysis/processed/persona_all.csv")
    d["id"]=d.domain+":"+d.annotation_item_id
    reg=pd.read_csv(ROOT/"facct/outputs/tables/case_sampling_register.csv")
    for domain,g in d.groupby("domain"):
        r=reg[reg.domain==domain]
        a=choose_cases(g,r)
        altered=g.copy()
        altered[["H","D","F","OA"]]=999
        b=choose_cases(altered.sample(frac=1,random_state=3),r.sample(frac=1,random_state=3))
        assert a==b
        assert len(set(a[0]))==2 and len(set(a[1]))==6
        assert set(a[1]).issubset(set(r.id.dropna()))


def test_packets_reproduce_without_participant_outcomes(tmp_path):
    a=prepare(output=tmp_path/"a")
    b=prepare(output=tmp_path/"b")
    assert a==b
    assert a["human_participants"]==0
    schedule=pd.read_csv(tmp_path/"a/planned_slots.csv")
    assert len(schedule)==9 and (schedule.status=="not enrolled").all()
    assert sorted(schedule[schedule.target=="initial target"].policy_order.value_counts())==[2,2,2]
    coverage=json.loads((tmp_path/"a/sampling_coverage.json").read_text())
    assert len(coverage)==3
    for p in (tmp_path/"a").glob("*/part[12]*.md"):
        text=p.read_text()
        assert "| Policy |" not in text and "source_id" not in text
