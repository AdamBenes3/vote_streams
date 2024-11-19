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
    def convert_from_result_list_into_ranked_candidates(votes : List[int]) -> List[int]:
        """
        Conver list of how much they got votes into sorted from best to worst
        """
        return [candidate + 1 for candidate, _ in sorted(enumerate(votes), key=lambda x: x[1], reverse=True)]