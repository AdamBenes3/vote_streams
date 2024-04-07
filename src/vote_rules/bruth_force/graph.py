class Graph:
    def __init__(self, *V):
        self.V = []
        if len(V) > 0:
            self.add_vertex(*V)
    
    def find_by_name(self, vertex, neighbour):
        # Find the vertex
        for v in self.V:
            if v.name == vertex:
                # Find the neighbour
                for n in v.neighbours:
                    # Look at its key
                    for key, _ in n.items():
                        if key.name == neighbour:
                            return v, n, key
    
    def update_value(self, vertex, neighbour, value) -> None:
        v, n, key = self.find_by_name(vertex, neighbour)
        print(v, n, key)
        n[key] = value
        return
    
    def get_value_between(self, vertex, neighbour) -> int:
        v, n, key = self.find_by_name(vertex, neighbour)
        return n[key]
    
    def __str__(self):
        result = ""
        for vertex in self.V:
            result += vertex.name + ": "
            for neighbour in vertex.neighbours:
                result += list(neighbour.keys())[0].name + ":" + str(list(neighbour.values())[0]) + ", "
            if result.endswith(", "):
                result = result[:-2]
            result += "\n"
        if result.endswith("\n"):
                result = result[:-1]
        return result
    
    def add_vertex(self, *V):
        for ver in V:
            if isinstance(ver, list):
                self.V = self.V + ver
            else:
                self.V.append(ver)
    
    @property
    def verticies_names(self):
        return [vertex.name for vertex in self.V]

    

class Vertex:
    def __init__(self, name = None, *neighbour):
        if name == None:
            raise TypeError("Vertex must have a name")
        self.name = name
        self.neighbours = []
        if len(neighbour) > 0:
            self.add_neighbour(*neighbour)
    
    def __str__(self):
        return self.name
    
    def add_neighbour(self, *append):
        for app in append:
            if isinstance(app, dict):
                for neighbour, weight in app.items():
                    self.neighbours.append(app)
            elif isinstance(app, list):
                self.neighbours.extend(app)
            else:
                self.neighbours.append(app)
                
    @property
    def neighbours_names(self):
        return [list(neighbor.keys())[0].name + ":" + str(list(neighbor.values())[0]) for neighbor in self.neighbours]



A = Vertex("a")

B = Vertex("b", [{A : 1}])

C = Vertex("c")

A.add_neighbour([{B : 3}, {C : 4}])

B.add_neighbour({C : 5})

C.add_neighbour({A : 7}, [{B : 2}])

G = Graph([A, B], C)

print(G)

print(G.verticies_names)

print(G.V[0].neighbours_names)

print("------")

x = G.get_value_between("a", "b") + 3

print(x)

G.update_value("a", "b", x)

print(A.neighbours)
