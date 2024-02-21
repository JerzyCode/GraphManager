from src.main.app.graph.vertex import Vertex
from src.main.app.utils.constants import *


def change_vertex_appearance_mode(new_appearance_mode: str):
    global vertex_bg_color, vertex_fg_color, vertex_bg_color_changed, vertex_fg_color_changed
    if new_appearance_mode == "Light":
        vertex_bg_color = VERTEX_BG_COLOR_LIGHT
        vertex_fg_color = VERTEX_FG_COLOR_LIGHT
        vertex_bg_color_changed = VERTEX_COLOR_CHANGE_BG_LIGHT
        vertex_fg_color_changed = VERTEX_COLOR_CHANGE_FG_LIGHT

    elif new_appearance_mode == "Dark":
        vertex_bg_color = VERTEX_BG_COLOR_DARK
        vertex_fg_color = VERTEX_FG_COLOR_DARK
        vertex_bg_color_changed = VERTEX_COLOR_CHANGE_BG_DARK
        vertex_fg_color_changed = VERTEX_COLOR_CHANGE_FG_DARK


class VertexDrawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_vertex(self, vertex: Vertex):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS, fill=vertex_bg_color,
                                outline=VERTEX_FG_COLOR_DARK,
                                width=2, tags=f"vertex_{vertex.label}")
        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label, font=("Arial", VERTEX_FONT_SIZE), fill=vertex_fg_color,
                                tags=f"text_{vertex.label}")

    def erase_vertex(self, vertex: Vertex):
        self.canvas.delete(f"vertex_{vertex.label}")
        self.canvas.delete(f"text_{vertex.label}")

    def raise_vertex(self, vertex: Vertex):
        self.canvas.tag_raise(f"vertex_{vertex.label}")
        self.canvas.tag_raise(f"text_{vertex.label}")

    def highlight_vertex_color(self, vertex: Vertex):
        if vertex is not None:
            self._change_vertex_color(vertex, vertex_bg_color_changed, vertex_fg_color_changed)

    def refresh_vertex_color(self, vertex: Vertex):
        if vertex is not None:
            self._change_vertex_color(vertex, vertex_bg_color, vertex_fg_color)

    def _change_vertex_color(self, vertex: Vertex, bg_color, fg_color):
        self.canvas.itemconfig(f"vertex_{vertex.label}", fill=bg_color)
        self.canvas.itemconfig(f"text_{vertex.label}", fill=fg_color)

    def raise_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.raise_vertex(vertex)

    def draw_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.draw_vertex(vertex)

    def erase_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self.erase_vertex(vertex)
