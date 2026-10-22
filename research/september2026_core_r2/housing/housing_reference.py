"""HESI September 2026 HUD reference gross rental benchmark. Not a certified adequacy standard."""
from pathlib import Path
import pandas as pd

BASE=Path(__file__).resolve().parent
BEDROOMS=tuple(range(5))
PERIOD='2026-09'

class UnresolvedHousingCase(ValueError): pass

class HousingReference:
 def __init__(self,root=BASE):
  root=Path(root)
  self.county=pd.read_csv(root/'county_model_ready.csv',dtype={'geo_id':str,'hud_area_code':str})
  self.small=pd.read_csv(root/'small_area_model_ready.csv',dtype={'geo_id':str,'hud_area_code':str})
  for df,typ in ((self.county,'county'),(self.small,'small_area')):
   assert (df.geo_type==typ).all()
   assert (df.source_period=='FY2026').all()
   assert not df.duplicated(['geo_id','hud_area_code']).any()
   assert df[[f'monthly_{b}br' for b in BEDROOMS]].gt(0).all().all()
 def estimate(self,geography,geo_id,hud_area_code,bedrooms,utility_extra=0,as_of=PERIOD):
  if as_of!=PERIOD: raise UnresolvedHousingCase('Reference snapshot restricted to September 2026')
  if type(bedrooms) is not int or bedrooms not in BEDROOMS: raise UnresolvedHousingCase('Bedroom count must be explicit integer 0–4')
  if utility_extra!=0: raise UnresolvedHousingCase('FMR already includes tenant-paid utilities. No automatic utility add-on')
  if geography not in ('county','small_area'): raise UnresolvedHousingCase('Explicit county or small_area geography required')
  df=self.county if geography=='county' else self.small
  matches=df[(df.geo_id==str(geo_id))&(df.hud_area_code==str(hud_area_code))]
  if len(matches)!=1: raise UnresolvedHousingCase(f'Exact geography requires a unique HUD match; got {len(matches)}')
  rec=matches.iloc[0]
  monthly=int(rec[f'monthly_{bedrooms}br'])
  return {'reference_month':PERIOD,'source':'HUD FY2026 revised effective 2026-05-21','geography':geography,'geo_id':str(geo_id),'hud_area_code':str(hud_area_code),'bedrooms':bedrooms,'monthly_gross_rent_usd':monthly,'annual_gross_rent_usd':monthly*12,'rent_measure':'HUD FMR policy benchmark; not observed available unit','scientific_status':'EXACT_LOOKUP_LOCKED; BEDROOM_ADEQUACY_NOT_CERTIFIED'}

def capacity_scenario(people):
 """Sensitivity only. Not a validated national adequacy standard."""
 if type(people) is not int or people<1: raise ValueError('people must be positive integer')
 bedrooms=max(1,(people+1)//2)
 if bedrooms>4: raise UnresolvedHousingCase('Four-bedroom HUD upper bound exceeded; no silent capping')
 return bedrooms
