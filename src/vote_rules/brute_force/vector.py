# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import List

class Vector:
    def __init__(self, lst : List[int] = []) -> None:
        self.lst = lst
        return
    
    def __add__(self_1: 'Vector', self_2: 'Vector') -> 'Vector':
        """
        Adds two vectors and return vector
        Input: vector 1, vector 2
        Output vector
        """
        # Compare lens of the vectors
        if len(self_1.lst) >= len(self_2.lst):
            # Add the shorter to the longer
            return_list = self_1.lst.copy()
            for i, item in enumerate(self_2.lst):
                return_list[i] += item
            return Vector(return_list)
        else:
            # Add the shorter to the longer
            return_list = self_2.lst.copy()
            for i, item in enumerate(self_1.lst):
                return_list[i] += item
            return Vector(return_list)

    def __sub__(self_1 : 'Vector', self_2 : 'Vector') -> 'Vector':
        """
        Subtract two vectors and return vector
        Input: vector 1, vector 2
        Output vector
        """
        # Convert subtraction to addition
        minus = [-item for item in self_2.lst]
        minus_vector = Vector(minus)
        return self_1 + minus_vector
    
    def swap_count(self_1 : 'Vector', self_2 : 'Vector') -> int:
        """
        Count the number of swaps needed to make same list
        Input: vector 1, vector 2
        Output number
        """

        lst_1, lst_2 = self_1.lst[:], self_2.lst[:]

        if sorted(lst_1) != sorted(lst_2):
            return -1  # Indicates an impossible transformation
        
        count = 0
        # Iterate through the lists and perform adjacent swaps
        for i in range(len(lst_1)):
            while lst_1[i] != lst_2[i]:
                # Find the index of the correct element in lst1 to swap
                swap_idx = lst1.index(lst_2[i], i)
                # Swap the element at swap_idx with the one before it until it's in the correct position
                for j in range(swap_idx, i, -1):
                    lst1[j], lst1[j-1] = lst_1[j-1], lst_1[j]
                    count += 1
        return count

    def __str__(self) -> str:
        return "(" + ', '.join(str(element) for element in self.lst) + ")"
