import tkinter
import unittest
from unittest.mock import Mock

import src.main.app.graph.algorithms.algorithms as sut
import tests.main.app.graph.graph_factory as factory
from src.main.app.ui.drawing.drawer import Drawer
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.ui.drawing.vertex_drawer import VertexDrawer


class TestKruskal(unittest.TestCase):
    def setUp(self):
        self.canvas_mock = Mock(spec=tkinter.Canvas)
        self.edge_drawer_mock = EdgeDrawer(self.canvas_mock)
        self.vertex_drawer_mock = VertexDrawer(self.canvas_mock)
        self.drawer_mock = Mock(spec=Drawer(self.canvas_mock, edge_drawer=self, vertex_drawer=self))

    def test_kruskal_empty_graph(self):
        # given
        graph = factory.generate_test_empty_graph_weighted()
        # when
        result = sut.kruskal_algorithm(graph, self.drawer_mock)
        # then
        num_of_colored_vertexes = [call for call in self.drawer_mock.highlight_vertex_delay.call_args_list if
                                   call[0][0] is not None]
        self.assertEqual(0, len(result))
        self.assertEqual(len(num_of_colored_vertexes), len(graph.V))

    def test_kruskal_no_weighted(self):
        # given
        graph = factory.generate_test_undirected_graph()
        # when
        result = sut.kruskal_algorithm(graph, self.drawer_mock)
        # then
        self.assertIsNone(result)

    def test_kruskal(self):
        # given
        graph = factory.generate_test_weighted_undirected_graph()
        # when
        result = sut.kruskal_algorithm(graph, self.drawer_mock)
        # then
        num_of_colored_kruskal = self.drawer_mock.highlight_edge_kruskal.call_count
        labels = {edge.label for edge in result}
        self.assertEqual(num_of_colored_kruskal, len(result))
        self.assertEqual(set(labels), {'1_2', '1_5', '2_6', '2_7', '2_4', '3_7', '4_8'})
        # in future check if tree connected and if there is a cycle

    # TEST UNCONNECTED GRAPH