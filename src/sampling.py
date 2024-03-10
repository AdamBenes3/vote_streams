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

def basic_sampling_algorithm(input_array, k):
    """
    O(n)
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    smp = sampling(k)
    for element in input_array:
        smp.update_R(element)
    return smp.S



def sampling_algorithm_L(input_array, k):
    """
    O(k(1 + log(n/k)))
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize reservoir with the first k elements of S
    output_array = input_array[:k]
    # Initialize W
    w = exp(log(random()) / k)
    # Start from the k+1-th element
    i = k
    while True:
        # Calculate the index to skip to
        i = i + floor(log(random()) / log(1 - w)) + 1
        # immitate the behavior of: if skip_to_index < n:
        try:
            # Replace a random item in the reservoir with the item at index skip_to_index
            random_index = randint(0, k - 1)
            output_array[random_index] = input_array[i]
            
            # Update W
            w *= exp(log(random()) / k)
        except IndexError:
            return output_array

# Example usage
# input_array = list(range(11))
# k = 10
# num_trials = 1000
# for _ in range(num_trials):
#     output_array = basic_sampling_algorithm(input_array, k)
#     print(output_array)
#     print()