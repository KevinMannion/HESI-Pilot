"""Survey sampling uncertainty for v4.8 covered household USDA-modeled food budgets.
Inputs: official ACS 2024 national housing PUMS ZIP and the v4.8 cached household food aggregation.
A conditional model-based mean; excludes infant-containing households, mainland rate used in AK/HI.
"""
import argparse,hashlib,json,zipfile,math
from pathlib import Path
import numpy as np,pandas as pd
COLS=[f'WGTP{i}' for i in range(1,81)]
COSTS=[f'{p}_{period}' for p in ('thrifty','low-cost','moderate-cost','liberal') for period in ('2024annual','2026sep')]

def run(housing_zip,person_pickle,out_dir):
    dest=Path(out_dir);dest.mkdir(exist_ok=True,parents=True)
    person=pd.read_pickle(person_pickle)
    if person.index.has_duplicates: raise ValueError('duplicate person household identifiers')
    costmat=person[COSTS].to_numpy(dtype='float64')
    # Build indexed lookup from cached person data, so a full housing/person join is unnecessary
    person['__ix']=np.arange(len(person),dtype=np.int32)
    n=0; total=0.; ncovered=0; wcovered=0.; infantn=0; infantw=0.; mismatchn=0; mismatchw=0.
    sums=np.zeros(8); rep_sums=np.zeros((80,8));rep_den=np.zeros(80)
    collist=['SERIALNO','WGTP','TYPEHUGQ','NP','STATE']+COLS
    with zipfile.ZipFile(housing_zip) as z:
        members=[x for x in z.namelist() if x.lower().endswith('.csv') and x.lower().split('/')[-1].startswith('psam_hus')]
        if len(members)!=2:raise ValueError(f'Expected two housing CSVs, found {members}')
        for member in members:
            for chunk in pd.read_csv(z.open(member),usecols=collist,dtype={'SERIALNO':str,'STATE':str},chunksize=65000):
                occupied=chunk.loc[(chunk.TYPEHUGQ==1)&(chunk.NP>0)&(chunk.WGTP>0)]
                n+=len(occupied);total+=float(occupied.WGTP.sum())
                ix=person['__ix'].reindex(occupied.SERIALNO).to_numpy()
                present=np.isfinite(ix)
                member_counts=np.zeros(len(occupied),dtype=bool)
                infant=np.zeros(len(occupied),dtype=bool)
                if present.any():
                    original=costmat[ix[present].astype(int)]
                    relevant=person.iloc[ix[present].astype(int)]
                    member_counts[present]=relevant.n_person.to_numpy()==occupied.NP.to_numpy()[present]
                    infant[present]=relevant.n_infant.to_numpy()>0
                good=present&member_counts&~infant
                bad=~present|~member_counts
                mismatchn+=int(bad.sum());mismatchw+=float(occupied.WGTP.to_numpy()[bad].sum())
                infantn+=int((~bad&infant).sum());infantw+=float(occupied.WGTP.to_numpy()[~bad&infant].sum())
                if not good.any():continue
                x=costmat[ix[good].astype(int)].copy()
                sizes=occupied.NP.to_numpy()[good]
                factor=np.select([sizes==1,sizes==2,sizes==3,sizes==4,sizes<=6],[1.2,1.1,1.05,1.,.95],default=.9)
                x=np.round(x*factor[:,None],2)
                w=occupied.WGTP.to_numpy(dtype='float64')[good]
                r=occupied.loc[good,COLS].to_numpy(dtype='float64')
                sums+=w@x
                rep_sums+=r.T@x
                rep_den+=r.sum(axis=0)
                ncovered+=int(good.sum()); wcovered+=float(w.sum())
            print('Finished',member,'occupied so far',n,flush=True)
    mean=sums/wcovered
    means=rep_sums/rep_den[:,None]
    se=np.sqrt((4./80.)*np.square(means-mean).sum(axis=0))
    results=[]
    for i,key in enumerate(COSTS):
        results.append({'measure':key,'weighted_mean':float(mean[i]),'standard_error':float(se[i]),'moe_90':float(1.645*se[i]),'ci_90_low':float(mean[i]-1.645*se[i]),'ci_90_high':float(mean[i]+1.645*se[i]),'covered_unweighted':ncovered,'covered_weighted':int(wcovered)})
    pd.DataFrame(results).to_csv(dest/'food_sampling_uncertainty.csv',index=False)
    status={'occupied_sample_households':n,'occupied_weighted_households':int(total),'covered_sample_households':ncovered,'covered_weighted_households':int(wcovered),'infant_excluded_sample':infantn,'infant_excluded_weighted':int(infantw),'member_mismatch_sample':mismatchn,'member_mismatch_weighted':int(mismatchw),'replicate_count':80,'method':'ACS PUMS 80 household replicate weights SDR variance factor 4/80; 90% normal MOE 1.645*SE','scope':'conditional covered-household food-model average only','publication_eligible':False,'limitations':['Sampling error conditional on USDA model only','Infant households excluded','Mainland food prices used in Alaska/Hawaii','2026 uses 2024 household mix','Independent validation and model uncertainty pending']}
    (dest/'audit.json').write_text(json.dumps(status,indent=2))
    pd.DataFrame({'replicate':range(1,81),**{name:means[:,j] for j,name in enumerate(COSTS)}}).to_csv(dest/'replicate_means.csv',index=False)
    print(json.dumps(status,indent=2));print(pd.DataFrame(results).to_string(index=False));return status

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--housing-zip',required=True);ap.add_argument('--person-cache',required=True);ap.add_argument('--out',required=True); a=ap.parse_args();run(a.housing_zip,a.person_cache,a.out)
