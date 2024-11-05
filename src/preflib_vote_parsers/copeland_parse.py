# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.graph_voting import graph_voting

class Copeland_parse():
    def __init__(self, candidates : List[str]) -> None:
        self.S = graph_voting(candidates)
        return
    
    def parse(self, vote : str) -> Union[int, List]:
        # Split the string by ':'
        parts = vote.split(':')
        
        line = parts[1].split(',')
        
        return int(parts[0]), line

    def input_line(self, line : str) -> None:
        nr_of_votes, vote = self.parse(line)
        for _ in range(nr_of_votes):
            self.S.process_vote(vote)
        return

    def result(self) -> str:
        return self.S.copeland_winner()
