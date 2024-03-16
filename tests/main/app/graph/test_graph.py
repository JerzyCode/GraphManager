import random as rd
import unittest

import src.main.app.graph.digraph as digraph
import src.main.app.graph.directed_graph as directed_graph
import src.main.app.graph.undirected_graph as undirected_graph
import tests.main.app.graph.graph_factory as factory


class TestGraph(unittest.TestCase):

    def test_add_vertex_graph(self):
        # given
        graph = factory.generate_test_empty_graph()
        vertex = factory.generate_test_vertex('1')
        # when
        graph.add_vertex(vertex)
        # then
        self.assertEqual(len(graph.V), 1)
        self.assertEqual(graph.V[0], vertex)

    def test_delete_vertex_graph(self):
        # given
        graph = factory.generate_test_two_vertex_graph()
        vertex1 = graph.V[0]
        vertex2 = graph.V[1]
        # when
        graph.delete_vertex(vertex1)
        # then
        self.assertEqual(len(graph.V), 1)
        self.assertEqual(len(graph.E), 0)
        self.assertNotIn(vertex1, vertex2.neighbors)
        self.assertNotIn(vertex2, vertex1.neighbors)
        self.assertEqual(len(vertex1.edges), 0)
        self.assertEqual(len(vertex2.edges), 0)

    def test_delete_edge_graph(self):
        # given
        graph = factory.generate_test_two_vertex_graph()
        vertex1 = graph.V[0]
        vertex2 = graph.V[1]
        edge_to_delete = list(graph.E)[0]
        # when
        graph.delete_edge(edge_to_delete)
        # then
        self.assertEqual(len(graph.V), 2)
        self.assertEqual(len(graph.E), 0)
        self.assertNotIn(vertex1, vertex2.neighbors)
        self.assertNotIn(vertex2, vertex1.neighbors)
        self.assertEqual(len(vertex1.edges), 0)
        self.assertEqual(len(vertex2.edges), 0)

    def test_add_edge_undirected_graph(self):
        # given
        graph = factory.generate_test_two_vertex_graph()
        vertex1 = graph.V[0]
        vertex3 = factory.generate_test_vertex('3')
        graph.V.append(vertex3)
        # when
        added_edge = graph.add_edge(vertex1, vertex3, is_directed=isinstance(graph, directed_graph.DirectedGraph), is_digraph=False, weight=None)
        # then
        self.assertEqual(len(graph.E), 2)
        self.assertEqual(added_edge.vertex1, vertex1)
        self.assertEqual(added_edge.vertex2, vertex3)
        self.assertFalse(added_edge.directed)
        self.assertIsNone(added_edge.weight)
        self.assertIn(vertex1, vertex3.neighbors)
        self.assertIn(vertex3, vertex1.neighbors)
        self.assertIn(added_edge, vertex1.edges)
        self.assertIn(added_edge, vertex3.edges)

    def test_add_edge_directed_graph(self):
        # given
        graph = factory.generate_test_two_vertex_directed_graph()
        vertex1 = graph.V[0]
        vertex3 = factory.generate_test_vertex('3')
        graph.V.append(vertex3)
        # when
        added_edge = graph.add_edge(vertex1, vertex3, is_directed=isinstance(graph, directed_graph.DirectedGraph), is_digraph=False, weight=5)
        # then
        self.assertEqual(len(graph.E), 2)
        self.assertEqual(added_edge.vertex1, vertex1)
        self.assertEqual(added_edge.vertex2, vertex3)
        self.assertTrue(added_edge.directed)
        self.assertIsNotNone(added_edge.weight)
        self.assertIn(vertex3, vertex1.neighbors)
        self.assertNotIn(vertex1, vertex3.neighbors)
        self.assertIn(added_edge, vertex1.edges)
        self.assertNotIn(added_edge, vertex3.edges)

    def test_generate_undirected_graph(self):
        # given
        probability = 0.5
        number_of_vertex = rd.randint(0, 100)
        max_width = rd.randint(100, 500)
        max_height = rd.randint(100, 500)
        is_weighted = True
        # when
        graph = undirected_graph.generate_graph(number_of_vertex, probability, max_width, max_height, is_weighted)
        # then
        self.assertTrue(graph.is_weighted)
        self.assertEqual(len(graph.V), number_of_vertex)
        self.assertNotIsInstance(graph, directed_graph.DirectedGraph)
        self.assertNotIsInstance(graph, digraph.Digraph)
        self.assertIsInstance(graph, undirected_graph.UndirectedGraph)
        self.assertIsNotNone(graph.E)
        for edge in graph.E:
            self.assertIsNotNone(edge.weight)
            self.assertFalse(edge.directed)

    def test_generate_directed_graph(self):
        # given
        probability = 0.5
        number_of_vertex = rd.randint(0, 100)
        max_width = rd.randint(100, 500)
        max_height = rd.randint(100, 500)
        is_weighted = True
        # when
        graph = directed_graph.generate_graph(number_of_vertex, probability, max_width, max_height, is_weighted)
        # then
        self.assertTrue(graph.is_weighted)
        self.assertEqual(len(graph.V), number_of_vertex)
        self.assertIsInstance(graph, directed_graph.DirectedGraph)
        self.assertNotIsInstance(graph, digraph.Digraph)
        self.assertNotIsInstance(graph, undirected_graph.UndirectedGraph)
        self.assertIsNotNone(graph.E)
        for edge in graph.E:
            self.assertIsNotNone(edge.weight)
            self.assertTrue(edge.directed)

    def test_generate_digraph_graph(self):
        # given
        probability = 0.5
        number_of_vertex = rd.randint(0, 100)
        max_width = rd.randint(100, 500)
        max_height = rd.randint(100, 500)
        is_weighted = True
        # when
        graph = digraph.generate_graph(number_of_vertex, probability, max_width, max_height, is_weighted)
        # then
        self.assertTrue(graph.is_weighted)
        self.assertEqual(len(graph.V), number_of_vertex)
        self.assertIsInstance(graph, directed_graph.DirectedGraph)
        self.assertIsInstance(graph, digraph.Digraph)
        self.assertNotIsInstance(graph, undirected_graph.UndirectedGraph)
        self.assertIsNotNone(graph.E)
        for edge in graph.E:
            self.assertIsNotNone(edge.weight)
            self.assertTrue(edge.directed)
