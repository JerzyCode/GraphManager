import tkinter as tk

from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.graph.vertex import Vertex
from src.main.app.ui.windows.set_weight_window import AskWeightDialog
from src.main.app.utils.constants import RADIUS
from src.main.app.utils.logger import setup_logger

logger = setup_logger("CanvasHandler")

BUTTON_PRESS_1 = "<ButtonPress-1>"
BUTTON_1_MOTION = "<B1-Motion>"
BUTTON_PRESS_3 = "<ButtonPress-3>"
ALT_BUTTON_PRESS_1 = "<Alt-ButtonPress-1>"
ENTER = "<Enter>"
LEAVE = "<Leave>"


def attract(event_x, event_y):
    delta_x = None
    delta_y = None
    potential_x = int(event_x / 50)
    potential_y = int(event_y / 50)
    if potential_x - potential_x * 50 <= 25:
        delta_x = event_x - potential_x * 50
    if potential_y - potential_y * 50 <= 25:
        delta_y = event_y - potential_y * 50
    return delta_x, delta_y


class CanvasHandler:
    def __init__(self, root, is_directed=False, is_digraph=False, is_weighted=False, graph=None):
        self.graph = None
        self.canvas = root.canvas
        self.drawer = root.drawer
        self.config = root.config
        self.vertex_to_delete = None
        self.edge_to_delete = None
        self.root = root
        self.is_directed = is_directed
        self.is_weighted = is_weighted
        self.is_digraph = is_digraph
        self.enabled = True
        self._create_graph(graph)
        self.selected_vertexes = []
        self.canvas.bind("<Shift-Button-1>", self._on_shift_button_1)
        self._create_vertex_popup_menu()
        self._create_edge_popup_menu()

    def set_graph(self, graph):
        if graph is None:
            return
        self.graph = graph
        for vertex in self.graph.V:
            self._bind_vertex(vertex)
        for edge in self.graph.E:
            self._bind_edge(edge)

    def _create_graph(self, graph):
        if graph is not None:
            self.graph = graph
            for vertex in graph.V:
                self._bind_vertex(vertex)
            for edge in graph.E:
                self._bind_edge(edge)
        else:
            if self.is_digraph:
                self.graph = Digraph([], self.is_weighted)
            elif self.is_directed:
                self.graph = DirectedGraph([], self.is_weighted)
            else:
                self.graph = UndirectedGraph([], self.is_weighted)
        self.prev_label = str(len(self.graph.V) + 1)

    def _create_vertex_popup_menu(self):
        self.vertex_pop_up = tk.Menu(self.root, tearoff=0)
        self.vertex_pop_up.add_command(label='Delete Vertex', command=self._on_delete_vertex)

    def _create_edge_popup_menu(self):
        self.edge_pop_up = tk.Menu(self.root, tearoff=0)
        self.edge_pop_up.add_command(label='Delete Edge', command=self._on_delete_edge)

    def _on_shift_button_1(self, event):
        self._add_vertex(event)

    def unbind(self):
        self.canvas.unbind("<Shift-Button-1>")

    def _on_add_edge(self):
        self.enabled_vertex_select = True

    def _add_vertex(self, event):
        logger.debug("Add Vertex")
        if len(self.graph.V) < 50:
            vertex = Vertex(self.prev_label, self.canvas.winfo_width(), self.canvas.winfo_height(), event.x,
                            event.y)
            self.graph.add_vertex(vertex)
            self.drawer.vertex_drawer.draw_vertex(vertex)
            self._bind_vertex(vertex)
            self.prev_label = str(int(self.prev_label) + 1)

    def _bind_vertex(self, vertex):
        self.canvas.tag_bind(f"text_{vertex.label}", ALT_BUTTON_PRESS_1, lambda event, v=vertex: self._on_vertex_click(event, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", ALT_BUTTON_PRESS_1, lambda event, v=vertex: self._on_vertex_click(event, v))
        self.canvas.tag_bind(f"text_{vertex.label}", BUTTON_PRESS_3, lambda event, v=vertex: self._on_vertex_right_click(event, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", BUTTON_PRESS_3, lambda event, v=vertex: self._on_vertex_right_click(event, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", ENTER, lambda event, v=vertex: self._on_enter_vertex(v))
        self.canvas.tag_bind(f"text_{vertex.label}", ENTER, lambda event, v=vertex: self._on_enter_vertex(v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", LEAVE, lambda event, v=vertex: self._on_leave_vertex(v))
        self.canvas.tag_bind(f"text_{vertex.label}", LEAVE, lambda event, v=vertex: self._on_leave_vertex(v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", BUTTON_PRESS_1, lambda event: self._start_move_vertex(event))
        self.canvas.tag_bind(f"vertex_{vertex.label}", BUTTON_1_MOTION, lambda event, v=vertex: self._move_vertex(event, v))
        self.canvas.tag_bind(f"text_{vertex.label}", BUTTON_PRESS_1, lambda event: self._start_move_vertex(event))
        self.canvas.tag_bind(f"text_{vertex.label}", BUTTON_1_MOTION, lambda event, v=vertex: self._move_vertex(event, v))

    def _bind_edge(self, edge):
        self.canvas.tag_bind(f"edge_{edge.label}", ENTER, lambda event, e=edge: self._on_enter_edge(e))
        self.canvas.tag_bind(f"edge_{edge.label}", LEAVE, lambda event, e=edge: self._on_leave_edge(e))
        self.canvas.tag_bind(f"edge_{edge.label}", BUTTON_PRESS_3, lambda event, e=edge: self._on_edge_right_click(e))

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
            logger.debug("Add Edge")
            edge = self.graph.add_edge(self.selected_vertexes[0], self.selected_vertexes[1], self.is_directed, self.is_digraph, weight)
            self._bind_edge(edge)
            self.drawer.vertex_drawer.refresh_vertex_color(self.selected_vertexes[0])
            self.drawer.vertex_drawer.refresh_vertex_color(self.selected_vertexes[1])
            self.drawer.edge_drawer.draw_edge(edge, self.graph)
            self.selected_vertexes = []

    def _on_edge_right_click(self, edge):
        self.edge_to_delete = edge
        x = self.canvas.winfo_rootx() + 0.5 * (edge.vertex1.x + edge.vertex2.x)
        y = self.canvas.winfo_rooty() + 0.5 * (edge.vertex1.y + edge.vertex2.y)
        self.edge_pop_up.tk_popup(int(x), int(y), 0)

    def _on_delete_edge(self):
        logger.debug(f"Deleting edge: {self.edge_to_delete}")
        self.drawer.edge_drawer.erase_edge(self.edge_to_delete)
        self.graph.delete_edge(self.edge_to_delete)
        self.edge_to_delete = None

    def _on_vertex_right_click(self, event, vertex):
        print('_on_vertex_right_click')
        if vertex.x - RADIUS < event.x < vertex.x + RADIUS and vertex.y - RADIUS < event.y < vertex.y + RADIUS:
            self.vertex_to_delete = vertex
            x = self.canvas.winfo_rootx() + vertex.x - 110
            y = self.canvas.winfo_rooty() + vertex.y
            self.vertex_pop_up.tk_popup(int(x), int(y), 0)

    def _on_delete_vertex(self):
        logger.debug(f"Deleting vertex: {self.vertex_to_delete}")
        self.drawer.erase_vertex_and_incidental_edges(self.vertex_to_delete)
        self.graph.delete_vertex(self.vertex_to_delete)
        self.vertex_to_delete = None

    def _start_move_vertex(self, event):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return

    def _move_vertex(self, event, vertex):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return
        delta_x = 0
        delta_y = 0
        if not self.config.is_grid_enabled:
            delta_x = event.x - vertex.x
            delta_y = event.y - vertex.y
            vertex.x = event.x
            vertex.y = event.y
        else:
            x, y = attract(event.x, event.y)
            if x is not None and y is not None:
                prev_x = vertex.x
                prev_y = vertex.y
                vertex.x = event.x - x
                vertex.y = event.y - y
                delta_x = vertex.x - prev_x
                delta_y = vertex.y - prev_y
        self.canvas.move(f"vertex_{vertex.label}", delta_x, delta_y)
        self.canvas.move(f"text_{vertex.label}", delta_x, delta_y)
        self.canvas.move(f'distance_{vertex.label}', delta_x, delta_y)
        self.drawer.edge_drawer.move_edge_incidental(vertex, self.graph)
        self.drawer.vertex_drawer.raise_all_vertexes(self.graph.V)

    def _ask_weight(self):
        dialog = AskWeightDialog(self.root)
        return dialog.weight

    def _on_enter_vertex(self, vertex):
        self.drawer.vertex_drawer.highlight_vertex_color(vertex)

    def _on_leave_vertex(self, vertex):
        if vertex not in self.selected_vertexes and not vertex.is_highlighted_by_algorithm:
            self.drawer.vertex_drawer.refresh_vertex_color(vertex)

    def _on_enter_edge(self, edge):
        self.drawer.edge_drawer.highlight_edge_color(edge)

    def _on_leave_edge(self, edge):
        if not edge.is_highlighted_by_algorithm:
            self.drawer.edge_drawer.refresh_edge_color(edge)
