import tkinter as tk

from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.graph.vertex import Vertex
from src.main.app.ui.windows.set_weight_window import AskWeightDialog
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("CanvasHandler")


class CanvasHandler:
    def __init__(self, root, is_directed=False, is_digraph=False, is_weighted=False, graph=None):
        self.canvas = root.canvas
        self.drawer = root.drawer
        self.vertex_to_delete = None
        self.root = root
        self.is_directed = is_directed
        self.is_weighted = is_weighted
        self.is_digraph = is_digraph
        self.enabled = True
        self._create_graph(graph)
        self.selected_vertexes = []
        self.canvas.bind("<Shift-Button-1>", self._on_shift_button_1)
        self._create_popup_menu()

    def _create_graph(self, graph):
        if graph is not None:
            for vertex in graph.V:
                self.graph = graph
                self._bind_vertex(vertex)
        else:
            if self.is_digraph:
                self.graph = Digraph([], self.is_weighted)
            elif self.is_directed:
                self.graph = DirectedGraph([], self.is_weighted)
            else:
                self.graph = UndirectedGraph([], self.is_weighted)
        self.prev_label = str(len(self.graph.V) + 1)

    def _create_popup_menu(self):
        self.pop_up = tk.Menu(self.root, tearoff=0)
        self.pop_up.add_command(label='Delete Vertex', command=self._on_delete_vertex)

    def _on_shift_button_1(self, event):
        self._add_vertex(event)

    def unbind(self):
        self.canvas.unbind("<Shift-Button-1>")

    def _on_add_edge(self):
        self.enabled_vertex_select = True

    def _add_vertex(self, event):
        if len(self.graph.V) < 50:
            vertex = Vertex(self.prev_label, self.canvas.winfo_width(), self.canvas.winfo_height(), event.x,
                            event.y)
            self.graph.add_vertex(vertex)
            self.drawer.vertex_drawer.draw_vertex(vertex)
            self._bind_vertex(vertex)
            self.prev_label = str(int(self.prev_label) + 1)

    def _bind_vertex(self, vertex):
        self.canvas.tag_bind(f"text_{vertex.label}", "<Alt-ButtonPress-1>", lambda e, v=vertex: self._on_vertex_click(e, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<Alt-ButtonPress-1>", lambda e, v=vertex: self._on_vertex_click(e, v))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-3>", lambda e, v=vertex: self._on_vertex_right_click(e, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-3>", lambda e, v=vertex: self._on_vertex_right_click(e, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move_vertex(event))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<B1-Motion>", lambda event, v=vertex: self._move_vertex(event, v))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move_vertex(event))
        self.canvas.tag_bind(f"text_{vertex.label}", "<B1-Motion>", lambda event, v=vertex: self._move_vertex(event, v))

    def _on_vertex_click(self, event, vertex):
        if (vertex.x - RADIUS < event.x < vertex.x + RADIUS and vertex.y - RADIUS < event.y < vertex.y + RADIUS
                and len(self.selected_vertexes) < 2 and vertex not in self.selected_vertexes):
            self.selected_vertexes.append(vertex)
            self.drawer.vertex_drawer.highlight_vertex_color(vertex)
        if len(self.selected_vertexes) == 2 and self.selected_vertexes[0] != self.selected_vertexes[1]:
            weight = None
            if self.is_weighted:
                weight = self._ask_weight()
                if weight >= 1000:
                    weight = 999
            edge = self.graph.add_edge(self.selected_vertexes[0], self.selected_vertexes[1], self.is_directed, self.is_digraph, weight)
            self.drawer.vertex_drawer.refresh_vertex_color(self.selected_vertexes[0])
            self.drawer.vertex_drawer.refresh_vertex_color(self.selected_vertexes[1])
            self.drawer.edge_drawer.draw_edge(edge, self.graph)
            self.selected_vertexes = []

    def _on_vertex_right_click(self, event, vertex):
        if vertex.x - RADIUS < event.x < vertex.x + RADIUS and vertex.y - RADIUS < event.y < vertex.y + RADIUS:
            self.vertex_to_delete = vertex
            x = self.canvas.winfo_rootx() + vertex.x - 110
            y = self.canvas.winfo_rooty() + vertex.y
            self.pop_up.tk_popup(x, y, 0)

    def _on_delete_vertex(self):
        self.drawer.erase_vertex_and_incidental_edges(self.vertex_to_delete)
        self.graph.delete_vertex(self.vertex_to_delete)
        self.vertex_to_delete = None

    def _start_move_vertex(self, event):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return

    def _move_vertex(self, event, vertex):
        delta_x = event.x - vertex.x
        delta_y = event.y - vertex.y
        vertex.x = event.x
        vertex.y = event.y
        self.canvas.move(f"vertex_{vertex.label}", delta_x, delta_y)
        self.canvas.move(f"text_{vertex.label}", delta_x, delta_y)
        self.drawer.edge_drawer.move_edge_incidental(vertex, self.graph)
        self.drawer.vertex_drawer.raise_all_vertexes(self.graph.V)

    def _ask_weight(self):
        dialog = AskWeightDialog(self.root)
        return dialog.weight