import random

from app.graph.Edge import Edge
from app.utils.const import *


class Vertex:
    def __init__(self, label, canvas):
        self.x = None
        self.y = None
        self.set_coords(canvas)
        self.label = label + ''
        self.edges = set()
        self.canvas = canvas
        self.neighbors = set()

    # def add_edge(self, vertex):
    #     edge = Edge(self, vertex)

    def set_coords(self, canvas):
        if canvas.winfo_width() < 2 * RADIUS or canvas.winfo_height() < 2 * RADIUS:
            self.x = random.randint(2 * RADIUS, GRAPH_VIEW_WIDTH - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, GRAPH_VIEW_HEIGHT - 2 * RADIUS)
        else:
            self.x = random.randint(2 * RADIUS, canvas.winfo_width() - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, canvas.winfo_height() - 2 * RADIUS)

    def find_edge_neigh(self, neigh):
        for edge in self.edges:
            if edge.vertex1 == neigh or edge.vertex2 == neigh:
                print(edge)
                return edge

    def add_neighbor(self, vertex):
        self.neighbors.add(vertex)

    def __str__(self):
        return self.label + ', (' + str(self.x) + ', ' + str(self.y) + ')'
