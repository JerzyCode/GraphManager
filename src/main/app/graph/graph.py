import uuid
from abc import abstractmethod

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex
from src.main.app.utils.logger import setup_logger

logger = setup_logger("Graph")


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
        # logger.debug("Add Vertex")
        self.V.append(vertex)

    def delete_vertex(self, vertex):
        self.V.remove(vertex)
        for edge in list(self.E):
            if edge.vertex1 == vertex or edge.vertex2 == vertex:
                self.delete_edge(edge)

    def delete_edge(self, edge):
        self.E.remove(edge)
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        if edge in vertex1.edges:
            vertex1.edges.remove(edge)
        if edge in vertex2.edges:
            vertex2.edges.remove(edge)
        if vertex1 in vertex2.neighbors:
            vertex2.neighbors.remove(vertex1)
        if vertex2 in vertex1.neighbors:
            vertex1.neighbors.remove(vertex2)

    def add_edge(self, vertex1, vertex2, is_directed, is_digraph, weight):
        # logger.debug("Add Edge")
        if is_digraph:
            is_directed = True
        edge = Edge(vertex1, vertex2, is_directed, digraph=is_digraph, weight=weight)
        vertex1.add_neighbor(vertex2, edge)
        if not is_directed:
            vertex2.add_neighbor(vertex1, edge)
        self.E.add(edge)
        return edge

    def get_vertex_by_label(self, label):
        for vertex in self.V:
            if vertex.label == label:
                return vertex

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
