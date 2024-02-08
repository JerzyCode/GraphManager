from unittest import TestCase

from src.main.app.app import App
from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.edge import Edge
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.graph.vertex import Vertex


class TestCanvasHandler(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = App()

    @classmethod
    def tearDownClass(cls):
        cls.app.destroy()

    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):
        self._start_app()
        self.app.add_graph_button.invoke()
        self.graph_window = self.app.add_graph_window

    def tearDown(self):
        self.app.clear_button.invoke()
        self.app.quit()

    def test_create_graph_undirected(self):
        is_weighted = True
        is_directed = False
        is_digraph = False
        self._create_graph(is_weighted, is_directed, is_digraph)
        graph = self.app.graph
        self._assertions_create_graph(graph, is_weighted, is_directed, is_digraph)

    def test_create_graph_directed(self):
        is_weighted = False
        is_directed = True
        is_digraph = False
        self._create_graph(is_weighted, is_directed, is_digraph)
        graph = self.app.graph
        self._assertions_create_graph(graph, is_weighted, is_directed, is_digraph)

    def test_create_graph_digraph(self):
        is_weighted = False
        is_directed = False
        is_digraph = True
        self._create_graph(is_weighted, is_directed, is_digraph)
        graph = self.app.graph
        self._assertions_create_graph(graph, is_weighted, is_directed, is_digraph)

    def test_add_vertex_to_existing(self):
        self._create_graph(is_weighted=False, is_directed=False, is_digraph=False)
        self.app.canvas_handler._on_shift_button_1(Event(120, 120))
        self._prepare_canvas_handler_adding_vertexes(False, False, False)
        edge = next(iter(self.app.graph.E), None)
        self._assertions_canvas_handler_adding_vertexes(edge)
        self.assertEqual(edge.label, '1_2')
        self.assertEqual(len(self.app.graph.V), 3)

    # w przyszloci zamienic wywolywanie na metodach prywatnych
    def test_canvas_handler_undirected_graph_adding_vertexes(self):
        self._prepare_canvas_handler_adding_vertexes(is_weighted=True, is_directed=False, is_digraph=False)
        edge = next(iter(self.app.graph.E), None)
        self._assertions_canvas_handler_adding_vertexes(edge)

    def test_canvas_handler_directed_graph_adding_vertexes(self):
        self._prepare_canvas_handler_adding_vertexes(is_weighted=False, is_directed=True, is_digraph=False)
        edge = next(iter(self.app.graph.E), None)
        self._assertions_canvas_handler_adding_vertexes(edge)

    def test_canvas_handler_digraph_graph_adding_vertexes(self):
        self._prepare_canvas_handler_adding_vertexes(is_weighted=True, is_directed=False, is_digraph=True)
        edge = next(iter(self.app.graph.E), None)
        self._assertions_canvas_handler_adding_vertexes(edge)

    def test_canvas_handler_deleting_vertexes(self):
        # given
        self._create_graph(False, False, False)
        vertex1 = Vertex('1', 122, 122)
        vertex2 = Vertex('2', 155, 155)
        edge = Edge(vertex1, vertex2, False, False, None)
        self.app.graph.add_vertex(vertex1)
        self.app.graph.add_vertex(vertex2)
        self.app.graph.add_edge(vertex1, vertex2, is_directed=edge.directed, is_digraph=edge.digraph)

        # when
        # tutaj sie nie zamyka ten popup, i bug jest przez to, zatzrymuje test
        # self.app.canvas_handler._on_vertex_right_click(Event(vertex1.x, vertex1.y), vertex1)
        self.app.canvas_handler.vertex_to_delete = vertex1
        self.app.canvas_handler._on_delete_vertex()

        # then
        self.assertTrue(edge not in self.app.graph.E)
        self.assertTrue(vertex1 not in vertex2.neighbors)
        self.assertTrue(vertex2 not in vertex1.neighbors)
        self.assertTrue(edge not in vertex1.edges)
        self.assertTrue(edge not in vertex2.edges)

    def _set_add_graph_params(self, is_weighted, is_directed, is_digraph):
        self.graph_window.is_weighted = is_weighted
        self.graph_window.is_directed = is_directed
        self.graph_window.is_digraph = is_digraph

    def _create_graph(self, is_weighted, is_directed, is_digraph):
        self._set_add_graph_params(is_weighted, is_directed, is_digraph)
        self.graph_window.set_params_button.invoke()

    def _assertions_create_graph(self, graph, is_weighted, is_directed, is_digraph):
        self.assertIsNotNone(graph)
        self.assertEqual(len(graph.V), 0)
        self.assertEqual(len(graph.E), 0)

        if is_weighted:
            self.assertTrue(graph.is_weighted)
        else:
            self.assertFalse(graph.is_weighted)

        if is_directed or is_digraph:
            self.assertTrue(isinstance(graph, DirectedGraph))
        else:
            self.assertFalse(isinstance(graph, DirectedGraph))

        if is_digraph:
            self.assertTrue(isinstance(graph, Digraph))
            self.assertTrue(isinstance(graph, DirectedGraph))
        else:
            self.assertFalse(isinstance(graph, Digraph))

        if not is_directed and not is_digraph:
            self.assertTrue(isinstance(graph, UndirectedGraph))

    def _prepare_canvas_handler_adding_vertexes(self, is_weighted, is_directed, is_digraph):
        self._create_graph(is_weighted=is_weighted, is_directed=is_directed, is_digraph=is_digraph)
        self.app.canvas_handler._on_shift_button_1(Event(55, 55))
        self.app.canvas_handler._on_shift_button_1(Event(50, 50))
        vertex1 = self.app.graph.V[0]
        vertex2 = self.app.graph.V[1]
        self.app.canvas_handler._on_vertex_click(Event(vertex1.x, vertex1.y), vertex1)
        self.app.canvas_handler._on_vertex_click(Event(vertex2.x, vertex2.y), vertex2)

    def _assertions_canvas_handler_adding_vertexes(self, edge):
        graph = self.app.graph
        vertex1 = self.app.graph.V[0]
        vertex2 = self.app.graph.V[1]
        self.assertIsNotNone(edge)
        self.assertEqual(len(self.app.graph.E), 1)
        # self.assertEqual(graph.is_weighted, edge.weight is not None)
        self.assertEqual(isinstance(graph, DirectedGraph), edge.directed)
        self.assertEqual(isinstance(graph, Digraph), edge.digraph)
        self.assertEqual(edge.vertex1, vertex1)
        self.assertEqual(edge.vertex2, vertex2)


class Event:
    def __init__(self, x, y):
        self.x = x
        self.y = y
