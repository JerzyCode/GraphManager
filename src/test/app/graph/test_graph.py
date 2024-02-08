import unittest

from src.main.app.graph.edge import Edge
from src.main.app.graph.graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        matrix = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]
        self.graph = Graph(matrix, is_weighted=False, max_width=123, max_height=123)
        self.vertex1 = self.graph.V[0]
        self.vertex2 = self.graph.V[1]

    def test__init__(self):
        matrix = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]

        self.graph = Graph(matrix, is_weighted=False, max_width=123, max_height=123)
        vertexes = self.graph.V
        self.assertEqual(len(vertexes), 3)
        self.assertEqual(vertexes[0].label, '1')
        self.assertEqual(vertexes[1].label, '2')
        self.assertEqual(vertexes[2].label, '3')

    def test_add_edge(self):
        # given
        edge = Edge(self.vertex1, self.vertex2, True, False, False)

        # when
        self.graph.add_edge(self.vertex1, self.vertex2, True, False)

        # then
        self.assertTrue(edge in self.graph.E)
        self.assertTrue(edge in self.vertex1.edges)
        self.assertTrue(self.vertex2 in self.vertex1.neighbors)
        self.assertFalse(self.vertex1 in self.vertex2.neighbors)
        self.assertFalse(edge in self.vertex2.edges)

    def test_delete_edge(self):
        # given
        edge = Edge(self.vertex1, self.vertex2, True, False, False)
        self.graph.add_edge(self.vertex1, self.vertex2, True, False)
        # when
        self.graph.delete_edge(edge)

        # then
        self.assert_after_edge_deleted(edge)

    def test_delete_vertex(self):
        # given
        edge = Edge(self.vertex1, self.vertex2, True, False, False)
        self.graph.add_edge(self.vertex1, self.vertex2, True, False)

        # when
        self.graph.delete_vertex(self.vertex1)

        # then
        self.assertTrue(self.vertex1 not in self.graph.V)
        self.assert_after_edge_deleted(edge)

    def assert_after_edge_deleted(self, edge):
        self.assertTrue(edge not in self.graph.E)
        self.assertTrue(self.vertex1 not in self.vertex2.neighbors)
        self.assertTrue(self.vertex2 not in self.vertex1.neighbors)
        self.assertTrue(edge not in self.vertex1.edges)
        self.assertTrue(edge not in self.vertex2.edges)
