import tkinter
from src.app.utils.const import *


def end_line_point(vertex1, vertex2):
    import math
    delta_x = 0
    delta_y = 0
    if vertex1.x == vertex2.x:
        delta_x = 0
        delta_y = RADIUS
    if vertex1.y == vertex2.y:
        delta_x = RADIUS
        delta_y = 0
    if vertex1.x != vertex2.x and vertex2.y != vertex1.y:
        a = (vertex2.y - vertex1.y) / (vertex2.x - vertex1.x)
        angle = math.atan(a)
        delta_y = RADIUS * math.sin(angle)
        delta_x = RADIUS * math.cos(angle)
    if vertex2.x - vertex1.x > 0:
        delta_x = -delta_x
        delta_y = -delta_y

    return delta_x, delta_y


def apex_point(vertex1, vertex2):
    import math
    mid_x = (vertex1.x + vertex2.x) / 2
    mid_y = (vertex1.y + vertex2.y) / 2
    dx = vertex2.x - vertex1.x
    dy = vertex2.y - vertex1.y
    perpendicular_dx = -dy
    perpendicular_dy = dx
    length = math.sqrt(perpendicular_dx ** 2 + perpendicular_dy ** 2)
    scaled_dx = (APEX_DISTANCE / length) * perpendicular_dx
    scaled_dy = (APEX_DISTANCE / length) * perpendicular_dy
    apex_x = mid_x + scaled_dx
    apex_y = mid_y + scaled_dy

    return apex_x, apex_y


class Drawer:

    def __init__(self, canvas):
        # self.graph = graph
        self.canvas = canvas
        # self.draw_all_vertexes()
        # self.draw_all_edges()

    # VERTEX_METHODS
    def draw_vertex(self, vertex, graph, back_color, font_color):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS,
                                fill=back_color,
                                outline=font_color, width=2,
                                tags=f"vertex_{vertex.label}")
        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label,
                                font=("Arial", VERTEX_FONT_SIZE),
                                fill=font_color,
                                tags=f"text_{vertex.label}")
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-1>", lambda event: self.start_move(event))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<B1-Motion>",
                             lambda event, g=graph, v=vertex: self.move(event, v, g))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-1>", lambda event: self.start_move(event))
        self.canvas.tag_bind(f"text_{vertex.label}", "<B1-Motion>",
                             lambda event, g=graph, v=vertex: self.move(event, v, g))

    def draw_all_vertexes(self, graph):
        for vertex in graph.V:
            self.draw_vertex(vertex, graph, VERTEX_BG_COLOR, VERTEX_FG_COLOR)

    def raise_vertex(self, vertex):
        self.canvas.tag_raise(f"vertex_{vertex.label}")
        self.canvas.tag_raise(f"text_{vertex.label}")

    def raise_vertexes(self, vertexes):
        for vertex in vertexes:
            self.raise_vertex(vertex)

    def color_vertex(self, vertex, graph):
        if vertex is not None:
            self.canvas.delete(f"vertex_{vertex.label}")
            self.canvas.delete(f"text_{vertex.label}")
            self.draw_vertex(vertex, graph, VERTEX_COLOR_CHANGE_BG, VERTEX_COLOR_CHANGE_FG)
            self.canvas.update_idletasks()
            self.canvas.tag_raise(f"vertex_{vertex.label}")
            self.canvas.tag_raise(f"text_{vertex.label}")

    # EDGE_METHODS
    def draw_all_edges(self, edges):
        for edge in edges:
            self.draw_edge(edge, VERTEX_FG_COLOR, EDGE_WIDTH)

    def erase_edges(self, edges):
        for edge in edges:
            self.canvas.delete(f"edge_{edge.label}")

    def draw_edge(self, edge, color, width):
        if edge.directed:
            self.draw_directed_edge(edge, color, width)
        else:
            self.draw_undirected_edge(edge, color, width)

    def draw_undirected_edge(self, edge, color, width):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        label = vertex1.label + '_' + vertex2.label
        end_line_points = end_line_point(vertex1, vertex2)
        self.canvas.create_line(
            vertex1.x,
            vertex1.y,
            vertex2.x + end_line_points[0],
            vertex2.y + end_line_points[1],
            fill=color, width=width,
            tags=f"edge_{label}",
            smooth=True)

    def draw_directed_edge(self, edge, color, width):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        label = vertex1.label + '_' + vertex2.label
        end_line_points = end_line_point(vertex1, vertex2)
        apex = apex_point(vertex1, vertex2)
        line = self.canvas.create_line(
            vertex1.x,
            vertex1.y,
            apex[0],
            apex[1],
            vertex2.x + end_line_points[0],
            vertex2.y + end_line_points[1],
            fill=color, width=width,
            tags=f"edge_{label}",
            smooth=True)
        if edge.directed:
            arrow_shape = (9, 9, 6)
            self.canvas.itemconfig(line, arrow=tkinter.LAST, arrowshape=arrow_shape)

    def color_edge(self, edge):
        if edge is not None:
            self.canvas.delete(f"edge_{edge.label}")
            self.canvas.tag_raise(f"edge_{edge.label}")
            self.draw_edge(edge, EDGE_COLOR_CHANGE_BG, EDGE_WIDTH + 1.5)
            self.canvas.update_idletasks()
            self.raise_vertex(edge.vertex1)
            self.raise_vertex(edge.vertex2)

    # OTHER_METHODS
    def refresh_all(self, graph):
        for vertex in graph.V:
            self.canvas.delete(f"vertex_{vertex.label}")
            self.canvas.delete(f"text_{vertex.label}")
        for edge in graph.E:
            self.canvas.delete(f"edge_{edge.label}")

        self.draw_all_edges(graph.E)
        self.draw_all_vertexes(graph)
        self.raise_vertexes(graph.V)

    def draw_graph(self, graph):
        self.erase_edges(graph.E)
        self.draw_all_vertexes(graph)
        self.draw_all_edges(graph.E)

    def start_move(self, event):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return

    def move(self, event, vertex, graph):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return
        delta_x = event.x - vertex.x
        delta_y = event.y - vertex.y
        vertex.x = event.x
        vertex.y = event.y
        self.erase_edges(graph.E)
        self.canvas.move(f"vertex_{vertex.label}", delta_x, delta_y)
        self.canvas.move(f"text_{vertex.label}", delta_x, delta_y)
        self.draw_all_edges(graph.E)
        self.raise_vertexes(graph.V)