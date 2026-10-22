"""HESI food pillar: source-anchored household calculations; not a validated security threshold."""
import csv, calendar, hashlib, json
from pathlib import Path

PLANS={'thrifty':'thrifty','low-cost':'low-cost','moderate-cost':'moderate-cost','liberal':'liberal'}
SIZES={1:1.20,2:1.10,3:1.05,4:1.0,5:.95,6:.95}

def normalize_plan(p):
    p=p.lower().replace(' ','-')
    if p not in PLANS: raise ValueError('Unsupported food plan: '+p)
    return p

def load_prices(path):
    catalog={};issues=[]
    with open(path,newline='') as f:
        for row in csv.DictReader(f):
            if row['geographic_area']!='Mainland U.S.' or row['fam_indv']!='Individual' or row['frequency']!='Monthly': continue
            try:
                plan=normalize_plan(row['food_plan'])
                month=list(calendar.month_name).index(row['month'])
                key=(int(row['year']),month,plan,row['group'],row['age'])
                price=float(row['cost'])
                if price<0: raise ValueError('Negative price')
            except (ValueError,TypeError) as e:
                issues.append({'type':'invalid_row','reason':str(e),'row':row}); continue
            if key in catalog:
                if catalog[key]!=price: issues.append({'type':'conflicting_duplicate','key':key,'a':catalog[key],'b':price})
            else: catalog[key]=price
    return catalog,issues

def age_key(age, sex, plan):
    if not isinstance(age,int) or isinstance(age,bool) or age<1 or age>110: raise ValueError('Age 0 or invalid age: infant method unresolved')
    if age<=11:
        group='Child'
        bands=[(1,1,'1 year'),(2,3,'2-3 years'),(4,5,'4-5 years'),(6,8,'6-8 years'),(9,11,'9-11 years')]
    else:
        if sex not in ('Female','Male'):raise ValueError('Sex must match a USDA table category for age 12+')
        group=sex
        if plan=='thrifty': bands=[(12,13,'12-13 years'),(14,19,'14-19 years'),(20,50,'20-50 years'),(51,70,'51-70 years'),(71,110,'71+ years')]
        else: bands=[(12,13,'12-13 years'),(14,18,'14-18 years'),(19,50,'19-50 years'),(51,70,'51-70 years'),(71,110,'71+ years')]
    return group,next(label for lo,hi,label in bands if lo<=age<=hi)

def monthly_cost(catalog,year,month,plan,members):
    plan=normalize_plan(plan)
    if not members:raise ValueError('Empty household')
    if month not in range(1,13):raise ValueError('Invalid month')
    total=0.0
    for member in members:
        group,age=age_key(member['age'],member.get('sex'),plan)
        key=(year,month,plan,group,age)
        if key not in catalog:raise ValueError('Missing or mismatched monthly price: '+str(key))
        total+=catalog[key]
    return round(total*SIZES.get(len(members),.9),2)

def period_cost(catalog,year,months,plan,members):
    months=list(months)
    if len(months)!=len(set(months)) or any(m not in range(1,13) for m in months): raise ValueError('Invalid or duplicate months')
    values=[monthly_cost(catalog,year,m,plan,members) for m in months]
    return {'year':year,'plan':normalize_plan(plan),'months':months,'monthly_costs':values,'total_cost':round(sum(values),2),'price_status':'published_monthly_prices','method_status':'scenario_not_certified'}

def source_sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
