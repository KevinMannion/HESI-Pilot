import json, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import run

def make_fixture(tmp_path, mismatch=False):
    data=tmp_path/'input_data';data.mkdir()
    people=pd.DataFrame({'SERIALNO':['A','A','B','C','D','E'], 'AGEP':[30,28,35,45,25,60], 'SEX':[1,2,1,2,1,2]})
    # A owner below threshold, B renter above, C tenure 4, D missing income, E count mismatch optionally
    rows=[]
    for serial,np_,ten,inc,rent,mort,weight in [('A',2,1,1000,0,1500,10),('B',1,3,100000,1000,0,20),('C',1,4,15000,0,0,30),('D',1,3,np.nan,600,0,40),('E',1 if not mismatch else 2,3,100000,500,0,50),('F',1,3,12000,500,0,60)]:
        row={'SERIALNO':serial,'NP':np_,'TEN':ten,'HINCP':inc,'ADJINC':1000000,'ADJHSG':1000000,'GRNTP':rent,'SMOCP':mort,'WGTP':weight}
        row.update({f'WGTP{k}':weight for k in range(1,81)})
        rows.append(row)
    housing=pd.DataFrame(rows)
    for fn,df in [('csv_pus.zip',people),('csv_hus.zip',housing)]:
        with zipfile.ZipFile(data/fn,'w') as z:z.writestr('data.csv',df.to_csv(index=False))
    return data

def test_complete_synthetic_calculation(tmp_path,monkeypatch):
    data=make_fixture(tmp_path)
    monkeypatch.setattr(run,'BASE',tmp_path)
    monkeypatch.setattr(run,'PERSONS',[data/'csv_pus.zip'])
    monkeypatch.setattr(run,'HOUSING',data/'csv_hus.zip')
    run.main()
    audit=json.loads((tmp_path/'audit.json').read_text())
    assert audit['person_records_read']==6
    assert audit['person_unique_households']==5
    assert audit['housing_records_read']==6
    assert audit['person_join_matched']==5
    assert audit['person_join_unmatched']==1
    assert audit['eligible_households_unweighted']==3
    assert audit['eligible_households_weighted']==80
    assert audit['excluded_households_total']==3
    assert audit['excluded_by_primary_reason']['unmatched_person_record']==1
    assert audit['excluded_by_primary_reason']['unsupported_tenure']==1
    assert audit['excluded_by_primary_reason']['missing_income']==1
    results=pd.read_csv(tmp_path/'results.csv')
    for plan in ('thrifty','low'):
        subset=results[(results.food_plan==plan)&(results.tenure=='all')].iloc[0]
        assert subset.households_unweighted==3
        assert subset.households_weighted==80
        assert subset.pct_below_housing_plus_food==12.5
        assert subset.ci_low==subset.ci_high==12.5 # all 80 replicate weights equal baseline
    assert (tmp_path/'manifest.json').exists()

def test_count_mismatch_fails_closed(tmp_path,monkeypatch):
    data=make_fixture(tmp_path,mismatch=True)
    monkeypatch.setattr(run,'BASE',tmp_path)
    monkeypatch.setattr(run,'PERSONS',[data/'csv_pus.zip'])
    monkeypatch.setattr(run,'HOUSING',data/'csv_hus.zip')
    with pytest.raises(ValueError,match='Person-count mismatch'):
        run.main()
    assert not (tmp_path/'results.csv').exists()
