# Add main directory to path
import sys
import os
main_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if main_directory not in sys.path:
    sys.path.append(main_directory)

from typing import Union, Dict, List, Tuple, Dict

class Vertex:
    def __init__(self, name : str = None, *neighbour) -> None:
        if name == None:
            raise TypeError("Vertex must have a name")
        self.name = name
        self.neighbours = []
        # Add the neightbours
        if len(neighbour) > 0:
            self.add_neighbour(*neighbour)
        return
    
    def __str__(self) -> str:
        return self.name
    
    def add_neighbour(self, *append : Union[Dict, List]) -> None:
        """
        Adding neighbor 
        """
        for app in append:
            # If we care also about weights connected to neighbours
            if isinstance(app, dict):
                for neighbour, weight in app.items():
                    self.neighbours.append(app)
            # If neighbors are just item without weight
            elif isinstance(app, list):
                self.neighbours.extend(app)
            else:
                self.neighbours.append(app)
        return
                
    @property
    def neighbours_names(self) -> List[str]:
        # Transform the neighbours to string by theyr name
        return [list(neighbor.keys())[0].name + ":" + str(list(neighbor.values())[0]) for neighbor in self.neighbours]



class Graph:
    def __init__(self, *V : Vertex) -> None:
        self.V = []
        if len(V) > 0:
            self.add_vertex(*V)
        return
    
    def find_by_name(self, vertex : str, neighbour : str) -> Tuple[Vertex, Dict, str]:
        """
        Find the vertex with given name (names are strings)
        """
        # Find the vertex
        x = None
        for v in self.V:
            if v.name == vertex:
                x = v
                break
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
        """
        Update the value of vertex -- neighbour
        """
        # Find the verticies by names
        v, n, key = self.find_by_name(vertex, neighbour)
        n[key] = value
        return
    
    def get_value_between(self, vertex : str, neighbour : str) -> int:
        """
        Returns the value get two verticies
        """
        # Find the verticies by names
        v, n, key = self.find_by_name(vertex, neighbour)
        return n[key]
    
    def __str__(self) -> str:
        """
        Returns the graph as a string (nicely readable)
        """
        result = ""
        for vertex in self.V:
            result += vertex.name + ": "
            # Adds the neighbors after the : so its is nicely readable
            for neighbour in vertex.neighbours:
                result += list(neighbour.keys())[0].name + ":" + str(list(neighbour.values())[0]) + ", "
            if result.endswith(", "):
                result = result[:-2]
            result += "\n"
        if result.endswith("\n"):
                result = result[:-1]
        return result
    
    def add_vertex(self, *V : Vertex) -> None:
        """
        Adds the vertex to the graph
        """
        for ver in V:
            # If it is a list of verticies adds it as that
            if isinstance(ver, list):
                self.V = self.V + ver
            # Otherwise adds it as one vertex
            else:
                self.V.append(ver)
        return
    
    @property
    def verticies_names(self) -> List[str]:
        # Transform the verticies to string by theyr name
        return [vertex.name for vertex in self.V]


