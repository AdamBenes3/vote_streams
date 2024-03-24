class Graph:
    def __init__(self, V = [], E = []):
        self.V = V
        self.E = E

    def __str__(self):
        str = ""
        for vertex in self.V:
            str += vertex.name + ": "
            for neighbour in vertex.neighbours:
                str += neighbour.name + ", "
            str += "\n"
        return str

    

class Vertex:
    def __init__(self, name = None, neighbours = [], value = None):
        if not isinstance(neighbours, list):
            raise TypeError("neighbours must be a list")
        for neighbour in neighbours:
            if not isinstance(neighbour, Vertex):
                raise TypeError("neighbour must be a Vertex")
        if name == None:
            raise TypeError("Vertex must have a name")
        self.name = name
        self.value = value
        self.neighbours = neighbours


class Edge:
    def __init__(self, vertices = [], value = None):
        if not isinstance(vertices, list):
            raise TypeError("vertices must be a list")
        self.vertices = vertices
        self.value = value

x = Vertex("X")

y = Vertex("Y")

x.neighbours = [y, x]
y.neighbours = [x, x]

g = Graph([x, y], [])

print(g)
