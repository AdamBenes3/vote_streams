class stv:
    def __init__(self, lst):
        self.lst =lst 
        
    def find_least_winner(self, D):
        if not D:
            return None
        
        min = []
        
        first_key = next(iter(D))  # Get the first key
        minimum = D[first_key]
        
        for key, value in D.items():
            if value < minimum:
                minimum = value
                min = [key]
            elif value == minimum:
                min.append(key)
        return min
        # print(min)

    def remove_worst(self):
        D = {}
        for i in self.lst:
            if i != []:
                if i[0] in D:
                    D[i[0]] += 1
                else:
                    D[i[0]] = 1
        # print(D)
        to_pop = self.find_least_winner(D)
        for i in to_pop:
            for j in self.lst:
                counter = 0
                for q in j:
                    if q == i:
                        j.pop(counter)
                    counter += 1
    
    def find_winner(self):
        while True:
            print(self.lst)
            self.remove_worst()
        
            
    
lst = [[4, 2, 3], [3, 1, 3], [4, 1, 3], [9, 1, 3]]

S = stv(lst)
S.find_winner()