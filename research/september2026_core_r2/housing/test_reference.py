import unittest
from housing_reference import HousingReference,UnresolvedHousingCase,capacity_scenario
class TestHUDReference(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.m=HousingReference()
 def test_exact_price(self):
  rec=self.m.county.iloc[0]; q=self.m.estimate('county',str(rec.geo_id),rec.hud_area_code,2);self.assertEqual(q['monthly_gross_rent_usd'],int(rec.monthly_2br));self.assertEqual(q['annual_gross_rent_usd'],12*int(rec.monthly_2br))
 def test_zip_hud_key(self):
  r=self.m.small.iloc[0];self.assertEqual(self.m.estimate('small_area',r.geo_id,r.hud_area_code,1)['monthly_gross_rent_usd'],int(r.monthly_1br))
 def test_no_puma(self):
  with self.assertRaises(UnresolvedHousingCase):self.m.estimate('puma','00100','ABC',2)
 def test_no_missing_hud_area(self):
  with self.assertRaises(UnresolvedHousingCase):self.m.estimate('county','0100199999','NOTAHUDCODE',2)
 def test_no_extra_utilities(self):
  r=self.m.county.iloc[0]
  with self.assertRaises(UnresolvedHousingCase):self.m.estimate('county',r.geo_id,r.hud_area_code,2,utility_extra=50)
 def test_bedrooms_outside(self):
  r=self.m.county.iloc[0]
  for b in [-1,5,1.5,'2']:
   with self.subTest(b=b),self.assertRaises(UnresolvedHousingCase):self.m.estimate('county',r.geo_id,r.hud_area_code,b)
 def test_not_actual_unit(self):
  r=self.m.county.iloc[0];self.assertIn('not observed',self.m.estimate('county',r.geo_id,r.hud_area_code,0)['rent_measure'])
 def test_capacity_scenario(self):
  self.assertEqual([capacity_scenario(x) for x in range(1,9)],[1,1,2,2,3,3,4,4])
 def test_capacity_excess(self):
  with self.assertRaises(UnresolvedHousingCase):capacity_scenario(9)
 def test_source_positive(self):self.assertGreater(len(self.m.small),30000)
if __name__=='__main__':unittest.main(verbosity=2)
