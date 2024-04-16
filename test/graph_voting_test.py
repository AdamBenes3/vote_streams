# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

import unittest
from collections import Counter

# Import functions to test
from src.vote_rules.brute_force.graph_voting import graph_voting

class graph_voting_test(unittest.TestCase):
    def test_plurality1(self):
        votes = [["a", "b", "c", "d"], ["d", "b", "c", "a"], ["d", "c", "a", "b"], ["d", "c", "a", "b"], ["d", "c", "a", "b"]]
        candidates = ["a", "b", "c", "d"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "d"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
        
if __name__ == '__main__':
    unittest.main()
