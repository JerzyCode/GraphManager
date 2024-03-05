import random as rd
from abc import ABC

from src.main.app.graph.edge import Edge
from src.main.app.graph.graph import Graph


class UndirectedGraph(Graph, ABC):
    def __init__(self, matrix=None, is_weighted=None, max_width=None, max_height=None):
        super().__init__(matrix, is_weighted, max_width, max_height)
        if self.matrix is not None:
            self.__create_edges__(self.is_weighted)

    def __create_edges__(self, is_weighted):
        size = len(self.matrix)
        for i in range(size):
            for j in range(i, size):
                if i != j and self.matrix[i][j] == 1:
                    weight = None
                    if is_weighted:
                        weight = rd.randint(0, 20)
                    edge = Edge(self.V[i], self.V[j], directed=False, digraph=False, weight=weight)
                    self.V[i].add_neighbor(self.V[j], edge)
                    self.V[j].add_neighbor(self.V[i], edge)
                    self.E.add(edge)


def generate_graph(n, probability, max_width, max_height, is_weighted):
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
                    matrix[j][i] = 1
    return UndirectedGraph(matrix, is_weighted, max_width, max_height)
