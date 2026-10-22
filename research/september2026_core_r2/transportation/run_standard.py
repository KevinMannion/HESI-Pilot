"""HESI Transportation reference standard: Sept 2026, 12,000 mi/year."""
from pathlib import Path
import argparse,csv,io,json
from model import VehicleCase,annual_cost
B=Path(__file__).resolve().parent

def compute_scenarios():
 with (B/'eia_us_regular_sept2026.csv').open() as f: rows=list(csv.DictReader(f))
 assert len(rows)==4
 gas=sum(float(r['usd_per_gallon']) for r in rows)/len(rows)
 assert abs(gas-4.35475)<1e-9
 assumptions=dict(acquisition_price=18990,resale_price_after_years=6500,horizon_years=6,annual_miles=12000,mpg=32,gas_per_gallon=gas,insurance_annual=1600,maintenance_annual=1200,registration_tax_annual=400,financing_interest_annual=350)
 scenarios=[]
 for label,miles in [('low_mileage',6000),('reference',12000),('high_mileage',15000)]:
  x=VehicleCase(**{**assumptions,'annual_miles':miles})
  c=annual_cost(x)
  scenarios.append({'scenario':label,'annual_miles':miles,'monthly':round(c['total_monthly'],2),'annual':round(c['total_annual'],2),'fuel_annual':round(c['components_annual']['fuel'],2),'status':c['scientific_status']})
 return scenarios

def csv_text(scenarios):
 buf=io.StringIO()
 w=csv.DictWriter(buf,fieldnames=scenarios[0].keys());w.writeheader();w.writerows(scenarios)
 return buf.getvalue()

if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--write-tracked',action='store_true',help='Overwrite transport_reference_2026_09.csv; default is compare-only')
 a=p.parse_args()
 scenarios=compute_scenarios()
 computed_rows=list(csv.DictReader(io.StringIO(csv_text(scenarios))))
 with (B/'transport_reference_2026_09.csv').open() as f:
  golden_rows=list(csv.DictReader(f))
 if computed_rows!=golden_rows:
  raise SystemExit('computed transport_reference_2026_09.csv differs from tracked golden file')
 if a.write_tracked:
  (B/'transport_reference_2026_09.csv').write_text(csv_text(scenarios))
 print(json.dumps(scenarios,indent=2))
