import unittest
from collections import Counter

# Add parent directory to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import functions to test
from src.sampling import algorithm_R

class sampling_test(unittest.TestCase):
    """
    THE TESTS ARE NOT DETEMINISTIC
    The tests tests work by running the sampling algorithms multiple times and checking if the output is roughly uniform.
    num_trials says how many times to run the randomize algorithm.
    The expected_count is the number of times each element should appear in the output array.
    The error_margin says maximal error that is consider uniform.
    """
    def test_basic_sampling_algorithm(self):
        # Example input array from 0 to 499
        input_array = list(range(500))
        # Example value for k
        k = 10
        # Number of trials to run
        num_trials = 5000
        
        # Count occurrences of each element in the output across multiple trials
        counts = Counter()
        for _ in range(num_trials):
            output_array = algorithm_R(input_array, k)
            counts.update(output_array)
        
        # Check if all elements in input_array have roughly the same count
        expected_count = num_trials / len(input_array)
        # 9% error margin
        error_margin = 0.09
        for count in counts.values():
            self.assertAlmostEqual(count, expected_count, delta=num_trials*error_margin)
    
    def test_sampling_algorithm_L(self):
        # Example input array from 0 to 499
        input_array = list(range(500))
        # Example value for k
        k = 10
        # Number of trials to run
        num_trials = 5000
        
        # Count occurrences of each element in the output across multiple trials
        counts = Counter()
        for _ in range(num_trials):
            output_array = algorithm_R(input_array, k)
            counts.update(output_array)
        
        # Check if all elements in input_array have roughly the same count
        expected_count = num_trials / len(input_array)
        # 9% error margin
        error_margin = 0.09
        for count in counts.values():
            self.assertAlmostEqual(count, expected_count, delta=num_trials*error_margin)



if __name__ == '__main__':
    unittest.main()