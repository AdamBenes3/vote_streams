# Add main directory to path
import sys
import os

main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.vector import Vector

class parse_and_pass():
    def __init__(self, candidates: List[str]) -> None:
        self.desired_length = len(candidates)
        self.V = Vector([])
        return
    
    def input_line(self, line: str) -> None:
        line = self.string_to_array(line)
        # print(line)
        vote = self.parse(line)
        # print(vote)
        self.V = self.V + Vector(vote)
        return

    def result(self) -> str:
        return self.V.lst

    def parse(self, arr):
        counter = 0
        ranked_arr = [0] * (self.desired_length + 1)
        array = arr[::-1]
        for item in array:
            # print(array)
            # print(ranked_arr)
            ranked_arr[array[counter]] = counter
            counter += 1
        return ranked_arr[1:]
    
    def string_to_array(self, input_string):
        # Split the input string by commas and convert each part to an integer
        arr = [int(num) for num in input_string.split(',')]
        return arr