import unittest
from adequacy import required_bedrooms,hud_eligible_bedroom_count,UnresolvedComposition
class TestAdequacy(unittest.TestCase):
 def test_single(self): self.assertEqual(required_bedrooms(1,0),1)
 def test_couple(self): self.assertEqual(required_bedrooms(2,0,1),1)
 def test_couple_two_children(self): self.assertEqual(required_bedrooms(2,2,1),2)
 def test_couple_three_children(self): self.assertEqual(required_bedrooms(2,3,1),3)
 def test_unrelated_adults(self): self.assertEqual(required_bedrooms(3,0),3)
 def test_adult_child(self): self.assertEqual(required_bedrooms(3,0,1),2)
 def test_five_bedrooms(self):
  with self.assertRaises(UnresolvedComposition):hud_eligible_bedroom_count(5,0)
 def test_no_couple_overlap(self):
  with self.assertRaises(UnresolvedComposition):required_bedrooms(3,0,2)
 def test_no_infant_exclusion(self):self.assertEqual(required_bedrooms(1,1),2)
 def test_no_floating_counts(self):
  with self.assertRaises(UnresolvedComposition):required_bedrooms(2.0,1)
 def test_zero_adults(self):
  with self.assertRaises(UnresolvedComposition):required_bedrooms(0,2)
if __name__=='__main__':unittest.main()
