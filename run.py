"""HESI research pilot: Dec 2024 USDA age-sex Thrifty/Low-cost food + ACS housing; not a complete essential-cost index."""
import numpy as np,pandas as pd,zipfile,pathlib,json,hashlib
BASE = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE / 'input_data'

# Support original Census csv_pus.zip directly, with fallback to split parts for backward compatibility
if (DATA_DIR / 'csv_pus.zip').exists():
    PERSONS = [DATA_DIR / 'csv_pus.zip']
else:
    PERSONS = [DATA_DIR / 'HESI_Person_Part_1.zip', DATA_DIR / 'HESI_Person_Part_2.zip']

HOUSING = DATA_DIR / 'csv_hus.zip'
# Official USDA monthly food plan tables issued Jan 2025; December 2024 (USD); age 0 extrapolation via age 1 value (flagged)
# child age bands; adult male/female ages 12+; table footnotes apply size economies
T_CHILD={'thrifty':[110.7,166.5,181.6,201.7,233.2],'low':[157.7,164.4,171,245.2,258.1]}
T_M={'thrifty':[249.3,314.5,307.4,272.3,259.9],'low':[301.4,307.1,303.6,285.4,283.6]}
T_F={'thrifty':[215.7,250.1,245.6,228.6,251.4],'low':[256.9,258.7,263.7,256.6,256.6]}
def costs(age,sex,plan):
    child=np.select([age<=1,age<=3,age<=5,age<=8,age<=11],T_CHILD[plan],default=np.nan)
    band=np.select([age<=13,age<=19 if plan=='thrifty' else age<=18,age<=50,age<=70],[0,1,2,3],default=4).astype(int)
    # Low-cost adult schedule begins at age 19; thrifty at 20. 19 year olds assigned low adult band 19-50.
    if plan=='low': band=np.select([age<=13,age<=18,age<=50,age<=70],[0,1,2,3],default=4).astype(int)
    return np.where(age<=11,child,np.where(sex==1,np.array(T_M[plan])[band],np.array(T_F[plan])[band]))
def factor(n):return np.select([n==1,n==2,n==3,n==4,n<=6],[1.2,1.1,1.05,1.,.95],default=.9)
def main():
    audit = {'person_records_read': 0, 'person_unique_households': 0, 'housing_records_read': 0, 'occupied_records_np_positive': 0, 'person_join_matched': 0, 'person_join_unmatched': 0, 'person_count_mismatch': 0, 'eligible_households_unweighted': 0, 'eligible_households_weighted': 0, 'excluded_by_primary_reason': {k: 0 for k in ('nonoccupied_or_zero_persons','unmatched_person_record','person_count_mismatch','unsupported_tenure','missing_income','missing_housing_cost','nonpositive_weight','invalid_adjustment_factor')}}
    parts=[]
    for p in PERSONS:
     with zipfile.ZipFile(p) as z:
      for member in z.namelist():
       if not member.endswith('.csv'):continue
       for d in pd.read_csv(z.open(member),usecols=['SERIALNO','AGEP','SEX'],chunksize=180000):
        audit['person_records_read'] += len(d)
        a=d.AGEP.to_numpy();s=d.SEX.to_numpy()
        d['thrifty']=costs(a,s,'thrifty');d['low']=costs(a,s,'low')
        parts.append(d.groupby('SERIALNO',sort=False).agg(persons=('AGEP','size'),thrifty=('thrifty','sum'),low=('low','sum')))
        print('person chunk',len(d),flush=True)
    # sum chunk groups safely across CSV boundaries
    agg=pd.concat(parts).groupby(level=0,sort=False).sum()
    audit['person_unique_households'] = len(agg)
    print('unique households in people',len(agg),flush=True)
    acc={(plan,group):{'den':np.zeros(81),'num':np.zeros(81),'covered':0,'n':0} for plan in ('thrifty','low') for group in ('all','renter','owner')}
    for p in [HOUSING]:
     with zipfile.ZipFile(p) as z:
      for member in z.namelist():
       if not member.endswith('.csv'):continue
       cols=['SERIALNO','NP','TEN','HINCP','ADJINC','ADJHSG','GRNTP','SMOCP','WGTP']+[f'WGTP{k}' for k in range(1,81)]
       for d in pd.read_csv(z.open(member),usecols=cols,chunksize=65000):
        d=d.join(agg,on='SERIALNO',how='left')
        audit['housing_records_read'] += len(d)
        occupied=(d.NP>0)
        matched=occupied & d.persons.notna()
        mismatched=matched & (d.NP != d.persons)
        audit['occupied_records_np_positive'] += int(occupied.sum())
        audit['person_join_matched'] += int(matched.sum())
        audit['person_join_unmatched'] += int((occupied & ~matched).sum())
        audit['person_count_mismatch'] += int(mismatched.sum())
        if mismatched.any():
         raise ValueError(f"Person-count mismatch in {int(mismatched.sum())} housing record(s); no results written")
        housing=np.where(d.TEN==3,d.GRNTP,np.where(d.TEN.isin([1,2]),d.SMOCP,np.nan))
        valid=(d.NP>0)&d.persons.notna()&d.TEN.isin([1,2,3])&d.HINCP.notna()&np.isfinite(housing)&(d.WGTP>0)&(d.ADJHSG>0)&(d.ADJINC>0)
        # Mutually exclusive primary exclusion reasons, in the same order as the validity gate.
        remaining=np.ones(len(d), dtype=bool)
        checks=(('nonoccupied_or_zero_persons',occupied.to_numpy()),
                ('unmatched_person_record',d.persons.notna().to_numpy()),
                ('person_count_mismatch',~mismatched.to_numpy()),
                ('unsupported_tenure',d.TEN.isin([1,2,3]).to_numpy()),
                ('missing_income',d.HINCP.notna().to_numpy()),
                ('missing_housing_cost',np.isfinite(housing)),
                ('nonpositive_weight',(d.WGTP>0).to_numpy()),
                ('invalid_adjustment_factor',((d.ADJHSG>0)&(d.ADJINC>0)).to_numpy()))
        for reason,passed in checks:
         newly_excluded=remaining & ~passed
         audit['excluded_by_primary_reason'][reason] += int(newly_excluded.sum())
         remaining &= passed
        assert np.array_equal(remaining,valid.to_numpy())
        audit['eligible_households_unweighted'] += int(valid.sum())
        audit['eligible_households_weighted'] += float(d.loc[valid,'WGTP'].sum())
        x=d[valid].copy()
        if x.empty:continue
        inc=x.HINCP.to_numpy(float)*x.ADJINC.to_numpy(float)/1e6
        h=np.where(x.TEN==3,x.GRNTP,x.SMOCP)*x.ADJHSG.to_numpy(float)/1e6 *12
        w=x[['WGTP']+[f'WGTP{k}' for k in range(1,81)]].to_numpy(float)
        n=x.persons.to_numpy(float)
        for plan in ('thrifty','low'):
         food=x[plan].to_numpy(float)*factor(n)*12
         hardship=((inc<h+food)).astype(float)
         for group,mask in [('all',np.ones(len(x),bool)),('renter',x.TEN.to_numpy()==3),('owner',x.TEN.isin([1,2]).to_numpy())]:
          a=acc[(plan,group)]; ww=w[mask];a['den']+=ww.sum(axis=0);a['num']+=(ww*hardship[mask,None]).sum(axis=0);a['n']+=mask.sum()
        print('household chunk',len(d),flush=True)
    rows=[]
    for (plan,group),a in acc.items():
     p=a['num']/a['den']; se=np.sqrt(.05*np.sum((p[1:]-p[0])**2))
     rows.append(dict(food_plan=plan,tenure=group,households_unweighted=int(a['n']),households_weighted=round(a['den'][0]),pct_below_housing_plus_food=round(p[0]*100,3),ci_low=round(max(0,p[0]-1.96*se)*100,3),ci_high=round(min(1,p[0]+1.96*se)*100,3)))
    pd.DataFrame(rows).to_csv(BASE/'results.csv',index=False)
    (BASE/'manifest.json').write_text(json.dumps({'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PERSONS+[HOUSING]},'USDA':['https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Thrifty_Food_Plan_December_2024.pdf','https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Low_Moderate_Liberal_Food_Plans_December_2024.pdf'],'reference_period':'December 2024 monthly food prices applied to full-year annual household income','limitation':'Not a complete essentials budget; taxes, healthcare, childcare, transport excluded. No 2024 full-year food average. Age-0 uses age-1 USDA estimate. Adult male low-cost groups use 19-50. Annualizing December 2024 prices is a scenario, not average 2024.', 'weight':'ACS WGTP and WGTP1-80, 4/80 variance'},indent=2))
    audit['eligible_households_weighted'] = round(audit['eligible_households_weighted'])
    audit['excluded_households_total'] = sum(audit['excluded_by_primary_reason'].values())
    assert audit['housing_records_read'] == audit['eligible_households_unweighted'] + audit['excluded_households_total']
    (BASE/'audit.json').write_text(json.dumps(audit,indent=2))
    print(pd.DataFrame(rows).to_string(index=False),flush=True)


if __name__ == "__main__":
    main()
