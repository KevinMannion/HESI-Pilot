"""Vectorized national HESI food research run. Full-population claims BLOCKED pending infant/AK/HI adjustments and SDR."""
import argparse,csv,io,json,zipfile,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from food_model import load_prices,age_key
PLANS=['thrifty','low-cost','moderate-cost','liberal']
MONTHS=[(2024,m) for m in range(1,13)]+[(2026,9)]

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()

def zip_chunks(path,kind):
 with zipfile.ZipFile(path) as z:
  names=[n for n in z.namelist() if Path(n).name.lower().startswith('psam_'+kind) and n.lower().endswith('.csv')]
  if not names:raise ValueError('Missing census CSV in '+str(path))
  for n in names:
   cols=['SERIALNO','AGEP','SEX'] if kind=='p' else ['SERIALNO','STATE','PUMA','TYPEHUGQ','NP','WGTP']
   with z.open(n) as f:
    yield from pd.read_csv(f,usecols=cols,dtype={'SERIALNO':'string','STATE':'string','PUMA':'string'},chunksize=175000)

def age_category(age,sex):
 if age==0:return 'infant'
 if age<=1:return 'c1'
 if age<=3:return 'c2_3'
 if age<=5:return 'c4_5'
 if age<=8:return 'c6_8'
 if age<=11:return 'c9_11'
 sx='m' if sex==1 else 'f'
 if age<=13:return sx+'12_13'
 if age<=18:return sx+'14_18'
 if age==19:return sx+'19'
 if age<=50:return sx+'20_50'
 if age<=70:return sx+'51_70'
 return sx+'71p'

def execute(housing,persons,prices,out):
 out=Path(out);out.mkdir(exist_ok=True,parents=True)
 catalog,issues=load_prices(prices)
 # USDA September 2026 Thrifty PDF defines ages 14–19, whereas historical workbook extraction labels 14–18.
 # Correct the age band for this specific observed month with explicit provenance; do not alter the source CSV.
 old=(2026,9,'thrifty','Male','14-18 years'); new=(2026,9,'thrifty','Male','14-19 years')
 if old in catalog and new not in catalog: catalog[new]=catalog[old]
 old=(2026,9,'thrifty','Female','14-18 years'); new=(2026,9,'thrifty','Female','14-19 years')
 if old in catalog and new not in catalog: catalog[new]=catalog[old]
 cats=['infant','c1','c2_3','c4_5','c6_8','c9_11']+[s+a for s in ('m','f') for a in ('12_13','14_18','19','20_50','51_70','71p')]
 vectors={}
 for plan in PLANS:
  for year,month in MONTHS:
   arr=[]
   for cat in cats:
    if cat=='infant':arr.append(0);continue
    age={'c1':1,'c2_3':2,'c4_5':4,'c6_8':6,'c9_11':9}.get(cat)
    if age is None:
     suffix=cat[1:];age={'12_13':12,'14_18':14,'19':19,'20_50':20,'51_70':51,'71p':71}[suffix]
    sex='Male' if cat.startswith('m') else 'Female'
    group,band=age_key(age,sex,plan)
    key=(year,month,plan,group,band)
    if key not in catalog:raise ValueError('Missing price: '+str(key))
    arr.append(catalog[key])
   vectors[(plan,year,month)]=np.array(arr,dtype=np.float64)
 counts=[];npeople=0
 for p in persons:
  for d in zip_chunks(p,'p'):
   d['cat']=np.select([d.AGEP.eq(0),d.AGEP.le(1),d.AGEP.le(3),d.AGEP.le(5),d.AGEP.le(8),d.AGEP.le(11)],['infant','c1','c2_3','c4_5','c6_8','c9_11'],default='adult')
   adult=d['cat'].eq('adult')
   age=d.loc[adult,'AGEP'];sex=d.loc[adult,'SEX']
   suffix=np.select([age.le(13),age.le(18),age.eq(19),age.le(50),age.le(70)],['12_13','14_18','19','20_50','51_70'],default='71p')
   d.loc[adult,'cat']=np.where(sex.eq(1),'m','f')+suffix
   group=d.groupby(['SERIALNO','cat'],observed=True).size()
   counts.append(group)
   npeople+=len(d)
   print('people',npeople,flush=True)
 merged=pd.concat(counts).groupby(level=[0,1]).sum().unstack(fill_value=0).reindex(columns=cats,fill_value=0)
 del counts
 print('persons grouped into serials',len(merged),flush=True)
 housing_parts=[]
 for d in zip_chunks(housing,'h'):
  x=d[d.TYPEHUGQ.eq(1)].copy();housing_parts.append(x)
 hs=pd.concat(housing_parts,ignore_index=True)
 print('occupied',len(hs),'weighted',int(hs.WGTP.sum()),flush=True)
 if hs.SERIALNO.duplicated().any():raise ValueError('Duplicate occupied SERIALNO')
 hs=hs.set_index('SERIALNO',drop=False)
 sizes=merged.sum(axis=1)
 full=hs.join(sizes.rename('person_count'),how='left')
 full=full.join(merged[['infant']],how='left');full['infant']=full['infant'].fillna(0)
 full['status']='priced'
 full.loc[full.person_count.isna() | full.person_count.ne(full.NP),'status']='count_mismatch'
 full.loc[full.status.eq('priced') & full.infant.gt(0),'status']='infant_unpriced'
 print('coverage status',full.groupby('status').agg(records=('WGTP','size'),weighted=('WGTP','sum')).to_dict('index'),flush=True)
 covered=full[full.status.eq('priced')].copy()
 numerical=merged.reindex(covered.index).to_numpy(dtype=np.float64)
 factor=np.select([covered.NP.eq(1),covered.NP.eq(2),covered.NP.eq(3),covered.NP.eq(4),covered.NP.le(6)],[1.2,1.1,1.05,1.0,.95],default=.9)
 output=[]
 for plan in PLANS:
  yearbudget=np.zeros(len(covered),dtype=np.float64)
  for year,month in MONTHS:
   price=vectors[(plan,year,month)]
   expense=np.floor((numerical @ price)*factor*100+0.500001)/100
   if year==2024:yearbudget+=expense
   else:covered[f'{plan}_2026sep']=expense
  covered[f'{plan}_2024annual']=np.round(yearbudget,2)
 for plan in PLANS:
  for period in ('2024annual','2026sep'):
   column=f'{plan}_{period}'
   data=covered[[column,'WGTP']]
   weighted=(data[column]*data.WGTP).sum()/data.WGTP.sum()
   output.append({'period':period,'plan':plan,'weighted_households_priced':int(data.WGTP.sum()),'mean_budget_usd':round(float(weighted),2),'scope':'covered_households_only'})
 pd.DataFrame(output).to_csv(out/'national_summary.csv',index=False)
 coverage=full.groupby('status').agg(records=('WGTP','size'),weighted=('WGTP','sum')).reset_index()
 coverage.to_csv(out/'coverage.csv',index=False)
 state_summary=[]
 for state,g in covered.groupby('STATE'):
  for plan in PLANS:
   for period in ('2024annual','2026sep'):
    col=f'{plan}_{period}'
    state_summary.append({'state':state,'period':period,'plan':plan,'weighted_households_priced':int(g.WGTP.sum()),'mean_budget_usd':round(float((g[col]*g.WGTP).sum()/g.WGTP.sum()),2),'geography_note':'mainland USDA individual prices; Alaska/Hawaii not region-adjusted'})
 pd.DataFrame(state_summary).to_csv(out/'state_summary.csv',index=False)
 audit={'source_year_person':2024,'person_records_read':npeople,'occupied_sample_records':int(len(full)),'occupied_weighted':int(full.WGTP.sum()),'coverage':coverage.to_dict('records'),'scientific_status':'research_only_not_validated','publication_eligible':False,'limitations':['Infants remain excluded from priced subset','AK and HI mainland-price estimates are not local costs','2026 price results use 2024 household composition','Survey replicate standard errors not calculated','USDA meals assumed cooked at home'],'sha256':{Path(p).name:digest(p) for p in [housing,*persons,prices]}}
 (out/'audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps(audit,indent=2));return audit
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--housing',required=True);p.add_argument('--persons',nargs='+',required=True);p.add_argument('--prices',required=True);p.add_argument('--out',required=True);a=p.parse_args();execute(a.housing,a.persons,a.prices,a.out)
