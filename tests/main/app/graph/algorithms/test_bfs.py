import tkinter
import unittest
from unittest.mock import Mock

import src.main.app.graph.algorithms.algorithms as sut
import tests.main.app.graph.graph_factory as factory
from src.main.app.ui.drawing.drawer import Drawer
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.ui.drawing.vertex_drawer import VertexDrawer


class TestBfs(unittest.TestCase):
    def setUp(self):
        self.canvas_mock = Mock(spec=tkinter.Canvas)
        self.edge_drawer_mock = EdgeDrawer(self.canvas_mock)
        self.vertex_drawer_mock = VertexDrawer(self.canvas_mock)
        self.drawer_mock = Mock(spec=Drawer(self.canvas_mock, edge_drawer=self, vertex_drawer=self))

    def test_bfs_empty_graph(self):
        # given
        graph = factory.generate_test_empty_graph()
        # when
        result = sut.binary_search(graph, self.drawer_mock)
        # then
        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        self.assertEqual(0, len(result))
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))

    def test_bfs_undirected_ten_vertexes_connected(self):
        # given
        graph = factory.generate_test_undirected_graph_bfs()
        # when
        result = sut.binary_search(graph, self.drawer_mock)
        # then
        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        res_set = [vertex.label for vertex in result]
        self.assertEqual(len(graph.V), len(result))
        self.assertEqual(result[0].label, '1')
        self.assertEqual(set(res_set[1:5]), {'5', '7', '8', '4'})
        self.assertEqual(set(res_set[5:10]), {'3', '10', '2', '6', '9'})
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))

    def test_bfs_directed_ten_vertexes_connected(self):
        # given
        graph = factory.generate_test_directed_graph_bfs()
        # when
        result = sut.binary_search(graph, self.drawer_mock)
        # then
        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        res_set = [vertex.label for vertex in result]
        self.assertEqual(len(graph.V), len(result))
        self.assertEqual(result[0].label, '1')
        self.assertEqual(set(res_set[1:3]), {'2', '3'})
        self.assertEqual(set(res_set[3:7]), {'4', '5', '6', '7'})
        self.assertEqual(set(res_set[7:10]), {'8', '9', '10'})
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))

    def test_bfs_no_connected(self):
        # given
        graph = factory.generate_test_no_connected_graph_bfs()
        # when
        result = sut.binary_search(graph, self.drawer_mock)
        # then
        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        res_set = [vertex.label for vertex in result]
        self.assertEqual(len(graph.V), len(result))
        self.assertEqual(result[0].label, '1')
        self.assertEqual(set(res_set[1:3]), {'3', '2'})
        self.assertEqual(set(res_set[3]), {'5'})
        self.assertEqual(set(res_set[4]), {'4'})
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))
