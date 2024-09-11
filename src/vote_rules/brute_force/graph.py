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
        self.neighbours =  []
        self.neighbours_name_dict =  {}
        # Add the neightbours
        if len(neighbour) > 0:
            self.add_neighbour(*neighbour)
        return
    
    def __str__(self) -> str:
        return self.name
    
    def add_neighbour(self, *append : Union[Dict, List]) -> None:
        """
        Adding neighbor and adding it to neighbout dict
        """
        for app in append:
            # If we care also about weights connected to neighbours
            if isinstance(app, dict):
                for neighbour, _ in app.items():
                    self.neighbours.append(app)
                    self.neighbours_name_dict[neighbour.name] = app
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
        # Dictionary to store vertices with their names as keys
        self.V = []
        self.verticies_names_dict = {}
        if len(V) > 0:
            self.add_vertex(*V)
        return
    

    def find_by_name(self, vertex : str, neighbour : str) -> Tuple[Vertex, Dict, str]:
        """
        Find the vertex with given name (names are strings)
        """
        v = self.verticies_names_dict[vertex]
        if v == None:
            raise EOFError("Vertex not found")
        
        n = v.neighbours_name_dict[neighbour]
        if n == None:
            raise EOFError("Neighbour not found")

        for key, _ in n.items():
            return v, n, key
    
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
        for vertex_name, vertex in self.vertices.items():
            result += vertex_name + ": "
            # Adds the neighbors after the : so it's nicely readable
            for neighbour_name, (neighbour_obj, weight) in vertex.neighbours.items():
                result += f"{neighbour_name}:{weight}, "
            if result.endswith(", "):
                result = result[:-2]
            result += "\n"
        if result.endswith("\n"):
            result = result[:-1]
        return result
    
    def add_vertex(self, *V : Vertex) -> None:
        """
        Adds the vertex to the graph and maps the vertex name to the vertex object.
        """
        for ver in V:
            # If it's a list of vertices, add each one
            if isinstance(ver, list):
                self.V = self.V + ver
                for vertex in ver:
                    self.verticies_names_dict[vertex.name] = vertex
            # Otherwise, add the single vertex
            else:
                self.V.append(ver)
                self.verticies_names_dict[ver.name] = ver
        return
    
    @property
    def verticies_names(self) -> List[str]:
        # Transform the verticies to string by theyr name
        return [vertex.name for vertex in self.V]