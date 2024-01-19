import unittest

from src.main.app.graph.directed_graph import DirectedGraph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        self.matrix = [[0, 1, 1, 1],
                       [0, 0, 1, 1],
                       [1, 0, 0, 1],
                       [1, 1, 0, 0]]
        self.max_height = 100
        self.max_width = 100

    def test___init___no_weights(self):
        is_weighted = False
        graph = DirectedGraph(self.matrix, is_weighted,
                              self.max_width, self.max_height)
        edges = graph.E
        vertexes = graph.V
        self.assertEqual(len(vertexes), 4)
        self.assertEqual(len(edges), 9)
        self.assertEqual(len(vertexes[0].neighbors), 3)
        self.assertEqual(len(vertexes[1].neighbors), 2)
        self.assertEqual(len(vertexes[2].neighbors), 2)
        self.assertEqual(len(vertexes[3].neighbors), 2)
        for edge in edges:
            self.assertTrue(edge.directed)
        for edge in edges:
            self.assertIsNone(edge.weight)

    def test___init___with_weights(self):
        is_weighted = True
        graph = DirectedGraph(self.matrix, is_weighted,
                              self.max_width, self.max_height)
        edges = graph.E
        vertexes = graph.V
        self.assertEqual(len(vertexes), 4)
        self.assertEqual(len(edges), 9)
        self.assertEqual(len(vertexes[0].neighbors), 3)
        self.assertEqual(len(vertexes[1].neighbors), 2)
        self.assertEqual(len(vertexes[2].neighbors), 2)
        self.assertEqual(len(vertexes[3].neighbors), 2)

        for edge in edges:
            self.assertTrue(edge.directed)
        for edge in edges:
            self.assertIsNotNone(edge.weight)
