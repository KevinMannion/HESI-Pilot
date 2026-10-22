import json,csv,math,pathlib
root=pathlib.Path(__file__).resolve().parent
parts=[json.loads((root/f'part_{p}.json').read_text()) for p in ('a','b')]
assert sum(x['allrows'] for x in parts)==1631969
assert sum(x['occupied'] for x in parts)==1348408
assert sum(x['weighted_all'] for x in parts)==132737145
assert sum(x['person_mismatch'] for x in parts)==7
assert sum(x['bygeo'] for x in parts)==1284329
assert sum(x['paired_n'] for x in parts)==1255743
allwt=sum(x['weighted_all'] for x in parts)
paired_w=sum(x['paired_weight'] for x in parts)
bygeo=sum(x['bygeo'] for x in parts)
sums=[sum(p['sums'][i] for p in parts) for i in range(4)]
wts=[sum(p['wts'][i] for p in parts) for i in range(4)]
paired=[sum(p['paired_sums'][i] for p in parts) for i in range(4)]
assert abs(sums[0]-sums[3])<1e-5
assert abs(paired[0]-paired[3])<1e-5
assert wts[1]<=wts[2]<=wts[0]
assert paired_w<=wts[1]
assert all(math.isfinite(x/y) and 0<x/y<10000 for x,y in zip(sums,wts))
rows=[]
for i,name in enumerate(['two_people_per_room','adult_individual_partner_share_children_pooled','adult_individual_partner_share_children_by_sex','two_people_recheck']):
 j=[0,2,1,3][i]
 rows.append({'scenario':name,'weighted_households_covered':round(wts[j]),'coverage_pct_canonical':round(wts[j]/allwt*100,4),'monthly_mean_variable_population':round(sums[j]/wts[j],6),'monthly_mean_paired_population':round(paired[j]/paired_w,6),'annual_paired':round(12*paired[j]/paired_w,6)})
with (root/'executed_results.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
audit={'canonical_occupied_unweighted':sum(x['occupied'] for x in parts),'canonical_occupied_weighted':allwt,'screened_geo_unweighted':bygeo,'screened_geography_unweighted_excluded':sum(x['occupied']-x['bygeo'] for x in parts),'composition_mismatch_after_geo':sum(x['person_mismatch'] for x in parts),'paired_unweighted':sum(x['paired_n'] for x in parts),'paired_weighted':paired_w,'paired_pct_canonical':round(paired_w/allwt*100,4),'over_four_composition_sex_unweighted':sum(x['over4'] for x in parts),'sampling_uncertainty_new_composition':'NOT_RUN','new_price_vintage':'HUD FY2026 revised applicable September 2026','population_vintage':'ACS PUMS 2024','methodology_status':'RESEARCH ONLY, bedroom baseline user-defined not independently validated'}
(root/'audit.json').write_text(json.dumps(audit,indent=2))
print('PASS: 11 integrity assertions; national composition calculations verified');print(json.dumps(audit,indent=2));print(rows)
