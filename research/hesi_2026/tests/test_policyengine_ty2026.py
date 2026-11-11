import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import policyengine_us  # noqa: F401

    HAS_PE = True
except ImportError:
    HAS_PE = False


@unittest.skipUnless(HAS_PE, "policyengine-us not installed in this environment")
class PolicyEngineTy2026(unittest.TestCase):
    def test_synthetic_ca_ty2026(self):
        from resources.policyengine_ty2026 import calculate_ty2026_synthetic

        out = calculate_ty2026_synthetic(
            {"state_code": "CA", "age": 35, "employment_income": 50000}
        )
        self.assertEqual(out.employment_income, 50000.0)
        self.assertGreater(out.income_tax, 0)
        self.assertGreaterEqual(out.adjusted_gross_income_person, out.employment_income - 1)

    def test_household_structure_requires_one_child(self):
        from resources.policyengine_ty2026 import calculate_ty2026_household

        with self.assertRaises(ValueError):
            calculate_ty2026_household(
                {
                    "state_code": "AL",
                    "members": [{"age": 35}, {"age": 33}],
                    "policyengine_synthetic": {
                        "primary_employment_income": 48000,
                        "spouse_employment_income": 24000,
                    },
                }
            )

    def test_tax_year_configuration(self):
        from resources.policyengine_ty2026 import TAX_YEAR, build_synthetic_household_ty2026

        situation = build_synthetic_household_ty2026(
            state_code="AL",
            primary_adult_age=35,
            spouse_adult_age=33,
            child_ages=[4],
            primary_employment_income=1000,
            spouse_employment_income=1000,
        )
        self.assertEqual(TAX_YEAR, "2026")
        self.assertEqual(situation["people"]["adult_primary"]["age"][TAX_YEAR], 35)


class PolicyEngineImportGuard(unittest.TestCase):
    def test_module_import_without_policyengine(self):
        spec = importlib.util.find_spec("resources.policyengine_ty2026")
        self.assertIsNotNone(spec)


if __name__ == "__main__":
    unittest.main()
