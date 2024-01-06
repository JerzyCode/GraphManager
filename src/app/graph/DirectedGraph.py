from abc import ABC
import random as rd
from src.app.graph.Edge import Edge
from src.app.graph.Graph import Graph


class DirectedGraph(Graph, ABC):
    def __init__(self, matrix, max_width, max_height):
        super().__init__(matrix, max_width, max_height)
        self.__create_edges__()

    def __create_edges__(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(size):
                if i != j and self.matrix[i][j] == 1:
                    edge = Edge(self.V[i], self.V[j], True, digraph=False, weight=None)
                    self.V[i].add_neighbor(self.V[j], edge)
                    self.E.add(edge)


def generate_graph(n, probability, max_width, max_height):
    if probability < 0 or probability > 1:
        probability = 0.5
    matrix = [[0] * n for _ in range(n)]
    probability = int(probability * 100)
    for i in range(n):
        for j in range(n):
            if i != j:
                rand = rd.randint(1, 100)
                if rand <= probability:
                    matrix[i][j] = 1
                    matrix[j][i] = 0
    return DirectedGraph(matrix, max_width, max_height)
