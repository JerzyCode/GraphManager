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

    def add_edge(self, vertex):
        edge = Edge(self, vertex)

    def __str__(self):
        return self.label + ', (' + str(self.x) + ', ' + str(self.y) + ')'
