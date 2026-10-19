import zipfile,pathlib,numpy as np,pandas as pd,json

BASE = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE / "input_data"
O = BASE

# Prefer the original Census person archive.
# Split archives remain supported for compatibility.
if (DATA_DIR / "csv_pus.zip").exists():
    ps = [DATA_DIR / "csv_pus.zip"]
else:
    ps = [
        DATA_DIR / "HESI_2019_Person_Part_1.zip",
        DATA_DIR / "HESI_2019_Person_Part_2.zip",
    ]

housing = DATA_DIR / "csv_hus.zip"

for source in ps + [housing]:
    if not source.is_file():
        raise FileNotFoundError(f"Missing 2019 Census archive: {source}")

# USDA official OCTOBER 2019 age-sex food plans, monthly dollars. October snapshot only, comparison to Dec 2024 is not matched month.
C={'thrifty':[95.1,104.1,109.9,139.2,158.1],'low':[127.7,134.5,138.,193.5,208.9]}
M={'thrifty':[169.2,175.2,187.5,171.,171.4],'low':[240.7,245.1,242.6,229.5,224.7]}
F={'thrifty':[168.2,166.3,166.3,165.2,160.8],'low':[207.6,206.8,210.5,205.2,201.7]}
def costs(a,s,p):
 child=np.select([a<=1,a<=3,a<=5,a<=8,a<=11],C[p],default=np.nan)
 band=np.select([a<=13,a<=18,a<=50,a<=70],[0,1,2,3],default=4).astype(int)
 return np.where(a<=11,child,np.where(s==1,np.array(M[p])[band],np.array(F[p])[band]))
def factor(n):return np.select([n==1,n==2,n==3,n==4,n<=6],[1.2,1.1,1.05,1.,.95],default=.9)
parts=[]; person_n=0
for p in ps:
 with zipfile.ZipFile(p) as z:
  for m in z.namelist():
   if not m.endswith('.csv'):continue
   for d in pd.read_csv(z.open(m),usecols=['SERIALNO','AGEP','SEX'],chunksize=150000):
    assert d.SERIALNO.str.startswith('2019').all()
    a=d.AGEP.to_numpy();s=d.SEX.to_numpy()
    d['thrifty']=costs(a,s,'thrifty');d['low']=costs(a,s,'low')
    parts.append(d.groupby('SERIALNO',sort=False).agg(persons=('AGEP','size'),thrifty=('thrifty','sum'),low=('low','sum')))
    person_n+=len(d)
 print('person done',p.name,person_n,flush=True)
agg=pd.concat(parts).groupby(level=0,sort=False).sum();del parts
print('unique person households',len(agg),flush=True)
acc={(plan,group):{'den':np.zeros(81),'num':np.zeros(81),'n':0} for plan in ('thrifty','low') for group in ('all','renter','owner')}
audit={'persons':person_n,'person_serials':len(agg),'occupied':0,'matched':0,'mismatched':0,'eligible':0,'excluded_nocash':0,'eligible_weighted':0}
with zipfile.ZipFile(housing) as z:
 for member in z.namelist():
  if not member.endswith('.csv'):continue
  cols=['SERIALNO','NP','TEN','HINCP','ADJINC','ADJHSG','GRNTP','SMOCP','WGTP']+[f'WGTP{k}' for k in range(1,81)]
  for d in pd.read_csv(z.open(member),usecols=cols,chunksize=40000):
   occ=(d.NP>0)&(d.WGTP>0);audit['occupied']+=int(occ.sum())
   d=d.join(agg,on='SERIALNO',how='left'); mat=occ & d.persons.eq(d.NP)
   audit['matched']+=int(mat.sum()); audit['mismatched']+=int((occ&~mat).sum())
   audit['excluded_nocash']+=int((occ & d.TEN.eq(4)).sum())
   housing_cost=np.where(d.TEN.eq(3),d.GRNTP,np.where(d.TEN.isin([1,2]),d.SMOCP,np.nan))
   valid=mat&d.TEN.isin([1,2,3])&d.HINCP.notna()&np.isfinite(housing_cost)&(d.ADJHSG>0)&(d.ADJINC>0)
   x=d.loc[valid];audit['eligible']+=len(x);audit['eligible_weighted']+=int(x.WGTP.sum())
   if x.empty:continue
   inc=x.HINCP.to_numpy(float)*x.ADJINC.to_numpy(float)/1e6
   house=np.where(x.TEN.eq(3),x.GRNTP,x.SMOCP)*x.ADJHSG.to_numpy(float)/1e6*12
   w=x[['WGTP']+[f'WGTP{i}' for i in range(1,81)]].to_numpy(float)
   n=x.persons.to_numpy(float)
   for plan in ('thrifty','low'):
    gap=inc-house-x[plan].to_numpy(float)*factor(n)*12
    hardship=(gap<0).astype(float)
    for group,mask in [('all',np.ones(len(x),bool)),('renter',x.TEN.to_numpy()==3),('owner',x.TEN.isin([1,2]).to_numpy())]:
     a=acc[(plan,group)];ww=w[mask];a['den']+=ww.sum(axis=0);a['num']+=(ww*hardship[mask,None]).sum(axis=0);a['n']+=int(mask.sum())
  print('housing segment',member,flush=True)
rows=[]
for (plan,group),a in acc.items():
 p=a['num']/a['den'];se=np.sqrt(.05*((p[1:]-p[0])**2).sum())
 rows.append(dict(year=2019,food_month='October',plan=plan,tenure=group,n=a['n'],weighted_households=int(round(a['den'][0])),pct=round(p[0]*100,3),ci_low=round((p[0]-1.96*se)*100,3),ci_high=round((p[0]+1.96*se)*100,3)))
pd.DataFrame(rows).to_csv(O/'results_2019_october_snapshot.csv',index=False)
(O/'audit.json').write_text(json.dumps(audit,indent=2)); print('AUDIT',audit,flush=True);print(pd.DataFrame(rows).to_string(index=False),flush=True)
