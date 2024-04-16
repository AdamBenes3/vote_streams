# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import unittest
from collections import Counter

# Import functions to test
from src.vote_rules.brute_force.plurality import Plurality

from src.vote_rules.brute_force.vector import Vector

class plurality_test(unittest.TestCase):
    def test_plurality1(self):
        votes = [[1, 1, 1, 0, 0], [0, 1, 1, 0, 1], [0, 0, 0, 1, 1], [1, 0, 1, 1, 0], [0, 0, 1, 1, 1], [1, 1, 1, 0, 0]]
        nr_of_candidates = 5
        Pl = Plurality(nr_of_candidates)
        result = Pl.votes_process(votes)
        expected_output_1 = str(Vector([3, 3, 5, 3, 3]))  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
        
if __name__ == '__main__':
    unittest.main()
