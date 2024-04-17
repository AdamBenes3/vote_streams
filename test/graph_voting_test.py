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
    def test_graph_voting1(self):
        votes = [["a", "b", "c", "d"], ["d", "b", "c", "a"], ["d", "c", "a", "b"], ["d", "c", "a", "b"], ["d", "c", "a", "b"]]
        candidates = ["a", "b", "c", "d"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "d"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_graph_voting2(self):
        votes = [["B", "C", "D", "A"], ["A", "D", "C", "B"], ["B", "A", "D", "C"], ["A", "B", "C", "D"], ["A", "C", "D", "B"]]
        candidates = ["A", "B", "C", "D"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_graph_voting3(self):
        votes = [["e", "b", "d", "a", "c"], ["c", "d", "a", "e", "b"], ["c", "a", "b", "d", "e"], ["a", "e", "c", "b", "d"], ["e", "a", "c", "b", "d"]]
        candidates = ["a", "b", "c", "d", "e"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_graph_voting4(self):
        votes = [["a"], ["a"], ["a"], ["a"]]
        candidates = ["a"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_graph_voting5(self):
        votes = [["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_graph_voting6(self):
        votes = [["D", "E", "F", "A", "B", "G", "C"], ["E", "C", "D", "A", "F", "G", "B"], ["G", "C", "E", "F", "D", "A", "B"], ["E", "F", "A", "B", "C", "D", "G"], ["D", "E", "F", "A", "B", "G", "C"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        Gv = graph_voting()
        G = graph_voting.inicilize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.find_winner(G)
        expected_output_1 = "E"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
        
if __name__ == '__main__':
    unittest.main()
