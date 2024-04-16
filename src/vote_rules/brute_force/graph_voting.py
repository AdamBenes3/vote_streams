from graph import Graph, Vertex
from typing import List

votes = [["a", "b", "c", "d"], ["d", "b", "c", "a"], ["d", "c", "a", "b"], ["d", "c", "a", "b"], ["d", "c", "a", "b"]]

def inicilize_complete_graph(vertecies : List[str]) -> Graph:
    V = []
    for i in first_vote:
        V.append(Vertex(i))
    for v in V:
        for i in V:
            if v != i:
                v.add_neighbour({i : 0})
    G = Graph(V)
    return G

first_vote = votes[0]

G = inicilize_complete_graph(first_vote)

def voting(votes : List[str], G : Graph) -> Graph:
    for vote in votes:
        for idx_i, i in enumerate(vote):
            for idx_j, j in enumerate(vote):
                if idx_i < idx_j:
                    x = G.get_value_between(i, j) + 1
                    G.update_value(i, j, x)
                    x = G.get_value_between(j, i) - 1
                    G.update_value(j, i, x)
    return G

G = voting(votes, G)

def find_winner(G : Graph) -> Vertex:
    best_vertex = G.V[0]
    best_counter = -1
    for v in G.V:
        positive_counter = 0
        for n in v.neighbours:
            for key, _ in n.items():
                if n[key] > 0:
                    positive_counter += 1
        if positive_counter > best_counter:
            best_counter = positive_counter
            best_vertex = v
    return best_vertex
        
v = find_winner(G)

print(v)

