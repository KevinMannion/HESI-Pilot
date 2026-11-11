import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from transport_vehicle_rules import VehicleEligibilityError, validate_vehicle_assignment


class TransportVehicleEligibility(unittest.TestCase):
    def test_zero_drivers_zero_vehicles_ok(self):
        hh = {"adults": 0, "drivers": 0, "vehicles_assigned": 0}
        self.assertEqual(validate_vehicle_assignment(hh), 0)

    def test_one_driver_one_vehicle_ok(self):
        hh = {"drivers": 1, "vehicles_assigned": 1}
        self.assertEqual(validate_vehicle_assignment(hh), 1)

    def test_two_drivers_two_vehicles_ok(self):
        hh = {"drivers": 2, "transport_vehicles": 2}
        self.assertEqual(validate_vehicle_assignment(hh), 2)

    def test_vehicles_exceed_drivers_fails(self):
        with self.assertRaises(VehicleEligibilityError):
            validate_vehicle_assignment({"drivers": 1, "vehicles_assigned": 2})

    def test_vehicles_exceed_cap_fails(self):
        with self.assertRaises(VehicleEligibilityError):
            validate_vehicle_assignment({"drivers": 3, "vehicles_assigned": 3})

    def test_negative_vehicles_fails(self):
        with self.assertRaises(VehicleEligibilityError):
            validate_vehicle_assignment({"drivers": 1, "vehicles_assigned": -1})


if __name__ == "__main__":
    unittest.main()
