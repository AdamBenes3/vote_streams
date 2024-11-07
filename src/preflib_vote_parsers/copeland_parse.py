# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.graph_voting import graph_voting

class Copeland_parse():
    def __init__(self, candidates: List[str]) -> None:
        """Initializes Copeland_parse with a list of candidates, creating a graph-based voting structure."""
        self.S = graph_voting(candidates)
        return
    
    def parse(self, vote: str) -> Union[int, List[str]]:
        """Parses a vote string into a tuple containing the number of votes and a list of ranked candidates.

        Args:
            vote (str): Vote data in the format 'multiplier:candidate1,candidate2,...'

        Returns:
            Tuple[int, List[str]]: The number of times the vote is repeated and a list of ranked candidates.
        """
        parts = vote.split(':')
        line = parts[1].split(',')
        return int(parts[0]), line

    def input_line(self, line: str) -> None:
        """Processes a single line of votes, parsing it and adding each vote to the voting structure.

        Args:
            line (str): Line of voting data in the format 'multiplier:candidate1,candidate2,...'
        """
        nr_of_votes, vote = self.parse(line)
        for _ in range(nr_of_votes):
            self.S.process_vote(vote)
        return

    def result(self) -> str:
        """Calculates and returns the Copeland winner based on accumulated votes.

        Returns:
            str: The winner determined by the Copeland method.
        """
        return self.S.copeland_winner()
