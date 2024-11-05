# Add main directory to path
import sys
import os

main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, List

from src.vote_rules.brute_force.plurality import Plurality

from src.vote_rules.brute_force.vector import Vector

class Plurality_parse():
    def __init__(self, candidates: List[str]) -> None:
        self.desired_length = len(candidates)
        self.V = Plurality(self.desired_length)
        return
    
    def input_line(self, line: str) -> None:
        parts = line.split(':')
        line = self.string_to_array(parts[1])
        # print(line)
        vote = self.parse(line)
        # print(vote)
        for _ in range(int(parts[0])):
            self.V.vote_update(vote)
        return

    def result(self) -> str:
        return self.V.result.lst

    def parse(self, arr):
        counter = 0
        ranked_arr = [0] * (self.desired_length + 1)
        array = arr[::-1]
        plus = self.desired_length - len(array)
        for item in array:
            # print(array)
            # print(ranked_arr)
            ranked_arr[array[counter]] = counter + plus
            counter += 1
        # print(ranked_arr[1:])
        return Vector(ranked_arr[1:])
    
    def string_to_array(self, input_string):
        # Split the input string by commas and convert each part to an integer
        arr = [int(num) for num in input_string.split(',')]
        return arr