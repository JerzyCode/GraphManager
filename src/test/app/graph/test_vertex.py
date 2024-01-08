import unittest

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex


class TestVertex(unittest.TestCase):
    def setUp(self):
        self.vertex1 = Vertex('1', 120, 120)
        self.vertex2 = Vertex('2', 120, 120)
        self.vertex3 = Vertex('3', 120, 120)
        self.vertex4 = Vertex('2', 120, 120)
        self.edge_directed1 = Edge(self.vertex1, self.vertex2, True, False, None)
        self.edge_directed2 = Edge(self.vertex2, self.vertex1, True, False, None)
        self.edge_directed3 = Edge(self.vertex1, self.vertex3, True, False, None)
        self.edge_directed4 = Edge(self.vertex1, self.vertex2, True, False, None)

        self.edge_undirected1 = Edge(self.vertex1, self.vertex2, False, False, None)
        self.edge_undirected2 = Edge(self.vertex2, self.vertex1, False, False, None)
        self.edge_undirected3 = Edge(self.vertex2, self.vertex3, False, False, None)
        self.edge_undirected4 = Edge(self.vertex1, self.vertex2, True, False, None)

    def test_add_neighbor(self):
        self.vertex1.add_neighbor(self.vertex2, self.edge_undirected1)
        self.vertex1.add_neighbor(self.vertex3, self.edge_undirected3)

        self.assertEqual(len(self.vertex1.edges), 2)
        self.assertEqual(len(self.vertex1.neighbors), 2)

        self.assertEqual(self.vertex1.edges.__contains__(self.edge_undirected1), True)
        self.assertEqual(self.vertex1.edges.__contains__(self.edge_undirected3), True)
        self.assertEqual(self.vertex1.neighbors[0], self.vertex2)
        self.assertEqual(self.vertex1.neighbors[1], self.vertex3)

    def test_find_edge(self):
        self.fail()
