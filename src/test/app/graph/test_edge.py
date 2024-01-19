import unittest

from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex


class TestEdge(unittest.TestCase):
    def setUp(self):
        vertex1 = Vertex('1', 120, 120)
        vertex2 = Vertex('2', 120, 120)
        vertex3 = Vertex('3', 120, 120)
        vertex4 = Vertex('2', 120, 120)
        self.edge_directed1 = Edge(vertex1, vertex2, True, False, None)
        self.edge_directed2 = Edge(vertex2, vertex1, True, False, None)
        self.edge_directed3 = Edge(vertex2, vertex3, True, False, None)
        self.edge_directed4 = Edge(vertex1, vertex2, True, False, None)

        self.edge_undirected1 = Edge(vertex1, vertex2, False, False, None)
        self.edge_undirected2 = Edge(vertex2, vertex1, False, False, None)
        self.edge_undirected3 = Edge(vertex2, vertex3, False, False, None)
        self.edge_undirected4 = Edge(vertex1, vertex2, True, False, None)

    def test_edge_directed(self):
        self.assertEqual(self.edge_directed1 == self.edge_directed2, False)
        self.assertEqual(self.edge_directed1 == self.edge_directed3, False)
        self.assertEqual(self.edge_directed1 == self.edge_directed4, True)

    def test_edge_undirected(self):
        self.assertEqual(self.edge_undirected1 == self.edge_undirected2, True)
        self.assertEqual(self.edge_undirected1 == self.edge_undirected3, False)
        self.assertEqual(self.edge_undirected1 == self.edge_undirected4, True)


if __name__ == '__main__':
    unittest.main()
