from typing import Union, Dict, List, Tuple, Dict

class Vertex:
    def __init__(self, name : str = None, *neighbour) -> None:
        if name == None:
            raise TypeError("Vertex must have a name")
        self.name = name
        self.neighbours = []
        if len(neighbour) > 0:
            self.add_neighbour(*neighbour)
        return
    
    def __str__(self) -> str:
        return self.name
    
    def add_neighbour(self, *append : Union[Dict, List]) -> None:
        for app in append:
            if isinstance(app, dict):
                for neighbour, weight in app.items():
                    self.neighbours.append(app)
            elif isinstance(app, list):
                self.neighbours.extend(app)
            else:
                self.neighbours.append(app)
        return
                
    @property
    def neighbours_names(self) -> List[str]:
        return [list(neighbor.keys())[0].name + ":" + str(list(neighbor.values())[0]) for neighbor in self.neighbours]



class Graph:
    def __init__(self, *V : Vertex) -> None:
        self.V = []
        if len(V) > 0:
            self.add_vertex(*V)
        return
    
    def find_by_name(self, vertex : str, neighbour : str) -> Tuple[Vertex, Dict, str]:
        # Find the vertex
        x = None
        for v in self.V:
            if v.name == vertex:
                x = v
                break;
        if x == None:
            raise EOFError("Vertex not found")
        v = x
        # Find the neighbour
        for n in v.neighbours:
            # Look at its key
            for key, _ in n.items():
                if key.name == neighbour:
                    return v, n, key
        raise EOFError("Neighbour not found")
    
    def update_value(self, vertex : str, neighbour : str, value : int) -> None:
        v, n, key = self.find_by_name(vertex, neighbour)
        n[key] = value
        return
    
    def get_value_between(self, vertex : str, neighbour : str) -> int:
        v, n, key = self.find_by_name(vertex, neighbour)
        return n[key]
    
    def __str__(self) -> str:
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
    
    def add_vertex(self, *V : Vertex) -> None:
        for ver in V:
            if isinstance(ver, list):
                self.V = self.V + ver
            else:
                self.V.append(ver)
        return
    
    @property
    def verticies_names(self) -> List[str]:
        return [vertex.name for vertex in self.V]


