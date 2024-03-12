from math import floor
import heapq

class MisraGries:
    
    def __init__(self, k, with_heap = True):
        self.D = {}
        self.k = k
        self.__with_heap__ = with_heap
        if (with_heap):
            self.H = []
            self.s = 0
            

    def misra_gries_update(self, element):
        """
        Update counts using either a heap or without a heap based on the initialization parameter.
        """
        if self.__with_heap__:
            self.__misra_gries_update_with_heap__(element)
        else:
            self.__misra_gries_update_without_heap__(element)

    def __misra_gries_update_without_heap__(self, element):
        """
        O(k)
        Input: An element
        Output: None
        """
        
        # If the element is already in the dictionary, increase the counter
        if (element in self.D):
            self.D[element] += 1
            return
        
        # If the element is not in the dictionary, add it if there is space
        if (len(self.D) <= self.k-1):
            self.D[element] = 1
            return
        
        keys_to_delete = []
        for key in self.D:
            # Decrease the counter of each key
            self.D[key] -= 1
            if (self.D[key] == 0):
                # Add the key to the list of keys to delete because the counter is 0
                keys_to_delete.append(key)
        # Delete the keys with counter 0
        for key in keys_to_delete:
            del self.D[key]

    def __misra_gries_update_with_heap__(self, element):
        """
        O(log(k))
        Input: An element
        Output: None
        """
        
        # If the element is already in the dictionary, increase the counter
        if element in self.D:
            self.D[element][0] += 1
            return
        
        # If the element is not in the dictionary, add it if there is space
        if len(self.D) < self.k - 1:
            heapq.heappush(self.H, (1, element))
            self.D[element] = [1, 1]
            return
        
        self.s += 1
        # while the minimum is less or equal to s we drop it 
        while self.H and self.D[self.H[0][1]][0] <= self.s:
            _, elem = heapq.heappop(self.H) # "_, elem" is little wierd
                                            #  but it means that we drop the first item
                                            #  and are jusinterested in the second one 
            self.D.pop(elem)


def misra_gries(k, input_array):
    """
    Used mainly for testing
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize the Misra-Gries
    mg = MisraGries(k, False)
    # run as a stream
    for element in input_array:
        mg.misra_gries_update(element)
    # Return the dictionary of the Misra-Gries object
    return list(mg.D)

def misra_gries_with_heap(k, input_array):
    """
    Used mainly for testing
    Input: An array of n elements and an integer k
    Output: An array of k elements
    """
    # Initialize the Misra-Gries
    mg = MisraGries(k)
    # run as a stream
    for element in input_array:
        mg.misra_gries_update(element)
    # Return the dictionary of the Misra-Gries object
    return list(mg.D)

# print(misra_gries(2, [1, 4, 5, 4, 4, 5, 4, 4])) # [4]