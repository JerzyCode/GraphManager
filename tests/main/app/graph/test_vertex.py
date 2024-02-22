import unittest

import tests.main.app.graph.graph_factory as factory
from src.main.app.graph.edge import Edge


class TestVertex(unittest.TestCase):

    def test_add_neighbor(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        edge = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
        # when
        vertex1.add_neighbor(vertex2, edge)
        # then
        self.assertEqual(len(vertex1.neighbors), 1)
        self.assertEqual(len(vertex1.edges), 1)
        self.assertEqual(list(vertex1.neighbors)[0], vertex2)

    def test_find_edge_undirected(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        edge = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
        vertex1.neighbors.add(vertex2)
        vertex2.neighbors.add(vertex1)
        vertex1.edges.add(edge)
        vertex2.edges.add(edge)
        # when
        result = vertex1.find_edge(vertex2, is_directed=False)
        # then
        self.assertEqual(result, edge)

    def test_find_edge_directed(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        edge = Edge(vertex1, vertex2, directed=True, digraph=False, weight=None)
        vertex1.neighbors.add(vertex2)
        vertex1.edges.add(edge)
        # when
        result_edge1 = vertex1.find_edge(vertex2, is_directed=True)
        result_edge2 = vertex2.find_edge(vertex1, is_directed=True)
        # then
        self.assertEqual(result_edge1, edge)
        self.assertIsNone(result_edge2)
