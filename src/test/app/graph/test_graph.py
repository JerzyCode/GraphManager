import unittest

from src.main.app.graph.graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        matrix = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]
        self.graph = Graph(matrix, is_weighted=False, max_width=123, max_height=123)

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
