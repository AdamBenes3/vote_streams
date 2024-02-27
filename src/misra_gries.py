from math import floor


def misra_gries(k, input_array):
    """
    O(k(log(m)+log(n))) where m is the number of distinct elements in the input array and n is the number of elements in the input array
    Input: An integer k and an array of n elements
    k is number that says that n/k is the minimum frequency of the elements that we want to count
    Output: A list (if list wanted change the return type to dictionary) with the elements that appear at least floor(n/k) times
    """
    # print("n/k = " + str(floor(len(input_array)/k))) <-- uncomment this line to see the value of n/k, very useful for debugging
    output_dict = {}
    for element in input_array:
        # If the element is already in the dictionary, increase the counter
        if (element in output_dict):
            output_dict[element] += 1
        # If the element is not in the dictionary, add it if there is space
        elif (len(output_dict) < k-1):
            output_dict[element] = 1
        else:
            keys_to_delete = []
            for key in output_dict:
                # Decrease the counter of each key
                output_dict[key] -= 1
                if (output_dict[key] == 0):
                    # Add the key to the list of keys to delete because the counter is 0
                    keys_to_delete.append(key)
            # Delete the keys with counter 0
            for key in keys_to_delete:
                del output_dict[key]
    return list(output_dict) # return output_dict

