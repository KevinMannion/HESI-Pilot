"""Rebuild joint model's two person-level inputs from original ACS PUMS person ZIPs."""
import argparse,sys,zipfile,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from food_model import load_prices,age_key

def main():
 a=argparse.ArgumentParser();a.add_argument('--person-zips',nargs='+',required=True);a.add_argument('--prices',default=str(ROOT/'inputs/source_2024_2026.csv'));a.add_argument('--out',default=str(ROOT/'data'));x=a.parse_args()
 out=Path(x.out);out.mkdir(parents=True,exist_ok=True)
 catalog,issues=load_prices(x.prices)
 for s in ('Male','Female'):
  old=(2026,9,'thrifty',s,'14-18 years');new=(2026,9,'thrifty',s,'14-19 years')
  if old in catalog and new not in catalog:catalog[new]=catalog[old]
 categories=[('Child',1),('Child',2),('Child',4),('Child',6),('Child',9)]+[(s,a) for s in ('Male','Female') for a in (12,14,19,20,51,71)]
 values=[]
 for s,a in categories:
  sex=None if s=='Child' else s
  key=age_key(a,sex,'thrifty');values.append(catalog[(2026,9,'thrifty',*key)])
 value=np.array(values)
 foods=[];comps=[];count=0
 for file in x.person_zips:
  tag=hashlib.sha256(str(Path(file).resolve()).encode()).hexdigest()[:12]
  fp=out/('food_part_'+tag+'.pkl'); cp=out/('composition_part_'+tag+'.pkl')
  if fp.exists() and cp.exists():
   foods.append(pd.read_pickle(fp));comps.append(pd.read_pickle(cp));print('Resumed',file,flush=True);continue
  filefoods=[];filecomps=[]
  with zipfile.ZipFile(file) as z:
   members=[n for n in z.namelist() if Path(n).name.lower().startswith('psam_pus') and n.lower().endswith('.csv')]
   if not members:raise ValueError('Missing person CSV '+file)
   for member in members:
    for d in pd.read_csv(z.open(member),usecols=['SERIALNO','AGEP','SEX','RELSHIPP'],dtype={'SERIALNO':str},chunksize=175000):
     age=d.AGEP.to_numpy();sex=d.SEX.to_numpy();rel=d.RELSHIPP.to_numpy()
     cat=np.select([age==1,(age>=2)&(age<=3),(age>=4)&(age<=5),(age>=6)&(age<=8),(age>=9)&(age<=11)],[0,1,2,3,4],default=-1)
     for ix,sexcode in enumerate((1,2)):
      for j,(lo,hi) in enumerate([(12,13),(14,18),(19,19),(20,50),(51,70),(71,120)]):cat[(age>=lo)&(age<=hi)&(sex==sexcode)]=5+ix*6+j
     if ((cat<0)&(age!=0)).any():raise ValueError('Unknown person category')
     food=pd.DataFrame({'SERIALNO':d.SERIALNO,'thrifty_2026sep':np.where(cat>=0,value[np.maximum(cat,0)],0),'n_person':1,'n_infant':(age==0).astype('int8')})
     filefoods.append(food.groupby('SERIALNO',sort=False)[['thrifty_2026sep','n_person','n_infant']].sum())
     comp=pd.DataFrame({'SERIALNO':d.SERIALNO,'adult':(age>=18).astype('int8'),'partner':np.isin(rel,[21,22,23,24]).astype('int8'),'male_child':((age<18)&(sex==1)).astype('int8'),'female_child':((age<18)&(sex==2)).astype('int8'),'young_child':(age<6).astype('int8'),'child':(age<18).astype('int8')})
     filecomps.append(comp.groupby('SERIALNO',sort=False)[['adult','partner','male_child','female_child','young_child','child']].sum())
     count+=len(d)
  onefood=pd.concat(filefoods).groupby(level=0).sum();onecomp=pd.concat(filecomps).groupby(level=0).sum()
  onefood.to_pickle(fp);onecomp.to_pickle(cp);foods.append(onefood);comps.append(onecomp)
  print('Checkpoint',file,'persons:',count,flush=True)
 food=pd.concat(foods).groupby(level=0).sum();comp=pd.concat(comps).groupby(level=0).sum()
 food.to_pickle(out/'acs2024_food_person_aggregates.pkl');comp.to_pickle(out/'acs2024_person_composition.pkl')
 print('SUMMARY',json.dumps({'person_rows':count,'households_food':len(food),'households_composition':len(comp)}),flush=True)
 seen=set()
 for file in x.person_zips:
  with zipfile.ZipFile(file) as z:
   for n in z.namelist():
    name=Path(n).name.lower()
    if name.startswith('psam_pus') and name.endswith('.csv'):
     seen.add(name)
 if seen!={'psam_pusa.csv','psam_pusb.csv'}:
  raise RuntimeError('Need both ACS person CSVs psam_pusa.csv and psam_pusb.csv; found '+str(sorted(seen)))
if __name__=='__main__':main()
