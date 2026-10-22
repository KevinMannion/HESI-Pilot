"""HESI three-component source-to-result reproduction. Requires original Census PUMS ZIPs."""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
import numpy as np,pandas as pd
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'tools'))
from pums_archive import person_zip_args, verify_housing_zip
HASHES={
 'housing':'8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0',
 'person_a':'05a4bdcb84fa8af1f3cc3034d9776a0a96e4311907fbb497298ff31bd445e6d8',
 'person_b':'2a891e40a44dec1374b9885926e20bc275c5ee93d6a55a12d0386893d091712c',
 'geography':'210a7ec6ae756ca8034cf3b7bff8afb3480d53186834cc7b304b913445f2a3ee',
 'prices':'90bc39d1a569073b9530ca0a78a4ccf19c781c4a42dd70c51a0bed9e1907602c'}
def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def check_results(generated):
 ref=P/'results/national_R22'
 a=pd.read_csv(ref/'common_cohort_results.csv').set_index('metric'); b=pd.read_csv(generated/'common_cohort_results.csv').set_index('metric')
 for metric in a.index:
  for field in ('mean','se_sdr','ci90_low','ci90_high'):
   if not np.isclose(a.loc[metric,field],b.loc[metric,field],atol=1e-7,rtol=0):raise AssertionError(f'{metric}.{field}: {a.loc[metric,field]} vs {b.loc[metric,field]}')
 old=pd.read_csv(ref/'replicate_results.csv'); new=pd.read_csv(generated/'replicate_results.csv')
 for field in old.columns:
  if not np.allclose(old[field],new[field],atol=1e-7,rtol=0):raise AssertionError('80 SDR replicates differ: '+field)
 oldaudit=json.loads((ref/'audit.json').read_text());newaudit=json.loads((generated/'audit.json').read_text())
 if oldaudit['frame']!=newaudit['frame']:raise AssertionError('Population / exclusion cascade mismatched')
 return {'status':'PASS','metrics_compared':len(a),'replicates_compared':80,'frame_exact':True}
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--housing',type=Path);ap.add_argument('--person-a',type=Path);ap.add_argument('--person-b',type=Path)
 ap.add_argument('--person-official',type=Path,help='Census csv_pus.zip; verified by inner CSV SHA-256, not by pretending it matches the split ZIP hashes')
 ap.add_argument('--output',type=Path,default=P/'local_reproduction')
 ap.add_argument('--check-existing',type=Path,help='Validate completed run without reprocessing inputs')
 x=ap.parse_args();env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 if x.check_existing:
  verdict=check_results(x.check_existing);print(json.dumps(verdict,indent=2));return
 if not x.housing:ap.error('Provide --housing')
 if x.person_official and (x.person_a or x.person_b):ap.error('Use either --person-official or both --person-a and --person-b')
 if not x.person_official and not all([x.person_a,x.person_b]):ap.error('Provide --person-official csv_pus.zip or both split person ZIPs')
 person_zips=person_zip_args(official=x.person_official, part1=x.person_a, part2=x.person_b)
 housing_report=verify_housing_zip(x.housing)
 print('SOURCE VERIFIED: housing', housing_report, flush=True)
 sources={'geography':P/'inputs/puma_fmr_screened.csv','prices':P/'inputs/source_2024_2026.csv'}
 for key,f in sources.items():
  if not f.is_file():raise FileNotFoundError(f)
  value=digest(f)
  if value!=HASHES[key]:raise RuntimeError(f'INPUT HASH MISMATCH {key}: {value} != {HASHES[key]}')
  print('SOURCE VERIFIED:',key,f.name,flush=True)
 output=x.output.resolve();cache=output/'derived_person_caches';cache.mkdir(parents=True,exist_ok=True)
 subprocess.run([sys.executable,str(P/'rebuild_raw_person_caches.py'),'--person-zips',*person_zips,'--prices',str(sources['prices']),'--out',str(cache)],env=env,check=True,cwd=P)
 national=output/'national'
 subprocess.run([sys.executable,str(P/'src/run_joint.py'),'--housing-zip',str(x.housing.resolve()),'--food-cache',str(cache/'acs2024_food_person_aggregates.pkl'),'--composition-cache',str(cache/'acs2024_person_composition.pkl'),'--geography',str(sources['geography']),'--out',str(national)],env=env,check=True,cwd=P)
 verdict=check_results(national)
 verdict['raw_source_hashes']=HASHES
 verdict['generated_cache_sha256']={n:digest(cache/n) for n in ('acs2024_food_person_aggregates.pkl','acs2024_person_composition.pkl')}
 (output/'REPRODUCTION_REPORT.json').write_text(json.dumps(verdict,indent=2)+'\n')
 print(json.dumps(verdict,indent=2),flush=True)
if __name__=='__main__':main()
