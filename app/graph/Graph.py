import random

from app.graph.Edge import Edge
from app.graph.Vertex import Vertex


class Graph:
    def __init__(self, matrix, canvas):
        self.matrix = matrix
        self.V = {}
        self.E = set()
        self.canvas = canvas
        self.create_vertexes()
        self.create_edges()

    def create_vertexes(self):
        size = len(self.matrix)
        for i in range(size):
            self.V[i] = Vertex(str(i + 1), self.canvas)

    def create_edges(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(i, size):
                if i != j and self.matrix[i][j] == 1:
                    self.V[i].add_edge(self.V[j])
                    self.E.add(Edge(self.V[i], self.V[j]))

    def find_edge(self, edge_label):
        for edge in self.E:
            if edge_label == edge.label:
                return edge
        return None


def generate_graph(n, canvas):
    A = generate_2d_array(n)
    for i in range(n):
        for j in range(i + 1, n):
            if i != j:
                rand = random.choice([0, 1])
                A[i][j] = rand
                A[j][i] = rand
    return Graph(A, canvas)


def generate_2d_array(n):
    return [[0] * n for _ in range(n)]



