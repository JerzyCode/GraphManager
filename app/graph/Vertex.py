import random

from app.graph.Edge import Edge
from app.graph.graphics.Drawer import Drawer


class Vertex:
    def __init__(self, label, canvas):
        self.label = label
        self.edges = []
        self.canvas = canvas
        self.drawer = Drawer(self, random.uniform(25, 400), random.uniform(25, 400), canvas)

    def add_edge(self, vertex):
        edge = Edge(self, vertex)
        self.drawer.draw_edge(edge)
