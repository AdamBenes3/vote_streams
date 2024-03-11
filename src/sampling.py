from random import randint, random
from math import exp, floor, log

class sampling:
    def __init__(self, k):
        self.k = k
        self.n = 0
        self.S = [None] * k
    
    def update_R(self, x):
        """
        O(1)
        Input: An integer x, a non-negative integer n, an array s of n elements, and an integer k
        Where:
        - x is the new element
        - n is the number of elements seen so far
        - s is the array of sample elements
        - k is the number of elements to sample
        Output: An integer n' and an array s' of n' elements
        """
        self.n += 1
        if (self.n-1 < self.k):
            self.S[self.n-1] = x
        else:
            i = randint(0, self.n-1)
            if (i < self.k):
                # If i < k, replace the i-th element of s with x
                self.S[i] = x

def algorithm_R(input_array, k):
    """
    O(n)
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    smp = sampling(k)
    for element in input_array:
        smp.update_R(element)
    return smp.S

# The L algorithm is not good for our purpouses
# since we cant easily skip lines in our file