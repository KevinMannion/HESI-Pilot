import pandas as pd,numpy as np,zipfile,pathlib,json,hashlib
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--person-zips', nargs='+',required=True)
parser.add_argument('--out',required=True)
args=parser.parse_args()
O=pathlib.Path(args.out); O.mkdir(parents=True,exist_ok=True)
if (O/'person_composition.pkl').exists():
 print('Checkpoint already exists');quit()
pieces=[]; person_total=0
for zp in map(pathlib.Path,args.person_zips):
 with zipfile.ZipFile(zp) as z:
  with z.open(z.namelist()[0]) as stream:
   for part in pd.read_csv(stream,usecols=['SERIALNO','AGEP','SEX','RELSHIPP'],dtype={'SERIALNO':str},chunksize=180000):
    person_total+=len(part)
    age=part.AGEP.to_numpy();rel=part.RELSHIPP.to_numpy();sex=part.SEX.to_numpy()
    # One reference-person partnership can share a sleeping room; no relationship among other adults is inferred.
    part['adult']=(age>=18).astype('int8')
    part['partner']=np.isin(rel,[21,22,23,24]).astype('int8')
    part['male_child']=((age<18)&(sex==1)).astype('int8')
    part['female_child']=((age<18)&(sex==2)).astype('int8')
    part['young_child']=(age<6).astype('int8')
    part['child']=(age<18).astype('int8')
    pieces.append(part.groupby('SERIALNO',sort=False)[['adult','partner','male_child','female_child','young_child','child']].sum())
 print('person file',zp.name,'processed',person_total,flush=True)
agg=pd.concat(pieces).groupby(level=0).sum();del pieces
print('person household aggregates',len(agg),flush=True)

agg.to_pickle(O/'person_composition.pkl')
(O/'person_checkpoint.json').write_text(json.dumps({'person_rows':person_total,'household_groups':len(agg)}))
print('SAVED CHECKPOINT',flush=True)
