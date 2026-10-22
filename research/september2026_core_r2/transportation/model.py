"""HESI September 2026 used-vehicle cost prototype. No national adequacy claim."""
from dataclasses import dataclass,asdict
from typing import Optional
import json

@dataclass(frozen=True)
class VehicleCase:
    acquisition_price: float
    resale_price_after_years: float
    horizon_years: float
    annual_miles: float
    mpg: float
    gas_per_gallon: float
    insurance_annual: float
    maintenance_annual: float
    registration_tax_annual: float
    financing_interest_annual: float=0.0
    other_annual: float=0.0
    evidence_verified: bool=False
    source_log: Optional[str]=None

def annual_cost(x:VehicleCase):
    a=asdict(x)
    for k in ['acquisition_price','resale_price_after_years','horizon_years','annual_miles','mpg','gas_per_gallon','insurance_annual','maintenance_annual','registration_tax_annual','financing_interest_annual','other_annual']:
        if a[k]<0: raise ValueError(f'Negative input {k}')
    if x.horizon_years<=0 or x.mpg<=0:raise ValueError('horizon and mpg must be positive')
    if x.resale_price_after_years>x.acquisition_price:raise ValueError('Resale exceeds purchase: use separate appreciation model')
    components={
      'depreciation':(x.acquisition_price-x.resale_price_after_years)/x.horizon_years,
      'fuel':x.annual_miles/x.mpg*x.gas_per_gallon,
      'insurance':x.insurance_annual,
      'maintenance':x.maintenance_annual,
      'registration_taxes':x.registration_tax_annual,
      'financing_interest':x.financing_interest_annual,
      'other':x.other_annual,
    }
    return {'components_annual':components,'total_annual':sum(components.values()),'total_monthly':sum(components.values())/12,'scientific_status':'verified_source_case' if x.evidence_verified and x.source_log else 'hypothetical_sensitivity_only'}

if __name__=='__main__':
    # Illustrative only: ALL non-fuel dollar assumptions lack validation.
    case=VehicleCase(acquisition_price=16000,resale_price_after_years=7000,horizon_years=6,annual_miles=10000,mpg=30,gas_per_gallon=4.35475,insurance_annual=1800,maintenance_annual=1000,registration_tax_annual=400,financing_interest_annual=400)
    print(json.dumps({'inputs':asdict(case),'result':annual_cost(case)},indent=2))
