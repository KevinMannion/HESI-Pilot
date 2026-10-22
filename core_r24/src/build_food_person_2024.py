"""Legacy raw person-data rebuild, requires external Census person PUMS plus historical USDA prices (included). NOT used by the R2.3 national replication."""
from pathlib import Path
import numpy as np, pandas as pd, json, hashlib
from fast_national_food import zip_chunks, PLANS, MONTHS
from food_model import load_prices, age_key

def run(housing, persons, prices, out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 catalog, issues=load_prices(prices)
 if [i for i in issues if i['type']=='conflicting_duplicate' and i['key'][0] in (2024,2026)]:raise ValueError('Relevant duplicate source keys')
 # The USDA source workbook mislabels September 2026 TFP 14-19 as 14-18; use PDF-correct label.
 for s in ('Male','Female'):
  old=(2026,9,'thrifty',s,'14-18 years');new=(2026,9,'thrifty',s,'14-19 years')
  if old in catalog and new not in catalog:catalog[new]=catalog[old]
 # 15 common person categories, plus age 19 handled explicitly by plan-specific lookup.
 groups=[('Child',1),('Child',2),('Child',4),('Child',6),('Child',9)] + [(s,a) for s in ('Male','Female') for a in (12,14,19,20,51,71)]
 price_matrix=[]
 for plan in PLANS:
  annual=[]
  for group,age in groups:
   sx=group if group!='Child' else None
   g,band=age_key(age,sx,plan)
   annual.append(sum(catalog[(2024,m,plan,g,band)] for m in range(1,13)))
  price_matrix.append(annual)
  monthly=[]
  for group,age in groups:
   sx=group if group!='Child' else None
   g,band=age_key(age,sx,plan)
   monthly.append(catalog[(2026,9,plan,g,band)])
  price_matrix.append(monthly)
 prices_array=np.array(price_matrix,dtype=np.float64)
 outputcols=[f'{p}_{per}' for p in PLANS for per in ('2024annual','2026sep')]
 # Person files sorted by serial. Aggregate per chunk, dropping enormous category MultiIndex.
 cache=out/'person_aggregates.pkl'
 if cache.exists():
  personagg=pd.read_pickle(cache);npeople=3422888;print('loaded cached person aggregates',len(personagg),flush=True)
 else:
  pieces=[]; npeople=0
  for p in persons:
   for d in zip_chunks(p,'p'):
    a=d.AGEP.to_numpy(dtype=np.int16);s=d.SEX.to_numpy(dtype=np.int8)
    category=np.select([a==1,(a>=2)&(a<=3),(a>=4)&(a<=5),(a>=6)&(a<=8),(a>=9)&(a<=11)],list(range(5)),default=-1)
    for ix,sex in enumerate((1,2)):
     offset=5+ix*6
     for k,(lo,hi) in enumerate([(12,13),(14,18),(19,19),(20,50),(51,70),(71,120)]):
      category[(a>=lo)&(a<=hi)&(s==sex)]=offset+k
    usable=(category>=0)
    if (~usable & (a!=0)).any():raise ValueError('Unmapped person age/sex group')
    x=np.zeros((len(d),8),dtype=np.float64)
    x[usable]=prices_array[:,category[usable]].T
    agg=pd.DataFrame(x,columns=outputcols)
    agg.insert(0,'SERIALNO',d.SERIALNO.to_numpy());agg['n_person']=1;agg['n_infant']=(a==0).astype('int8')
    pieces.append(agg.groupby('SERIALNO',sort=False).sum())
    npeople+=len(d)
   print('person file complete',Path(p).name,'rows',npeople,flush=True)
  print('aggregating chunk summaries',len(pieces),flush=True)
  personagg=pd.concat(pieces).groupby(level=0,sort=False).sum();del pieces
  personagg.to_pickle(cache);print('cached person aggregate',cache,flush=True)
  print('unique person identifiers',len(personagg),flush=True)
 housingparts=[]
 for fpath in housing:
  for d in pd.read_csv(fpath,dtype={'SERIALNO':'string','STATE':'string'},chunksize=300000):
   housingparts.append(d[d.TYPEHUGQ.eq(1)&d.WGTP.gt(0)&d.NP.gt(0)].copy())
 hs=pd.concat(housingparts,ignore_index=True);del housingparts
 if hs.SERIALNO.duplicated().any():raise ValueError('Duplicate SERIALNO in housing')
 hs=hs.set_index('SERIALNO',drop=False)
 print('households',len(hs),'weighted',hs.WGTP.sum(),flush=True)
 merged=hs.join(personagg,how='left');del personagg
 merged['status']='priced'
 merged.loc[merged.n_person.isna()|merged.n_person.ne(merged.NP),'status']='count_mismatch'
 merged.loc[(merged.status=='priced')&(merged.n_infant>0),'status']='infant_unpriced'
 counts=merged.groupby('status').agg(records=('WGTP','size'),households=('WGTP','sum'))
 print(counts.to_string(),flush=True)
 covered=merged[merged.status.eq('priced')].copy()
 f=np.select([covered.NP.eq(1),covered.NP.eq(2),covered.NP.eq(3),covered.NP.eq(4),covered.NP.le(6)],[1.2,1.1,1.05,1,.95],default=.9)
 for col in outputcols:covered[col]=np.round(covered[col]*f,2)
 records=[];states=[]
 for col in outputcols:
  records.append({'plan':col.rsplit('_',1)[0],'period':col.rsplit('_',1)[1], 'weighted_mean_covered':float(np.average(covered[col],weights=covered.WGTP)), 'weighted_households_covered':int(covered.WGTP.sum()),'unweighted_households_covered':len(covered)})
 for state,g in covered.groupby('STATE'):
  for col in outputcols:
   states.append({'state':state,'plan':col.rsplit('_',1)[0],'period':col.rsplit('_',1)[1],'weighted_mean_covered':float(np.average(g[col],weights=g.WGTP)),'weighted_households_covered':int(g.WGTP.sum())})
 pd.DataFrame(records).to_csv(out/'national_summary.csv',index=False)
 pd.DataFrame(states).to_csv(out/'state_summary.csv',index=False)
 counts.reset_index().to_csv(out/'coverage.csv',index=False)
 audit={'person_records_read':npeople,'occupied_records':len(hs),'occupied_weighted':int(hs.WGTP.sum()),'coverage':counts.reset_index().to_dict('records'),'publication_eligible':False,'status':'research_only','limitations':['Infant-containing households not priced','Uses mainland USDA reference values for Alaska and Hawaii','2026 values applied to 2024 household composition','Household prices are sum of rounded person cost cells; inflation and model assumptions not tested','SDR replicate sampling uncertainty pending']}
 (out/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2));return audit
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--housing',nargs='+',required=True);a.add_argument('--persons',nargs='+',required=True);a.add_argument('--prices',required=True);a.add_argument('--out',required=True);x=a.parse_args();run(x.housing,x.persons,x.prices,x.out)
