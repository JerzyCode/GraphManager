import tkinter
import unittest
from unittest.mock import Mock

import src.main.app.graph.algorithms.algorithms as alg
from src.main.app.ui.drawing.drawer import Drawer
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.ui.drawing.vertex_drawer import VertexDrawer


class TestBfs(unittest.TestCase):
    def setUp(self):
        self.canvas_mock = Mock(spec=tkinter.Canvas)
        self.edge_drawer_mock = EdgeDrawer(self.canvas_mock)
        self.vertex_drawer_mock = VertexDrawer(self.canvas_mock)
        self.drawer_mock = Mock(spec=Drawer(self.canvas_mock, edge_drawer=self, vertex_drawer=self))

    def test_bfs_undirected(self):
        graph_matrix = [
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
            [1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            [1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 0, 1, 0, 1, 0]
        ]
        graph = UndirectedGraph(graph_matrix, is_weighted=False, max_width=12, max_height=12)
        self.assert_equal_graph(graph)

    def test_bfs_directed(self):
        graph_matrix = [
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 1, 0, 1, 0, 0, 1, 0, 1, 0]
        ]
        graph = DirectedGraph(graph_matrix, is_weighted=False, max_width=12, max_height=12)
        self.assert_equal_graph(graph)

    def assert_equal_graph(self, graph):
        res = alg.binary_search(graph, self.drawer_mock)
        res_set = [vertex.label for vertex in res]

        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        self.assertEqual(res[0].label, '1')
        self.assertEqual(set(res_set[1:5]), {'5', '7', '8', '10'})
        self.assertEqual(set(res_set[5:10]), {'2', '3', '4', '6', '9'})
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))