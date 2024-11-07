# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.stv import stv

class STV_parse():
    def __init__(self, candidates: List[str]) -> None:
        """Initializes STV_parse with a list of candidates and sets up the STV voting system.

        Args:
            candidates (List[str]): List of candidates involved in the voting process.
        """
        self.desired_length = len(candidates)
        self.S = stv(candidates, [])
        return
    
    def parse(self, vote: str, length: int) -> Union[int, List[int]]:
        """Parses a vote string and returns the number of votes and a list of ranked candidates.

        Args:
            vote (str): A string representing a vote, in the format 'multiplier:candidate1,candidate2,...'
            length (int): The desired length of the ranked vote list.

        Returns:
            Union[int, List[int]]: The number of votes as an integer and a list of candidates as integers, padded with `None` if necessary.
        """
        parts = vote.split(':')
        numbers = list(map(int, parts[1].split(',')))
        result = numbers + [None] * (length - len(numbers))
        return int(parts[0]), result

    def input_line(self, line: str) -> None:
        """Processes a line of vote data by parsing and applying the vote to the STV system.

        Args:
            line (str): A line of vote data in the format 'multiplier:candidate1,candidate2,...'
        """
        nr_of_votes, vote = self.parse(line, self.desired_length)
        for _ in range(nr_of_votes):
            self.S.add_vote(vote)
        return

    def result(self) -> str:
        """Returns the result of the STV election.

        Returns:
            str: The result of the STV election.
        """
        return self.S.stv()
