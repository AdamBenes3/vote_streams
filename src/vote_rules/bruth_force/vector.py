from typing import List

class Vector:
    def __init__(self, lst : List[int] = []) -> None:
        self.lst = lst
        return
    
    def __add__(self_1: 'Vector', self_2: 'Vector') -> 'Vector':
        if len(self_1.lst) >= len(self_2.lst):
            return_list = self_1.lst.copy()
            for i, item in enumerate(self_2.lst):
                return_list[i] += item
            return Vector(return_list)
        else:
            return_list = self_2.lst.copy()
            for i, item in enumerate(self_1.lst):
                return_list[i] += item
            return Vector(return_list)

    def __sub__(self_1 : 'Vector', self_2 : 'Vector') -> 'Vector':
        minus = [-item for item in self_2.lst]
        minus_vector = Vector(minus)
        return self_1 + minus_vector

    def __str__(self) -> str:
        return "(" + ', '.join(str(element) for element in self.lst) + ")"
