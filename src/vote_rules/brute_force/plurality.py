# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import List

from src.vote_rules.brute_force.vector import Vector

class Plurality:
    def __init__(self, nr_of_candidates) -> None:
        self.result = Vector([0] * nr_of_candidates)
        return
    def vote_update(self, new_vote : Vector) -> None:
        """
        Adding one vote
        """
        self.result += new_vote
        return
    def votes_process(self, votes : List[Vector]) -> str:
        """
        Adds list of votes
        """
        for vote in votes:
            x = Vector(vote)
            self.vote_update(x)
        return str(self.result)
