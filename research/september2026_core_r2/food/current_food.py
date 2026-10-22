"""September 2026 USDA source-specific household food estimator; no security classifications."""
import csv,hashlib,json
from pathlib import Path
SRC=Path(__file__).with_name('usda_september_2026.csv')
SIZE={1:1.20,2:1.10,3:1.05,4:1.,5:.95,6:.95}
def key(age,sex,plan):
    if type(age)!=int or age<1 or age>110:raise ValueError('Unsupported age; infants are not priced')
    if age<=11:
        bands=[(1,1,'1 year'),(2,3,'2-3 years'),(4,5,'4-5 years'),(6,8,'6-8 years'),(9,11,'9-11 years')]
        return 'Child',next(s for lo,hi,s in bands if lo<=age<=hi)
    if sex not in ('Male','Female'):raise ValueError('USDA age-sex group required for age 12+')
    bands=[(12,13,'12-13 years'),(14,19,'14-19 years'),(20,50,'20-50 years'),(51,70,'51-70 years'),(71,110,'71+ years')] if plan=='Thrifty' else [(12,13,'12-13 years'),(14,18,'14-18 years'),(19,50,'19-50 years'),(51,70,'51-70 years'),(71,110,'71+ years')]
    return sex,next(s for lo,hi,s in bands if lo<=age<=hi)
def load(path=SRC):
    with open(path,newline='') as f:rows=list(csv.DictReader(f))
    d={}
    for r in rows:
        k=(r['plan'],r['group'],r['age'])
        if k in d:raise ValueError('Duplicate source key '+str(k))
        d[k]=float(r['monthly_usd'])
    assert len(d)==60,f'Expected 60 costs (4 plans x 15 groups), got {len(d)}'
    return d
def calculate(members,plan='Low-Cost',prices=None):
    if not members:raise ValueError('Household cannot be empty')
    if plan not in ('Thrifty','Low-Cost','Moderate-Cost','Liberal'):raise ValueError('Unsupported food plan')
    d=prices if prices is not None else load()
    subtotal=sum(d[(plan,*key(m['age'],m.get('sex'),plan))] for m in members)
    factor=SIZE.get(len(members),.90)
    return {'reference_month':'2026-09','cost_usd_monthly':round(subtotal*factor,2),'food_plan':plan,'persons':len(members),'source_status':'observed_usda_published_rates','method_status':'research_not_full_coverage','geography':'mainland_us_reference_rates','infants_supported':False,'annual_2026_observed':False}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
if __name__=='__main__':
    family=[{'age':35,'sex':'Male'},{'age':35,'sex':'Female'},{'age':7,'sex':'Male'},{'age':10,'sex':'Female'}]
    for p in ('Thrifty','Low-Cost','Moderate-Cost','Liberal'):print(json.dumps(calculate(family,p)))
