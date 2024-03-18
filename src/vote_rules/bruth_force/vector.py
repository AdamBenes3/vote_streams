class Vector:
    def __init__(self, lst = []):
        self.lst = lst 
    
    def __add__(self_1, self_2):
        if (len(self_1.lst) >= len(self_2.lst)):
            return_list = self_1.lst
            i = 0
            for item in self_2.lst:
                return_list[i] += item
                i += 1 
            return Vector(return_list)
        else:
            return_list = self_2.lst
            i = 0
            for item in self_1.lst:
                return_list[i] += item
                i += 1 
            return Vector(return_list)

    def __sub__(self_1, self_2):
        minus = []
        i = 0
        for item in self_2.lst:
            minus.append(-1 * item)
            i += 1
        minus_vector = Vector(minus)
        return self_1 + minus_vector

    def __str__(self):
        return "(" + ', '.join(str(element) for element in self.lst) + ")"
