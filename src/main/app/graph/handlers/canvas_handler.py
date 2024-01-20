from src.main.app.graph.vertex import Vertex
from src.main.app.utils.constants import *


class CanvasHandler:
    def __init__(self, canvas, drawer, graph, is_directed, is_digraph):
        self.canvas = canvas
        self.graph = graph
        self.drawer = drawer
        self.is_directed = is_directed
        self.is_digraph = is_digraph
        self.selected_vertexes = []
        self.canvas.bind("<Shift-Button-1>", self._on_shift_button_1)

    def _on_shift_button_1(self, event):
        self._add_vertex(event)

    def change_is_directed(self):
        self.is_directed = not self.is_directed

    def change_is_digraph(self):
        self.is_digraph = not self.is_digraph

    def _on_add_edge(self, event):
        self.enabled_vertex_select = True

    def _add_vertex(self, event):
        if len(self.graph.V) < 50:
            vertex = Vertex(str(len(self.graph.V) + 1),
                            self.canvas.winfo_width(),
                            self.canvas.winfo_height(),
                            event.x,
                            event.y)
            self.graph.add_vertex(vertex)
            self.drawer.draw_vertex(vertex, self.graph, VERTEX_BG_COLOR, VERTEX_FG_COLOR)
            self.canvas.tag_bind(f"text_{vertex.label}", "<Alt-ButtonPress-1>",
                                 lambda e, v=vertex: self._on_vertex_click(e, v))
            self.canvas.tag_bind(f"vertex_{vertex.label}", "<Alt-ButtonPress-1>",
                                 lambda e, v=vertex: self._on_vertex_click(e, v))

    def _on_vertex_click(self, event, vertex):
        if (vertex.x - RADIUS < event.x < vertex.x + RADIUS and vertex.y - RADIUS < event.y < vertex.y + RADIUS
                and len(self.selected_vertexes) < 2 and vertex not in self.selected_vertexes):
            self.selected_vertexes.append(vertex)
            self.drawer.color_vertex(vertex, self.graph)
        if len(self.selected_vertexes) == 2 and self.selected_vertexes[0] != self.selected_vertexes[1]:
            edge = self.graph.add_edge(self.selected_vertexes[0], self.selected_vertexes[1], self.is_directed,
                                       self.is_digraph)
            self.drawer.uncolor_vertex(self.selected_vertexes[0], self.graph)
            self.drawer.uncolor_vertex(self.selected_vertexes[1], self.graph)
            self.drawer.draw_edge(edge)
            self.selected_vertexes = []
