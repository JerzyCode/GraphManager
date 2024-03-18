import tkinter
from unittest import TestCase
from unittest.mock import Mock

import tests.main.app.graph.graph_factory as factory
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.utils.config import Config
from src.main.app.utils.constants import EDGE_COLOR_DARK


class TestEdgeDrawer(TestCase):
    def setUp(self):
        self.canvas_mock = Mock(spec=tkinter.Canvas)
        self.config_mock = Mock(spec=Config)
        self.config_mock.edge_width = 1.25
        self.config_mock.edge_color = EDGE_COLOR_DARK

        self.config_mock.vertex_radius = 14
        self.sut = EdgeDrawer(self.canvas_mock, self.config_mock)

    def test_draw_edge_digraph(self):
        # given
        graph = factory.generate_test_two_vertex_digraph()
        edge = list(graph.E)[0]
        # when
        self.sut.draw_edge(edge, graph)
        # then
        self.assertEqual(1, self.canvas_mock.create_line.call_count)
        self.assertEqual(1, self.canvas_mock.itemconfig.call_count)

    def test_draw_edge_directed(self):
        # given
        graph = factory.generate_test_directed_graph()
        edge = list(graph.E)[0]
        # when
        self.sut.draw_edge(edge, graph)
        # then
        self.assertEqual(1, self.canvas_mock.create_line.call_count)
        self.assertEqual(1, self.canvas_mock.itemconfig.call_count)

    def test_draw_edge_undirected(self):
        # given
        graph = factory.generate_test_two_vertex_graph()
        edge = list(graph.E)[0]
        # when
        self.sut.draw_edge(edge, graph)
        # then
        self.assertEqual(1, self.canvas_mock.create_line.call_count)
        self.assertEqual(0, self.canvas_mock.itemconfig.call_count)

    # to add more test methods
