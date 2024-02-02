from abc import abstractmethod

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex


class Graph:
    def __init__(self, matrix, is_weighted, max_width=None, max_height=None):
        self.matrix = matrix
        self.is_weighted = is_weighted
        self.V = []
        self.E = set()
        self._create_vertexes(max_width, max_height)
        self.__create_edges__(is_weighted)

    def _create_vertexes(self, max_width, max_height):
        size = len(self.matrix)
        for i in range(size):
            self.V.append(Vertex(str(i + 1), max_width, max_height))

    def add_vertex(self, vertex):
        self.V.append(vertex)

    def add_edge(self, vertex1, vertex2, is_directed, is_digraph):
        if is_digraph:
            is_directed = True
        edge = Edge(vertex1, vertex2, is_directed, digraph=is_digraph, weight=None)
        vertex1.add_neighbor(vertex2, edge)
        if not is_directed:
            vertex2.add_neighbor(vertex1, edge)
        self.E.add(edge)
        return edge

    @abstractmethod
    def __create_edges__(self, is_weighted):
        pass

    def __str__(self):
        string = ''
        for vertex in self.V:
            string = 'vertex:' + vertex.label + ": "
            string += 'edges: '
            for ede in vertex.edges:
                string += str(ede) + ', '
            string += 'neighbors: '
            for neigh in vertex.neighbors:
                string += str(neigh) + ', '
            print(string)
        return string
