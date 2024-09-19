# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from src.vote_rules.brute_force.plurality import Plurality

from src.misra_gries import Misra_Gries

class MGSR:
    def __init__(self, nr_of_candidates : int, k : int) -> None:
        self.result = Vector([0] * nr_of_candidates)
        mg = Misra_Gries(k)
        return

    def parse(new_vote : str) -> None:
        mg.misra_gries_update(new_vote)