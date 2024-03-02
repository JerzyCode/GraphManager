import tkinter
from unittest import TestCase
from unittest.mock import Mock

import src.main.app.graph.algorithms.algorithms as sut
import tests.main.app.graph.graph_factory as factory
from src.main.app.ui.drawing.drawer import Drawer
from src.main.app.ui.drawing.edge_drawer import EdgeDrawer
from src.main.app.ui.drawing.vertex_drawer import VertexDrawer


class TestDijkstra(TestCase):

    def setUp(self):
        self.canvas_mock = Mock(spec=tkinter.Canvas)
        self.edge_drawer_mock = EdgeDrawer(self.canvas_mock)
        self.vertex_drawer_mock = VertexDrawer(self.canvas_mock)
        self.drawer_mock = Mock(spec=Drawer(self.canvas_mock, edge_drawer=self, vertex_drawer=self))

    def test_dijkstra_empty_graph(self):
        # given
        graph = factory.generate_test_empty_graph_weighted()
        # when
        result = sut.dijkstra_algorithm(graph, None, self.drawer_mock)
        # then
        colored_vertexes = self.drawer_mock.highlight_vertex_delay.call_count
        draw_distances = self.drawer_mock.draw_dijkstra_distance.call_count
        colored_edges = self.drawer_mock.highlight_edge_delay.call_count
        refreshed_edges = self.drawer_mock.refresh_edge_delay.call_count
        self.assertEqual(0, colored_vertexes)
        self.assertEqual(0, draw_distances)
        self.assertEqual(0, colored_edges)
        self.assertEqual(0, refreshed_edges)

    def test_dijkstra_no_weighted_graph(self):
        # given
        graph = factory.generate_test_undirected_graph()
        # when
        result = sut.dijkstra_algorithm(graph, None, self.drawer_mock)
        # then
        colored_vertexes = self.drawer_mock.highlight_vertex_delay.call_count
        draw_distances = self.drawer_mock.draw_dijkstra_distance.call_count
        colored_edges = self.drawer_mock.highlight_edge_delay.call_count
        refreshed_edges = self.drawer_mock.refresh_edge_delay.call_count
        self.assertIsNone(result)
        self.assertEqual(0, colored_vertexes)
        self.assertEqual(0, draw_distances)
        self.assertEqual(0, colored_edges)
        self.assertEqual(0, refreshed_edges)

    def test_dijkstra_negative_weight_graph(self):
        # given
        graph = factory.generate_test_graph_negative_weight()
        # when
        result = sut.dijkstra_algorithm(graph, None, self.drawer_mock)
        # then
        colored_vertexes = self.drawer_mock.highlight_vertex_delay.call_count
        draw_distances = self.drawer_mock.draw_dijkstra_distance.call_count
        colored_edges = self.drawer_mock.highlight_edge_delay.call_count
        refreshed_edges = self.drawer_mock.refresh_edge_delay.call_count
        self.assertIsNone(result)
        self.assertEqual(0, colored_vertexes)
        self.assertEqual(0, draw_distances)
        self.assertEqual(0, colored_edges)
        self.assertEqual(0, refreshed_edges)

    def test_dijkstra_undirected_graph(self):
        # given
        graph = factory.generate_test_weighted_undirected_graph()
        vertexes = graph.V
        # when
        result = sut.dijkstra_algorithm(graph, vertexes[0], self.drawer_mock)
        paths = result['paths']
        distances = result['weights']
        print(paths)
        # then
        colored_vertexes = self.drawer_mock.highlight_vertex_delay.call_count
        draw_distances = self.drawer_mock.draw_dijkstra_distance.call_count
        colored_edges = self.drawer_mock.highlight_edge_delay.call_count
        refreshed_edges = self.drawer_mock.refresh_edge_delay.call_count
        self.assertIsNotNone(result)
        self.assertEqual(8, colored_vertexes)
        self.assertEqual(24, draw_distances)
        self.assertEqual(8, colored_edges)
        self.assertEqual(1, refreshed_edges)
        self.assertEqual(0, distances[vertexes[0]])
        self.assert_vertex(False, vertexes[1], paths, distances[vertexes[1]], 2, vertexes[0])
        self.assert_vertex(False, vertexes[2], paths, distances[vertexes[2]], 6, vertexes[0])
        self.assert_vertex(False, vertexes[3], paths, distances[vertexes[3]], 3, vertexes[1])
        self.assert_vertex(False, vertexes[4], paths, distances[vertexes[4]], 32, vertexes[0])
        self.assert_vertex(False, vertexes[5], paths, distances[vertexes[5]], 6, vertexes[1])
        self.assert_vertex(False, vertexes[6], paths, distances[vertexes[6]], 5, vertexes[1])
        self.assert_vertex(False, vertexes[7], paths, distances[vertexes[7]], 8, vertexes[3])

    def test_dijkstra_directed_graph(self):
        # given
        graph = factory.generate_test_weighted_directed_graph()
        vertexes = graph.V
        # when
        result = sut.dijkstra_algorithm(graph, vertexes[0], self.drawer_mock)
        paths = result['paths']
        distances = result['weights']
        print(paths)
        # then
        colored_vertexes = self.drawer_mock.highlight_vertex_delay.call_count
        draw_distances = self.drawer_mock.draw_dijkstra_distance.call_count
        colored_edges = self.drawer_mock.highlight_edge_delay.call_count
        refreshed_edges = self.drawer_mock.refresh_edge_delay.call_count
        self.assertIsNotNone(result)
        self.assertEqual(8, colored_vertexes)
        self.assertEqual(24, draw_distances)
        self.assertEqual(8, colored_edges)
        self.assertEqual(1, refreshed_edges)
        self.assertEqual(0, distances[vertexes[0]])
        self.assert_vertex(True, vertexes[1], paths, distances[vertexes[1]], 2, vertexes[0])
        self.assert_vertex(True, vertexes[2], paths, distances[vertexes[2]], 6, vertexes[0])
        self.assert_vertex(True, vertexes[3], paths, distances[vertexes[3]], 3, vertexes[1])
        self.assert_vertex(True, vertexes[4], paths, distances[vertexes[4]], 32, vertexes[0])
        self.assert_vertex(True, vertexes[5], paths, distances[vertexes[5]], 6, vertexes[1])
        self.assert_vertex(True, vertexes[6], paths, distances[vertexes[6]], 5, vertexes[1])
        self.assert_vertex(True, vertexes[7], paths, distances[vertexes[7]], 8, vertexes[3])

    def assert_vertex(self, directed, vertex, paths, distance, expected_distance, expected_previous):
        self.assertEqual(paths[vertex], expected_previous.find_edge(vertex, directed))
        self.assertEqual(int(distance), expected_distance)
