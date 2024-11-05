# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.stv import stv

class STV_parse():
    def __init__(self, candidates : List[str]) -> None:
        self.desired_length = len(candidates)
        self.S = stv(candidates, [])
        return
    
    def parse(self, vote : str, length : int) -> Union[int, List]:
        # Split the string by ':'
        parts = vote.split(':')
        
        # Extract numbers and convert them to integers
        numbers = list(map(int, parts[1].split(',')))
        
        # Create the result list with given numbers followed by None
        result = numbers + [None] * (length - len(numbers))
        
        return int(parts[0]), result

    def input_line(self, line : str) -> None:
        nr_of_votes, vote = self.parse(line, self.desired_length)
        for _ in range(nr_of_votes):
            # print(vote)
            self.S.add_vote(vote)
        return

    def result(self) -> str:
        return self.S.stv()
