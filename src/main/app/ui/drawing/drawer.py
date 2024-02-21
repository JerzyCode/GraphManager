from src.main.app.ui.drawing.edge_drawer import change_edge_appearance_mode
from src.main.app.utils.constants import *
from src.main.app.utils.logger import setup_logger

logger = setup_logger("CanvasHandler")

global vertex_bg_color, vertex_fg_color, vertex_bg_color_changed, vertex_fg_color_changed, edge_color_changed, weight_color_changed


def change_appearance_mode(new_appearance_mode: str):
    global vertex_bg_color, vertex_fg_color, vertex_bg_color_changed, vertex_fg_color_changed, edge_color_changed, weight_color_changed
    if new_appearance_mode == "Light":
        vertex_bg_color = VERTEX_BG_COLOR_LIGHT
        vertex_fg_color = VERTEX_FG_COLOR_LIGHT
        vertex_bg_color_changed = VERTEX_COLOR_CHANGE_BG_LIGHT
        vertex_fg_color_changed = VERTEX_COLOR_CHANGE_FG_LIGHT
        edge_color_changed = EDGE_COLOR_CHANGE_LIGHT
        weight_color_changed = WEIGHT_COLOR_CHANGE_LIGHT
        change_edge_appearance_mode("Light")

    elif new_appearance_mode == "Dark":
        vertex_bg_color = VERTEX_BG_COLOR_DARK
        vertex_fg_color = VERTEX_FG_COLOR_DARK
        vertex_bg_color_changed = VERTEX_COLOR_CHANGE_BG_DARK
        vertex_fg_color_changed = VERTEX_COLOR_CHANGE_FG_DARK
        edge_color_changed = EDGE_COLOR_CHANGE_DARK
        weight_color_changed = WEIGHT_COLOR_CHANGE_DARK
        change_edge_appearance_mode("Dark")


change_appearance_mode("Dark")


class Drawer:

    def __init__(self, canvas, edge_drawer):
        self.graph = None
        self.canvas = canvas
        self.edge_drawer = edge_drawer

    def draw_vertex(self, vertex, graph):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS, fill=vertex_bg_color,
                                outline=VERTEX_FG_COLOR_DARK,
                                width=2, tags=f"vertex_{vertex.label}")
        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label, font=("Arial", VERTEX_FONT_SIZE), fill=vertex_fg_color,
                                tags=f"text_{vertex.label}")
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move(event))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<B1-Motion>", lambda event, g=graph, v=vertex: self._move(event, v, g))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move(event))
        self.canvas.tag_bind(f"text_{vertex.label}", "<B1-Motion>", lambda event, g=graph, v=vertex: self._move(event, v, g))

    def _draw_all_vertexes(self, graph):
        for vertex in graph.V:
            self.draw_vertex(vertex, graph)

    def _raise_vertex(self, vertex):
        self.canvas.tag_raise(f"vertex_{vertex.label}")
        self.canvas.tag_raise(f"text_{vertex.label}")

    def _raise_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self._raise_vertex(vertex)

    def erase_vertex_and_incidental_edges(self, vertex):
        self.canvas.delete(f"vertex_{vertex.label}")
        self.canvas.delete(f"text_{vertex.label}")
        self.edge_drawer.erase_edges_incidental(vertex, self.graph)

    def color_vertex(self, vertex):
        if vertex is not None:
            self._color_vertex(vertex, vertex_bg_color_changed, vertex_fg_color_changed)

    def color_vertex_delay(self, vertex, delay):
        self.canvas.after(delay, lambda: self.color_vertex(vertex))

    def uncolor_vertex(self, vertex):
        if vertex is not None:
            self._color_vertex(vertex, vertex_bg_color, vertex_fg_color)

    def _color_vertex(self, vertex, color_bg, color_fg):
        self.canvas.itemconfig(f"vertex_{vertex.label}", fill=color_bg)
        self.canvas.itemconfig(f"text_{vertex.label}", fill=color_fg)

    def _draw_all_edges(self, graph):
        for edge in graph.E:
            self.edge_drawer.draw_edge(edge, graph)

    def _erase_edges(self, edges):
        for edge in edges:
            self.edge_drawer.erase_edge(edge)

    # TODO metody na dole powinny mieć logike w edge_drawer, a tutaj ewentualnie wywołanie dla ułatwienia
    def color_edge(self, edge):
        if edge is not None:
            self.edge_drawer.change_edge_params(edge, edge_color_changed, EDGE_WIDTH_WIDER, weight_color_changed)
            self._raise_vertex(edge.vertex1)
            self._raise_vertex(edge.vertex2)

    def color_edge_delay(self, edge, delay):
        self.canvas.after(delay, lambda: self.color_edge(edge))

    def color_edge_kruskal(self, edge, delay):
        self.color_vertex_delay(edge.vertex1, delay)
        self.color_vertex_delay(edge.vertex2, delay)
        if edge is not None:
            self.color_edge_delay(edge, delay)

    # OTHER_METHODS
    def refresh_all(self, graph):
        if graph is not None:
            for vertex in graph.V:
                self.canvas.delete(f"vertex_{vertex.label}")
                self.canvas.delete(f"text_{vertex.label}")
            self._erase_edges(graph.E)
            self._draw_all_edges(graph)
            self._draw_all_vertexes(graph)
            self._raise_all_vertexes(graph.V)

    def erase_all(self):
        self.canvas.delete('all')

    def draw_graph(self, graph):
        self.graph = graph
        self._erase_edges(graph.E)
        self._draw_all_vertexes(graph)
        self._draw_all_edges(graph)
        self._raise_all_vertexes(graph.V)

    def _start_move(self, event):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return

    def _move(self, event, vertex, graph):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return
        delta_x = event.x - vertex.x
        delta_y = event.y - vertex.y
        vertex.x = event.x
        vertex.y = event.y
        self.canvas.move(f"vertex_{vertex.label}", delta_x, delta_y)
        self.canvas.move(f"text_{vertex.label}", delta_x, delta_y)
        self.edge_drawer.move_edge_incidental(vertex, graph)
        self._raise_all_vertexes(graph.V)
