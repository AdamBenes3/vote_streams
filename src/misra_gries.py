from math import floor
import heapq

class MisraGries:
    
    def __init__(self, k):
        self.D1 = {}
        self.D2 = {}
        self.H = []
        self.k = k
        self.s = 0

    def misra_gries_update(self, element):
        """
        O(k)
        Input: An element
        Output: None
        """
        
        # If the element is already in the dictionary, increase the counter
        if (element in self.D1):
            self.D1[element] += 1
            return
        
        # If the element is not in the dictionary, add it if there is space
        if (len(self.D1) <= self.k-1):
            self.D1[element] = 1
            return
        
        keys_to_delete = []
        for key in self.D1:
            # Decrease the counter of each key
            self.D1[key] -= 1
            if (self.D1[key] == 0):
                # Add the key to the list of keys to delete because the counter is 0
                keys_to_delete.append(key)
        # Delete the keys with counter 0
        for key in keys_to_delete:
            del self.D1[key]

    def misra_gries_update_with_heap(self, element):
        """
        O(log(k))
        Input: An element
        Output: None
        """
        
        # If the element is already in the dictionary, increase the counter
        if element in self.D2:
            self.D2[element][0] += 1
            return
        
        # If the element is not in the dictionary, add it if there is space
        if len(self.D2) < self.k - 1:
            heapq.heappush(self.H, (1, element))
            self.D2[element] = [1, 1]
            return
        
        self.s += 1
        # while the minimum is less or equal to s we drop it 
        while self.H and self.D2[self.H[0][1]][0] <= self.s:
            _, elem = heapq.heappop(self.H) # "_, elem" is little wierd
                                            #  but it means that we drop the first item
                                            #  and are jusinterested in the second one 
            self.D2.pop(elem)


def misra_gries(k, input_array):
    """
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize the Misra-Gries object
    mg = MisraGries(k)
    # Update the Misra-Gries object with the input array
    for element in input_array:
        mg.misra_gries_update(element)
    # Return the dictionary of the Misra-Gries object
    return list(mg.D1)

def misra_gries_with_heap(k, input_array):
    """
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize the Misra-Gries object
    mg = MisraGries(k)
    # Update the Misra-Gries object with the input array
    for element in input_array:
        mg.misra_gries_update_with_heap(element)
    # Return the dictionary of the Misra-Gries object
    return list(mg.D2)

# print(misra_gries(2, [1, 4, 5, 4, 4, 5, 4, 4])) # [4]