# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from random import randint, random
from math import exp, floor, log
from typing import List

class sampling:
    def __init__(self, k : int) -> None:
        self.k = k
        self.n = 0
        self.S = [None] * k
        return
    
    def update_R(self, x) -> None:
        """
        O(1)
        Input new element x
        Output None
        """
        self.n += 1
        if (self.n-1 < self.k):
            self.S[self.n-1] = x
        else:
            i = randint(0, self.n-1)
            if (i < self.k):
                # If i < k, replace the i-th element of s with x
                self.S[i] = x
        return

def algorithm_R(input_array, k : int) -> List:
    """
    O(n)
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    smp = sampling(k)
    for element in input_array:
        smp.update_R(element)
    return smp.S

# Algorithm L is not good for our purpouses
# since we cant easily skip lines in our file
