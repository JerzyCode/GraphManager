import random

from app.graph.Edge import Edge
from app.utils.const import RADIUS, WINDOW_WIDTH, WINDOW_HEIGHT


class Vertex:
    def __init__(self, label, canvas):
        self.x = random.randint(RADIUS, WINDOW_WIDTH - RADIUS)
        self.y = random.randint(RADIUS, WINDOW_HEIGHT - RADIUS - 100)
        self.label = label + ''
        self.edges = set()
        self.canvas = canvas
        self.neighbors = set()

    def add_edge(self, vertex):
        edge = Edge(self, vertex)

    def find_edge_neigh(self, neigh):
        for edge in self.edges:
            if edge.vertex1 == neigh or edge.vertex2 == neigh:
                print(edge)
                return edge

    def add_neighbor(self, vertex):
        self.neighbors.add(vertex)

    def __str__(self):
        return self.label + ', (' + str(self.x) + ', ' + str(self.y) + ')'
