from random import randint, random
from math import exp, floor, log

def basic_sampling_algorithm(input_array, k):
    """
    O(n)
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    output_array = []
    i = 0
    for element in input_array:
        # If i < k, add the element to the output array
        if (i < k):
            output_array.append(element)
        # If i >= k, try replacing a random element in the output array with the current element
        else:
            j = randint(0, i)
            if (j < k):
                output_array[j] = element
        i += 1
    return output_array

def random_sample_update(x, n, s, k):
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
    n += 1
    i = randint(0, n-1)
    # If i < k, replace the i-th element of s with x
    if (i < k):
        s[i] = x
    # Return the new values of n and s
    return n, s

