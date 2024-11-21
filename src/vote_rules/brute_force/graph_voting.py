# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.vote_rules.brute_force.graph import Graph, Vertex
from typing import List

class graph_voting():
    def __init__(self, vertecies : List[str]) -> None:
        """
        Inicilize the complete graph (easy to do just by putting there the first vote :))
        """
        V = []
        # Append all the candidates to graph
        for i in vertecies:
            V.append(Vertex(i))
        # Add them all as a neighbours with value 0
        for v in V:
            for i in V:
                if v != i:
                    v.add_neighbour({i : 0})
        self.G = Graph(V)
        return
    def process_vote(self, vote : List[str]) -> Graph:
        """
        Compute weight on neighbours
        """
        # For every tuple in vote
        for idx_i, i in enumerate(vote):
            for idx_j, j in enumerate(vote):
                # We do not want to count them twice
                if idx_i < idx_j:
                    # Compute who was before who
                    x = self.G.get_value_between(i, j) + 1
                    self.G.update_value(i, j, x)
                    x = self.G.get_value_between(j, i) - 1
                    self.G.update_value(j, i, x)

        all_candidates = self.G.verticies_names

        # Determine absent candidates
        absent_candidates = set(all_candidates) - set(vote)

        # Treat absent candidates as worse than all listed candidates
        for candidate in vote:
            for absent in absent_candidates:
                x = self.G.get_value_between(candidate, absent) + 1
                self.G.update_value(candidate, absent, x)
                x = self.G.get_value_between(absent, candidate) - 1
                self.G.update_value(absent, candidate, x)
        
        return self.G
    def voting(self, votes : List[List[str]]) -> Graph:
        """
        Apply all votes
        """
        # For every vote
        for vote in votes:
            # For every tuple in vote
            self.process_vote(vote)
        return self.G
    def copeland_winner(self) -> Vertex:
        """
        Find the candidate with most wins against others
        """
        # Inicilize with first candidate
        best_vertex = self.G.V[0]
        # Set best_counter to be bad (so someone for sure will be better)
        best_counter = float('-inf')
        for v in self.G.V:
            positive_counter = 0
            # We look at neighbours
            for n in v.neighbours:
                for key, _ in n.items():
                    # If candidate wins against this counter we increas its counter
                    if n[key] > 0:
                        positive_counter += 1
            # Check if this candidate is the best yet
            if positive_counter > best_counter:
                best_counter = positive_counter
                best_vertex = v
        return str(best_vertex)
    def maximin_condorcet_winner(self) -> Vertex:
        """
        Find the candidate with best worst matchup
        """
        # Inicilize with first candidate
        best_vertex = self.G.V[0]
        # Set best_counter to be bad (so someone for sure will be better)
        best_counter = float('-inf')
        for v in self.G.V:
            # Worst matchup for this vertex
            worst_matchup = float('inf')
            # We look at neighbours
            for n in v.neighbours:
                for key, _ in n.items():
                    # If candidate wins against this counter we increas its counter
                    if n[key] < worst_matchup:
                        worst_matchup = n[key]
            # Check if this candidate is the best yet
            if worst_matchup > best_counter:
                best_counter = worst_matchup
                best_vertex = v
        return str(best_vertex)