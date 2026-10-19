"""HESI research pilot: Dec 2024 USDA age-sex Thrifty/Low-cost food + ACS housing; not a complete essential-cost index."""
import numpy as np,pandas as pd,zipfile,pathlib,json,hashlib
BASE=pathlib.Path(__file__).resolve().parent
PERSONS=[pathlib.Path('/mnt/data/HESI_Person_Part_1.zip'),pathlib.Path('/mnt/data/HESI_Person_Part_2.zip')]
HOUSING=pathlib.Path('/mnt/data/csv_hus.zip')
# Official USDA monthly food plan tables issued Jan 2025; December 2024 (USD); age 0 extrapolation via age 1 value (flagged)
# child age bands; adult male/female ages 12+; table footnotes apply size economies
T_CHILD={'thrifty':[110.7,166.5,181.6,201.7,233.2],'low':[157.7,164.4,171,245.2,258.1]}
T_M={'thrifty':[249.3,314.5,307.4,272.3,259.9],'low':[301.4,307.1,303.6,285.4,283.6]}
T_F={'thrifty':[215.7,250.1,245.6,228.6,251.4],'low':[256.9,258.7,263.7,256.6,256.6]}
def costs(age,sex,plan):
    child=np.select([age<=1,age<=3,age<=5,age<=8,age<=11],T_CHILD[plan],default=np.nan)
    band=np.select([age<=13,age<=19 if plan=='thrifty' else age<=18,age<=50,age<=70],[0,1,2,3],default=4).astype(int)
    # Low-cost adult schedule begins at age 19; thrifty at 20. 19 year olds assigned low adult band 19-50.
    if plan=='low': band=np.select([age<=13,age<=18,age<=50,age<=70],[0,1,2,3],default=4).astype(int)
    return np.where(age<=11,child,np.where(sex==1,np.array(T_M[plan])[band],np.array(T_F[plan])[band]))
def factor(n):return np.select([n==1,n==2,n==3,n==4,n<=6],[1.2,1.1,1.05,1.,.95],default=.9)
parts=[]
for p in PERSONS:
 with zipfile.ZipFile(p) as z:
  for member in z.namelist():
   if not member.endswith('.csv'):continue
   for d in pd.read_csv(z.open(member),usecols=['SERIALNO','AGEP','SEX'],chunksize=180000):
    a=d.AGEP.to_numpy();s=d.SEX.to_numpy()
    d['thrifty']=costs(a,s,'thrifty');d['low']=costs(a,s,'low')
    parts.append(d.groupby('SERIALNO',sort=False).agg(persons=('AGEP','size'),thrifty=('thrifty','sum'),low=('low','sum')))
    print('person chunk',len(d),flush=True)
# sum chunk groups safely across CSV boundaries
agg=pd.concat(parts).groupby(level=0,sort=False).sum()
print('unique households in people',len(agg),flush=True)
acc={(plan,group):{'den':np.zeros(81),'num':np.zeros(81),'covered':0,'n':0} for plan in ('thrifty','low') for group in ('all','renter','owner')}
for p in [HOUSING]:
 with zipfile.ZipFile(p) as z:
  for member in z.namelist():
   if not member.endswith('.csv'):continue
   cols=['SERIALNO','NP','TEN','HINCP','ADJINC','ADJHSG','GRNTP','SMOCP','WGTP']+[f'WGTP{k}' for k in range(1,81)]
   for d in pd.read_csv(z.open(member),usecols=cols,chunksize=65000):
    d=d.join(agg,on='SERIALNO',how='left')
    assert ((d.loc[(d.NP>0)&d.persons.notna(),'NP'] ==d.loc[(d.NP>0)&d.persons.notna(),'persons'])).all()
    housing=np.where(d.TEN==3,d.GRNTP,np.where(d.TEN.isin([1,2]),d.SMOCP,np.nan))
    valid=(d.NP>0)&d.persons.notna()&d.TEN.isin([1,2,3])&d.HINCP.notna()&np.isfinite(housing)&(d.WGTP>0)&(d.ADJHSG>0)&(d.ADJINC>0)
    x=d[valid].copy()
    if x.empty:continue
    inc=x.HINCP.to_numpy(float)*x.ADJINC.to_numpy(float)/1e6
    h=np.where(x.TEN==3,x.GRNTP,x.SMOCP)*x.ADJHSG.to_numpy(float)/1e6 *12
    w=x[['WGTP']+[f'WGTP{k}' for k in range(1,81)]].to_numpy(float)
    n=x.persons.to_numpy(float)
    for plan in ('thrifty','low'):
     food=x[plan].to_numpy(float)*factor(n)*12
     hardship=((inc<h+food)).astype(float)
     for group,mask in [('all',np.ones(len(x),bool)),('renter',x.TEN.to_numpy()==3),('owner',x.TEN.isin([1,2]).to_numpy())]:
      a=acc[(plan,group)]; ww=w[mask];a['den']+=ww.sum(axis=0);a['num']+=(ww*hardship[mask,None]).sum(axis=0);a['n']+=mask.sum()
    print('household chunk',len(d),flush=True)
rows=[]
for (plan,group),a in acc.items():
 p=a['num']/a['den']; se=np.sqrt(.05*np.sum((p[1:]-p[0])**2))
 rows.append(dict(food_plan=plan,tenure=group,households_unweighted=int(a['n']),households_weighted=round(a['den'][0]),pct_below_housing_plus_food=round(p[0]*100,3),ci_low=round(max(0,p[0]-1.96*se)*100,3),ci_high=round(min(1,p[0]+1.96*se)*100,3)))
pd.DataFrame(rows).to_csv(BASE/'results.csv',index=False)
(BASE/'manifest.json').write_text(json.dumps({'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PERSONS+[HOUSING]},'USDA':['https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Thrifty_Food_Plan_December_2024.pdf','https://fns-prod.azureedge.us/sites/default/files/resource-files/Cost_Of_Food_Low_Moderate_Liberal_Food_Plans_December_2024.pdf'],'reference_period':'December 2024 monthly food prices applied to full-year annual household income','limitation':'Not a complete essentials budget; taxes, healthcare, childcare, transport excluded. No 2024 full-year food average. Age-0 uses age-1 USDA estimate. Adult male low-cost groups use 19-50. Annualizing December 2024 prices is a scenario, not average 2024.', 'weight':'ACS WGTP and WGTP1-80, 4/80 variance'},indent=2))
print(pd.DataFrame(rows).to_string(index=False),flush=True)
