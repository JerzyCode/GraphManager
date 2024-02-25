import unittest

import tests.main.app.graph.graph_factory as factory
from src.main.app.graph.edge import Edge


class TestEdge(unittest.TestCase):

    def test_create_edge_undirected(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        label = vertex1.label + '_' + vertex2.label
        # when
        edge = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
        # then
        self.assertFalse(edge.directed)
        self.assertFalse(edge.digraph)
        self.assertIsNone(edge.weight)
        self.assertEqual(edge.label, label)

    def test_create_edge_directed(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        label = vertex1.label + '_' + vertex2.label
        # when
        edge = Edge(vertex1, vertex2, directed=True, digraph=False, weight=None)
        # then
        self.assertTrue(edge.directed)
        self.assertFalse(edge.digraph)
        self.assertIsNone(edge.weight)
        self.assertEqual(edge.label, label)

    def test_create_edge_weighted(self):
        # given
        weight = 100
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        label = vertex1.label + '_' + vertex2.label
        # when
        edge = Edge(vertex1, vertex2, directed=False, digraph=False, weight=weight)
        # then
        self.assertFalse(edge.directed)
        self.assertFalse(edge.digraph)
        self.assertEqual(edge.weight, weight)
        self.assertEqual(edge.label, label)

    def test_equal_undirected_should_not_equal(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        vertex3 = factory.generate_test_vertex('3')
        edge1 = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
        edge2 = Edge(vertex1, vertex3, directed=False, digraph=False, weight=None)
        # when
        result = edge1 == edge2
        # then
        self.assertFalse(result)

    def test_equal_undirected_should_equal(self):
        # given
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        edge1 = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
        edge2 = Edge(vertex2, vertex1, directed=False, digraph=False, weight=None)
        # when
        result = edge1 == edge2
        # then
        self.assertTrue(result)

    def test_equal_directed_should_not_equal(self):
        vertex1 = factory.generate_test_vertex('1')
        vertex2 = factory.generate_test_vertex('2')
        edge1 = Edge(vertex1, vertex2, directed=True, digraph=False, weight=None)
        edge2 = Edge(vertex2, vertex1, directed=True, digraph=False, weight=None)
        # when
        result = edge1 == edge2
        # then
        self.assertFalse(result)
