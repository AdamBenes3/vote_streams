# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.vote_rules.brute_force.graph import Graph, Vertex
from typing import List

class graph_voting():
    def initialize_complete_graph(vertecies : List[str]) -> Graph:
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
        G = Graph(V)
        return G
    def process_vote(G : Graph, vote : str) -> Graph:
        """
        Compute weight on neighbours
        """
        # For every tuple in vote
        for idx_i, i in enumerate(vote):
            for idx_j, j in enumerate(vote):
                # We do not want to count them twice
                if idx_i < idx_j:
                    # Compute who was before who
                    x = G.get_value_between(i, j) + 1
                    G.update_value(i, j, x)
                    x = G.get_value_between(j, i) - 1
                    G.update_value(j, i, x)
        return G
    def voting(votes : List[str], G : Graph) -> Graph:
        """
        Apply all votes
        """
        # For every vote
        for vote in votes:
            # For every tuple in vote
            graph_voting.process_vote(G, vote)
        return G
    def copeland_winner(G : Graph) -> Vertex:
        """
        Find the candidate with most wins against others
        """
        # Inicilize with first candidate
        best_vertex = G.V[0]
        # Set best_counter to be bad (so someone for sure will be better)
        best_counter = float('-inf')
        for v in G.V:
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
    def minimax_condorcet_winner(G : Graph) -> Vertex:
        """
        Find the candidate with best worst matchup
        """
        # Inicilize with first candidate
        best_vertex = G.V[0]
        # Set best_counter to be bad (so someone for sure will be better)
        best_counter = float('-inf')
        for v in G.V:
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