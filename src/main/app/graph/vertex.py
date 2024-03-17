import random

from src.main.app.utils.constants import GRAPH_VIEW_WIDTH, GRAPH_VIEW_HEIGHT, MAX_RADIUS


class Vertex:
    def __init__(self, label, max_width=None, max_height=None, x=None, y=None):
        if x is None and y is None:
            self._set_coords(max_width, max_height)
        else:
            self.x = x
            self.y = y
        self.label = label + ''
        self.edges = set()
        self.neighbors = set()
        self.is_highlighted_by_algorithm = False

    def _set_coords(self, max_width, max_height):
        if max_width < 2 * MAX_RADIUS or max_height < 2 * MAX_RADIUS:
            self.x = random.randint(2 * MAX_RADIUS, GRAPH_VIEW_WIDTH - 2 * MAX_RADIUS)
            self.y = random.randint(2 * MAX_RADIUS, GRAPH_VIEW_HEIGHT - 2 * MAX_RADIUS)
        else:
            self.x = random.randint(2 * MAX_RADIUS, max_width - 2 * MAX_RADIUS)
            self.y = random.randint(2 * MAX_RADIUS, max_height - 2 * MAX_RADIUS)

    def find_edge(self, neigh, is_directed):
        if is_directed:
            edge = self.find_edge_directed(neigh)
        else:
            edge = self.find_edge_undirected(neigh)
        return edge

    def find_edge_directed(self, neigh):
        print(f'neigh={neigh}')
        for edge in self.edges:
            if edge.vertex2 == neigh:
                return edge

    def find_edge_undirected(self, neigh):
        for edge in self.edges:
            if edge.vertex2 == neigh or edge.vertex1 == neigh:
                return edge

    def add_neighbor(self, vertex, edge):
        self.neighbors.add(vertex)
        self.edges.add(edge)

    def __str__(self):
        return f'label={self.label}'

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.label == other.label
        return False

    def __hash__(self):
        return hash('vertex' + self.label)
