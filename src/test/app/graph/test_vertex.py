import unittest

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex


class TestVertex(unittest.TestCase):
    def setUp(self):
        self.vertex1 = Vertex('1', 120, 120)
        self.vertex2 = Vertex('2', 120, 120)
        self.edge_directed_v1_v2 = Edge(self.vertex1, self.vertex2, True, False, None)
        self.edge_directed_v2_v1 = Edge(self.vertex2, self.vertex1, True, False, None)

        self.edge_undirected_v1_v2 = Edge(self.vertex1, self.vertex2, False, False, None)
        self.edge_undirected_v2_v1 = Edge(self.vertex2, self.vertex1, False, False, None)

    def test_add_neighbor_directed_edge(self):
        self.vertex1.add_neighbor(self.vertex2, self.edge_directed_v1_v2)
        self.assertEqual(len(self.vertex1.neighbors), 1)
        self.assertEqual(len(self.vertex2.neighbors), 0)
        self.assertEqual(len(self.vertex1.edges), 1)
        self.assertEqual(len(self.vertex2.edges), 0)
        self.assertEqual(list(self.vertex1.neighbors)[0], self.vertex2)

    def test_add_neighbor_undirected_edge(self):
        self.vertex1.add_neighbor(self.vertex2, self.edge_undirected_v1_v2)
        self.vertex2.add_neighbor(self.vertex1, self.edge_undirected_v2_v1)
        self.assertEqual(len(self.vertex1.neighbors), 1)
        self.assertEqual(len(self.vertex2.neighbors), 1)
        self.assertEqual(len(self.vertex1.edges), 1)
        self.assertEqual(len(self.vertex2.edges), 1)
        self.assertEqual(list(self.vertex1.neighbors)[0], self.vertex2)
        self.assertEqual(list(self.vertex2.neighbors)[0], self.vertex1)

    def test_find_edge_directed(self):
        self.vertex1.add_neighbor(self.vertex2, self.edge_directed_v1_v2)
        self.vertex2.add_neighbor(self.vertex1, self.edge_directed_v2_v1)

        edge = self.vertex1.find_edge(self.vertex2, True)
        self.assertEqual(edge, self.edge_directed_v1_v2)
        self.assertNotEqual(edge, self.edge_directed_v2_v1)

    def test_find_edge_undirected(self):
        self.vertex1.add_neighbor(self.vertex2, self.edge_undirected_v1_v2)
        self.vertex2.add_neighbor(self.vertex1, self.edge_undirected_v2_v1)

        edge = self.vertex1.find_edge(self.vertex2, False)
        self.assertEqual(edge, self.edge_undirected_v1_v2)
        self.assertEqual(edge, self.edge_undirected_v2_v1)
