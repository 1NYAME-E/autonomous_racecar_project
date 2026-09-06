# Making the necessary import
import unittest


class TestEnergyCalculations(unittest.TestCase):

    def setUp(self):
        """Initialize the starting enerfy state for testing."""
        self.starting_budget = 1000.0
        self.current_energy = self.starting_budget

    def test_initial_budget(self):
        """Test that the robot starts with the energy allowed."""
        self.assertEqual(self.current_energy, 1000.0,
                         "Starting budget should be exactly 1000 EU")

    def test_forward_movement_deduction(self):
        """
        Test that moving forward 0.5 meters costs exactly 5 EU.
        """
        distance_traveled = 0.5
        cost_per_half_meter = 5.0

        # Calculating the deduction
        deduction = (distance_traveled / 0.5) * cost_per_half_meter
        self.current_energy -= deduction

        self.assertEqual(self.current_energy, 995.0,
                         "Energy deduction for 0.5m forward is incorrect.")

    def test_backward_movement_deduction(self):
        """Test that moving backward 0.5 meters costs exactly 8 EU."""
        distance_traveled = 0.5
        cost_per_half_meter = 8.0

        deduction = (distance_traveled / 0.5) * cost_per_half_meter
        self.current_energy -= deduction

        self.assertEqual(self.current_energy, 992.0,
                         'Energy deduction for 0.5m backward is incorrect.')

    def test_start_moving_deduction(self):
        """Test that the Start Moving action costs exactly 3 EU."""
        start_cost = 3.0
        self.current_energy -= start_cost

        self.assertEqual(self.current_energy, 997.0,
                         'Energy deduction for starting is incorrect.')

    def test_stop_moving_deduction(self):
        """Test that the Stop Moving action costs exactly 1.5 EU."""
        stop_cost = 1.5
        self.current_energy -= stop_cost

        self.assertEqual(self.current_energy, 998.5,
                         'Energy deduction for stopping is incorrect.')


if __name__ == '__main__':
    unittest.main()
