import sys

from src.main.app.graph.vertex import Vertex
from src.main.app.utils.constants import VERTEX_FG_COLOR_DARK, WEIGHT_FONT_SIZE


class VertexDrawer:
    def __init__(self, canvas, config):
        self.config = config
        self.canvas = canvas

    def draw_vertex(self, vertex: Vertex):
        radius = self.config.vertex_radius
        vertex_bg_color = self.config.vertex_bg_color
        vertex_fg_color = self.config.vertex_fg_color
        self.canvas.create_oval(vertex.x - radius, vertex.y - radius, vertex.x + radius, vertex.y + radius, fill=vertex_bg_color,
                                outline=VERTEX_FG_COLOR_DARK,
                                width=2, tags=f"vertex_{vertex.label}")
        if self.config.is_label_enabled:
            self.canvas.create_text(vertex.x, vertex.y, text=vertex.label, font=("Arial", radius), fill=vertex_fg_color,
                                    tags=f"text_{vertex.label}")

    def erase_vertex(self, vertex: Vertex):
        self.canvas.delete(f"vertex_{vertex.label}")
        self.canvas.delete(f"text_{vertex.label}")

    def raise_vertex(self, vertex: Vertex):
        self.canvas.tag_raise(f"vertex_{vertex.label}")
        self.canvas.tag_raise(f"text_{vertex.label}")

    def highlight_vertex_color(self, vertex: Vertex):
        if vertex is not None:
            self._change_vertex_color(vertex,
                                      self.config.vertex_bg_color_changed,
                                      self.config.vertex_fg_color_changed)

    def refresh_vertex_color(self, vertex: Vertex):
        if vertex is not None:
            self._change_vertex_color(vertex,
                                      self.config.vertex_bg_color,
                                      self.config.vertex_fg_color)

    def draw_current_distance(self, vertex, distance):
        self.erase_current_distance(vertex)
        if distance >= sys.maxsize / 2:
            distance = "∞"
        font_size = WEIGHT_FONT_SIZE
        if distance == "∞":
            font_size += 5
        self.canvas.create_text(vertex.x, vertex.y - self.config.vertex_radius - 8, fill='red', font=("Arial", font_size, "bold"),
                                text=distance, anchor="center", tags=f'distance_{vertex.label}')

    def erase_current_distance(self, vertex: Vertex):
        self.canvas.delete(f"distance_{vertex.label}")

    def _change_vertex_color(self, vertex: Vertex, bg_color, fg_color):
        self.canvas.itemconfig(f"vertex_{vertex.label}", fill=bg_color)
        self.canvas.itemconfig(f"text_{vertex.label}", fill=fg_color)

    def refresh_all_vertexes(self, vertexes):
        self.erase_all_vertexes(vertexes)
        self.draw_all_vertexes(vertexes)

    def raise_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.raise_vertex(vertex)

    def draw_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.draw_vertex(vertex)

    def erase_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.erase_vertex(vertex)
