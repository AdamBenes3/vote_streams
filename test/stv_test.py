# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import unittest
from collections import Counter

# Import functions to test
from src.vote_rules.brute_force.stv import stv

class stv_test(unittest.TestCase):
    def test_stv1(self):
        candidates = [1, 2, 3, 4, 5]
        votes = [[4, 2, 3, 1, 5], [3, 1, 2, 4, 5], [4, 1, 3, 5, 2], [5, 1, 3, 2, 4]]
        S = stv(candidates, votes)
        expected_output_1 = 4  # Expected output dictionary
        self.assertEqual(S.stv(), expected_output_1)
    
    def test_stv2(self):
        candidates = ["a", "b", "c", "d", "e"]
        votes = [["a", "b", "c", "d", "e"], ["c", "a", "b", "e", "d"], ["a", "b", "c", "d", "e"], ["b", "a", "c", "d", "e"]]
        S = stv(candidates, votes)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(S.stv(), expected_output_1)
    
    def test_stv3(self):
        candidates = [1, 2, 3, 4, 5]
        votes = [[5, 4, 2, 3, 1], [1, 2, 4, 3, 5], [5, 2, 4, 1, 3], [2, 3, 4, 5, 1]]
        S = stv(candidates, votes)
        expected_output_3 = 5  # Expected output dictionary
        self.assertEqual(S.stv(), expected_output_3)
    
    def test_stv4(self):
        candidates = [1, 2, 3]
        votes = [[1, 2, 3], [1, 2], [1], [1, 2, 3]]
        S = stv(candidates, votes)
        expected_output_3 = 1  # Expected output dictionary
        self.assertEqual(S.stv(), expected_output_3)
        
        

if __name__ == '__main__':
    unittest.main()
