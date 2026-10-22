"""HESI September 2026 three-cost scenario on a common ACS 2024 PUMS household frame.
NOT an approved nationally representative six-pillar HESI. The 12,000-mi one-car input is provisional.
"""
import argparse, json, zipfile, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

def sha256_file(path):
    digest=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()

def run(housing_zip,food_cache,composition_cache,geography,out,transport_annual=7264.70):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    food=pd.read_pickle(food_cache)[['thrifty_2026sep','n_person','n_infant']]
    comp=pd.read_pickle(composition_cache)
    geo=pd.read_csv(geography,dtype={'puma_geoid':str});geo=geo.loc[geo.status.eq('COMPLETE_UNAMBIGUOUS')].set_index('puma_geoid')
    if not food.index.is_unique or not comp.index.is_unique or not geo.index.is_unique:raise ValueError('Duplicate key in a lookup')
    fmrs=geo[[f'monthly_{i}br_benchmark' for i in range(5)]]
    totals={k:0 for k in ['raw_rows','occupied_rows','occupied_weight','geography_excluded_rows','geography_excluded_weight','composition_excluded_rows','composition_excluded_weight','over4_excluded_rows','over4_excluded_weight','infant_excluded_rows','infant_excluded_weight','included_rows','included_weight']}
    vals=np.zeros(6,dtype='float64') # food, housing, transport, combined, income, below income numerator
    den80=np.zeros(80);num80=np.zeros((80,5)); rep_below=np.zeros(80)
    wgroups={'owner':[0.,0.],'renter':[0.,0.],'rent_free':[0.,0.],'other_tenure':[0.,0.]}
    no_car_below=0.0; no_car_rep=np.zeros(80)
    outputs=[]
    cols=['SERIALNO','STATE','PUMA','TYPEHUGQ','NP','WGTP','HINCP','ADJINC','TEN']+[f'WGTP{i}' for i in range(1,81)]
    with zipfile.ZipFile(housing_zip) as z:
      members=sorted([n for n in z.namelist() if n.lower().split('/')[-1].startswith('psam_hus') and n.lower().endswith('.csv')]);assert len(members)>=1,members
      for member in members:
       for h in pd.read_csv(z.open(member),usecols=cols,dtype={'SERIALNO':str,'STATE':str,'PUMA':str},chunksize=100000):
        totals['raw_rows']+=len(h)
        h=h.loc[h.TYPEHUGQ.eq(1)&h.NP.gt(0)&h.WGTP.gt(0)].copy()
        totals['occupied_rows']+=len(h);totals['occupied_weight']+=float(h.WGTP.sum())
        h['puma_geoid']=h.STATE.str.zfill(2)+h.PUMA.str.zfill(5)
        good=h.puma_geoid.isin(geo.index)
        totals['geography_excluded_rows']+=int((~good).sum());totals['geography_excluded_weight']+=float(h.loc[~good,'WGTP'].sum())
        h=h.loc[good].copy()
        if h.empty:continue
        c=comp.reindex(h.SERIALNO);f=food.reindex(h.SERIALNO)
        valid=c[['adult','child','partner']].notna().all(axis=1).to_numpy() & f[['n_person','n_infant','thrifty_2026sep']].notna().all(axis=1).to_numpy()
        ad=c.adult.to_numpy(); ch=c.child.to_numpy(); pt=c.partner.to_numpy()
        valid &= ((ad+ch)==h.NP.to_numpy()) & (f.n_person.to_numpy()==h.NP.to_numpy()) & (pt<=ad) & (ad>=1)
        totals['composition_excluded_rows']+=int((~valid).sum());totals['composition_excluded_weight']+=float(h.loc[~valid,'WGTP'].sum())
        h=h.loc[valid].copy();c=c.iloc[np.flatnonzero(valid)];f=f.iloc[np.flatnonzero(valid)]
        if h.empty:continue
        br=(c.adult.to_numpy()-np.minimum(c.partner.to_numpy(),1)+np.ceil(c.child.to_numpy()/2)).astype(int)
        passbr=(br>=1)&(br<=4)
        totals['over4_excluded_rows']+=int((~passbr).sum());totals['over4_excluded_weight']+=float(h.loc[~passbr,'WGTP'].sum())
        h=h.iloc[np.flatnonzero(passbr)].copy();f=f.iloc[np.flatnonzero(passbr)];br=br[passbr]
        if h.empty:continue
        notinf=f.n_infant.to_numpy()==0
        totals['infant_excluded_rows']+=int((~notinf).sum());totals['infant_excluded_weight']+=float(h.loc[~notinf,'WGTP'].sum())
        h=h.iloc[np.flatnonzero(notinf)].copy();f=f.iloc[np.flatnonzero(notinf)];br=br[notinf]
        if h.empty:continue
        r=fmrs.reindex(h.puma_geoid).to_numpy(dtype=float)
        rent=r[np.arange(len(h)),br]
        n=h.NP.to_numpy();factor=np.select([n==1,n==2,n==3,n==4,n<=6],[1.2,1.1,1.05,1.,.95],default=.9)
        meal=np.round(f.thrifty_2026sep.to_numpy(dtype=float)*factor,2)
        car=float(transport_annual)/12
        inc=h.HINCP.to_numpy(dtype=float)*h.ADJINC.to_numpy(dtype=float)/1e6/12
        eligible=np.isfinite(rent)&np.isfinite(meal)&np.isfinite(inc)
        if not eligible.all():raise ValueError('Nonfinite cost/income; add explicit exclusion audit')
        w=h.WGTP.to_numpy(dtype=float)
        joint=rent+meal+car
        # Same-household additive cost, conditional on all eligible households assigned one car.
        base=np.column_stack([meal,rent,np.full(len(h),car),joint,inc])
        vals[:5]+=w@base; vals[5]+=w@(inc<joint)
        no_car_below+=w@(inc<(rent+meal))
        reps=h[[f'WGTP{i}' for i in range(1,81)]].to_numpy(float)
        den80+=reps.sum(axis=0);num80+=reps.T@base;rep_below+=reps.T@(inc<joint).astype(float)
        no_car_rep+=reps.T@(inc<(rent+meal)).astype(float)
        totals['included_rows']+=len(h);totals['included_weight']+=w.sum()
        for tenure,k in [('owner',h.TEN.isin([1,2]).to_numpy()),('renter',h.TEN.eq(3).to_numpy()),('rent_free',h.TEN.eq(4).to_numpy()),('other_tenure',~h.TEN.isin([1,2,3,4]).to_numpy())]:
            wgroups[tenure][0]+=w[k].sum();wgroups[tenure][1]+=(w[k]*joint[k]).sum()
       print('processed',member,'eligible so far',totals['included_rows'],flush=True)
    assert abs(sum(totals[k+'_weight'] for k in ['geography_excluded','composition_excluded','over4_excluded','infant_excluded','included'])-totals['occupied_weight'])<2
    m=vals[:5]/totals['included_weight'];p=vals[5]/totals['included_weight']
    mr=num80/den80[:,None];pr=rep_below/den80
    se=np.sqrt((4/80)*((mr-m)**2).sum(axis=0));pse=np.sqrt((4/80)*((pr-p)**2).sum())
    labels=['food_month','housing_month','one_vehicle_month_PROVISIONAL','total_month_PROVISIONAL','income_month_2024_vintage']
    result=[]
    for i,label in enumerate(labels):result.append({'metric':label,'mean':m[i],'se_sdr':se[i],'ci90_low':m[i]-1.645*se[i],'ci90_high':m[i]+1.645*se[i]})
    result.append({'metric':'share_income_below_three_costs_PROVISIONAL','mean':p,'se_sdr':pse,'ci90_low':p-1.645*pse,'ci90_high':p+1.645*pse})
    no_car=no_car_below/totals['included_weight']; no_car_replicates=no_car_rep/den80
    no_car_se=np.sqrt((4/80)*((no_car_replicates-no_car)**2).sum())
    result.append({'metric':'share_below_cost_NO_CAR_sensitivity','mean':no_car,'se_sdr':no_car_se,'ci90_low':no_car-1.645*no_car_se,'ci90_high':no_car+1.645*no_car_se})
    pd.DataFrame(result).to_csv(out/'common_cohort_results.csv',index=False)
    pd.DataFrame({'replicate':range(1,81),**{labels[j]:mr[:,j] for j in range(5)},'share_below':pr,'share_below_no_car':no_car_replicates}).to_csv(out/'replicate_results.csv',index=False)
    input_paths={'acs_housing_zip':housing_zip,'food_person_cache':food_cache,'composition_person_cache':composition_cache,'puma_fmr_table':geography}
    audit={'input_sha256':{key:{'sha256':sha256_file(path),'size_bytes':Path(path).stat().st_size,'basename':Path(path).name} for key,path in input_paths.items()},'frame':totals,'tenure_groups':wgroups,'status':'RESEARCH_ONLY','reference':'September 2026 USDA and HUD costs; 2024 ACS composition AND 2024 income; one assumed 12000-mile vehicle','limitations':['One vehicle per included household is a sensitivity scenario, not supported mobility allocation','Income is 2024, not a 2026 nowcast','PUMA rent is modeled area mean not actual household location','Infant-containing households excluded','Households needing >4 bedrooms excluded','No healthcare, childcare, essentials or taxes','Replicate intervals capture ACS survey sampling only, not price, geographical, household-mobility, or model uncertainty']}
    assert abs(sum(z[0] for z in wgroups.values())-totals['included_weight'])<2, 'Tenure groups fail weighted reconciliation'
    audit['execution_status']='EXECUTED_BY_AUTHOR_NOT_INDEPENDENTLY_REPRODUCED'
    (out/'audit.json').write_text(json.dumps(audit,indent=2));print(pd.DataFrame(result).to_string(index=False));return audit

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for x in ['housing-zip','food-cache','composition-cache','geography','out']:p.add_argument('--'+x,required=True)
 a=p.parse_args();run(a.housing_zip,a.food_cache,a.composition_cache,a.geography,a.out)
