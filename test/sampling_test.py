import unittest
from collections import Counter

# Add parent directory to path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import functions to test
from src.sampling import basic_sampling_algorithm, random_sample_update

class sampling_test(unittest.TestCase):
    def test_basic_sampling_algorithm(self):
        # Example input array from 0 to 99
        input_array = list(range(500))
        # Example value for k
        k = 10
        # Number of trials to run
        num_trials = 5000
        
        # Count occurrences of each element in the output across multiple trials
        counts = Counter()
        for _ in range(num_trials):
            output_array = basic_sampling_algorithm(input_array, k)
            counts.update(output_array)
        
        # Check if all elements in input_array have roughly the same count
        expected_count = num_trials / len(input_array)
        # 9% error margin
        i = 0.09
        for count in counts.values():
            self.assertAlmostEqual(count, expected_count, delta=num_trials * i)
    



if __name__ == '__main__':
    unittest.main()