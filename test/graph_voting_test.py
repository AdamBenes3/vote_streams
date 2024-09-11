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
    def test_copeland1(self):
        votes = [["a", "b", "c", "d"], ["d", "b", "c", "a"], ["d", "c", "a", "b"], ["d", "c", "a", "b"], ["d", "c", "a", "b"]]
        candidates = ["a", "b", "c", "d"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "d"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_copeland2(self):
        votes = [["B", "C", "D", "A"], ["A", "D", "C", "B"], ["B", "A", "D", "C"], ["A", "B", "C", "D"], ["A", "C", "D", "B"]]
        candidates = ["A", "B", "C", "D"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_copeland3(self):
        votes = [["e", "b", "d", "a", "c"], ["c", "d", "a", "e", "b"], ["c", "a", "b", "d", "e"], ["a", "e", "c", "b", "d"], ["e", "a", "c", "b", "d"]]
        candidates = ["a", "b", "c", "d", "e"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_copeland4(self):
        votes = [["a"], ["a"], ["a"], ["a"]]
        candidates = ["a"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_copeland5(self):
        votes = [["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_copeland6(self):
        votes = [["D", "E", "F", "A", "B", "G", "C"], ["E", "C", "D", "A", "F", "G", "B"], ["G", "C", "E", "F", "D", "A", "B"], ["E", "F", "A", "B", "C", "D", "G"], ["D", "E", "F", "A", "B", "G", "C"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.copeland_winner(G)
        expected_output_1 = "E"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)

    def test_minimax1(self):
        votes = [["a", "b", "c", "d"], ["d", "b", "c", "a"], ["d", "c", "a", "b"], ["d", "c", "a", "b"], ["d", "c", "a", "b"]]
        candidates = ["a", "b", "c", "d"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "d"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        return

    def test_minimax2(self):
        votes = [["B", "C", "D", "A"], ["A", "D", "C", "B"], ["B", "A", "D", "C"], ["A", "B", "C", "D"], ["A", "C", "D", "B"]]
        candidates = ["A", "B", "C", "D"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_minimax3(self):
        votes = [["e", "b", "d", "a", "c"], ["c", "d", "a", "e", "b"], ["c", "a", "b", "d", "e"], ["a", "e", "c", "b", "d"], ["e", "a", "c", "b", "d"]]
        candidates = ["a", "b", "c", "d", "e"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_minimax4(self):
        votes = [["a"], ["a"], ["a"], ["a"]]
        candidates = ["a"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "a"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
    def test_minimax5(self):
        votes = [["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"], ["A", "B", "C", "D", "E", "F", "G"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "A"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)

    def test_minimax6(self):
        votes = [["D", "E", "F", "A", "B", "G", "C"], ["E", "C", "D", "A", "F", "G", "B"], ["G", "C", "E", "F", "D", "A", "B"], ["E", "F", "A", "B", "C", "D", "G"], ["D", "E", "F", "A", "B", "G", "C"]]
        candidates = ["A", "B", "C", "D", "E", "F", "G"]
        G = graph_voting()
        G = graph_voting.initialize_complete_graph(candidates)
        G = graph_voting.voting(votes, G)
        result = graph_voting.minimax_condorcet_winner(G)
        expected_output_1 = "E"  # Expected output dictionary
        self.assertEqual(result, expected_output_1)
        
if __name__ == '__main__':
    unittest.main()