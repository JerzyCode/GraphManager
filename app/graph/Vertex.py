import random

from app.graph.Edge import Edge
from app.utils.const import *


class Vertex:
    def __init__(self, label, max_width, max_height):
        self.x = None
        self.y = None
        self.set_coords(max_width, max_height)
        self.label = label + ''
        self.edges = set()
        self.neighbors = set()

    def set_coords(self, max_width, max_height):
        if max_width < 2 * RADIUS or max_height < 2 * RADIUS:
            self.x = random.randint(2 * RADIUS, GRAPH_VIEW_WIDTH - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, GRAPH_VIEW_HEIGHT - 2 * RADIUS)
        else:
            self.x = random.randint(2 * RADIUS, max_width - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, max_height - 2 * RADIUS)

    def find_edge_neigh(self, neigh):
        for edge in self.edges:
            if edge.vertex1 == neigh or edge.vertex2 == neigh:
                print(edge)
                return edge

    def add_neighbor(self, vertex):
        self.neighbors.add(vertex)

    def __str__(self):
        return self.label
