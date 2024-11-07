# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.graph_voting import graph_voting

class Minimax_parse():
    def __init__(self, candidates: List[str]) -> None:
        """Initializes Minimax_parse with a list of candidates, setting up a graph-based voting structure."""
        self.S = graph_voting(candidates)
        return
    
    def parse(self, vote: str) -> Union[int, List[str]]:
        """Parses a vote string into a multiplier and a list of ranked candidates.

        Args:
            vote (str): Vote data in the format 'multiplier:candidate1,candidate2,...'

        Returns:
            Tuple[int, List[str]]: The number of repetitions of the vote and a list of candidates.
        """
        parts = vote.split(':')
        line = parts[1].split(',')
        return int(parts[0]), line

    def input_line(self, line: str) -> None:
        """Processes a line of votes by parsing and applying each vote to the voting structure.

        Args:
            line (str): A line of voting data in the format 'multiplier:candidate1,candidate2,...'
        """
        nr_of_votes, vote = self.parse(line)
        for _ in range(nr_of_votes):
            self.S.process_vote(vote)
        return

    def result(self) -> str:
        """Calculates and returns the Minimax Condorcet winner based on votes.

        Returns:
            str: The winner determined by the Minimax Condorcet method.
        """
        return self.S.minimax_condorcet_winner()
