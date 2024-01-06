import random
from src.app.utils.const import *


class Vertex:
    def __init__(self, label, max_width, max_height):
        self.x = None
        self.y = None
        self.set_coords(max_width, max_height)
        self.label = label + ''
        self.edges = set()
        self.neighbors = []

    def set_coords(self, max_width, max_height):
        if max_width < 2 * RADIUS or max_height < 2 * RADIUS:
            self.x = random.randint(2 * RADIUS, GRAPH_VIEW_WIDTH - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, GRAPH_VIEW_HEIGHT - 2 * RADIUS)
        else:
            self.x = random.randint(2 * RADIUS, max_width - 2 * RADIUS)
            self.y = random.randint(2 * RADIUS, max_height - 2 * RADIUS)

    def find_edge(self, neigh, is_directed):
        if is_directed:
            edge = self.find_edge_directed(neigh)
        else:
            edge = self.find_edge_undirected(neigh)
        # print(edge)
        return edge

    def find_edge_directed(self, neigh):
        for edge in self.edges:
            if edge.vertex2 == neigh:
                return edge

    def find_edge_undirected(self, neigh):
        for edge in self.edges:
            if edge.vertex2 == neigh or edge.vertex1 == neigh:
                print('find_edge', str(edge))
                return edge

    def add_neighbor(self, vertex, edge):
        self.neighbors.append(vertex)
        self.edges.add(edge)

    def __str__(self):
        return self.label
