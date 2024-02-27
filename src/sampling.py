from random import randint, random
from math import exp, floor, log

def basic_sampling_algorithm(input_array, k):
    """
    O(n)
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize reservoir with the first k elements of S
    output_array = input_array[:k]
    i = k
    for element in input_array:
        # If i >= k, try replacing a random element in the output array with the current element
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
    for _ in input_array[k:]:
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
    return output_array

# Example usage
# input_array = list(range(500))
# k = 10
# num_trials = 10
# for _ in range(num_trials):
#     output_array = basic_sampling_algorithm(input_array, k)
#     print(output_array)
#     output_array = sampling_algorithm_L(input_array, k)
#     print(output_array)
#     print()