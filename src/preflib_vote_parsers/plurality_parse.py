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
        """Initializes Plurality_parse with a list of candidates and sets up the Plurality voting system.

        Args:
            candidates (List[str]): List of candidates involved in the voting process.
        """
        self.desired_length = len(candidates)
        self.V = Plurality(self.desired_length)
        return
    
    def input_line(self, line: str) -> None:
        """Processes a line of vote data by splitting, converting to an array, and applying votes.

        Args:
            line (str): A line of vote data in the format 'multiplier:candidate1,candidate2,...'
        """
        parts = line.split(':')
        line = self.string_to_array(parts[1])
        vote = self.parse(line)
        for _ in range(int(parts[0])):
            self.V.vote_update(vote)
        return

    def result(self) -> str:
        """Returns the result of the plurality vote.

        Returns:
            str: The result of the plurality vote.
        """
        return self.V.result.lst

    def parse(self, arr):
        counter = 0
        ranked_arr = [0] * (self.desired_length + 1)
        array = arr[::-1]
        
        # If the array is shorter add this
        plus = self.desired_length - len(array)
        
        # Iterate over items in array
        for item in array:
            ranked_arr[array[counter]] = counter + plus
            counter += 1
        return Vector(ranked_arr[1:])
    
    def string_to_array(self, input_string: str) -> List[int]:
        """Converts a comma-separated string of numbers into a list of integers.

        Args:
            input_string (str): A string of numbers separated by commas.

        Returns:
            List[int]: List of integers parsed from the input string.
        """
        arr = [int(num) for num in input_string.split(',')]
        return arr
