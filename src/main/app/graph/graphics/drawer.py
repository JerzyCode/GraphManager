import tkinter

from src.main.app.utils.constants import *


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


def middle_point(vertex1, vertex2):
    mid_x = (vertex1.x + vertex2.x) / 2
    mid_y = (vertex1.y + vertex2.y) / 2
    return mid_x, mid_y


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


def _prepare_draw_edge(edge, is_digraph):
    params = {}
    vertex1 = edge.vertex1
    vertex2 = edge.vertex2
    label = vertex1.label + '_' + vertex2.label
    end_line_points = end_line_point(vertex1, vertex2)
    params['vertex1_x'] = edge.vertex1.x
    params['vertex1_y'] = edge.vertex1.y
    params['vertex2_x'] = edge.vertex2.x
    params['vertex2_y'] = edge.vertex2.y
    params['label'] = label
    params['end_line_points'] = end_line_points
    if is_digraph:
        apex = apex_point(vertex1, vertex2)
        params['apex'] = apex
    return params


class Drawer:

    def __init__(self, canvas):
        self.canvas = canvas

    # VERTEX_METHODS
    def draw_vertex(self, vertex, graph, back_color, font_color):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS, fill=back_color, outline=font_color,
                                width=2, tags=f"vertex_{vertex.label}")
        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label, font=("Arial", VERTEX_FONT_SIZE), fill=font_color, tags=f"text_{vertex.label}")
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move(event))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<B1-Motion>", lambda event, g=graph, v=vertex: self._move(event, v, g))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-1>", lambda event: self._start_move(event))
        self.canvas.tag_bind(f"text_{vertex.label}", "<B1-Motion>", lambda event, g=graph, v=vertex: self._move(event, v, g))

    def _draw_all_vertexes(self, graph):
        for vertex in graph.V:
            self.draw_vertex(vertex, graph, VERTEX_BG_COLOR, VERTEX_FG_COLOR)

    def _raise_vertex(self, vertex):
        self.canvas.tag_raise(f"vertex_{vertex.label}")
        self.canvas.tag_raise(f"text_{vertex.label}")

    def _raise_all_vertexes(self, vertexes):
        for vertex in vertexes:
            self._raise_vertex(vertex)

    def color_vertex(self, vertex):
        if vertex is not None:
            self._color_vertex(vertex, VERTEX_COLOR_CHANGE_BG, VERTEX_COLOR_CHANGE_FG)

    def color_vertex_delay(self, vertex, delay):
        self.canvas.after(delay, lambda: self.color_vertex(vertex))

    def uncolor_vertex(self, vertex):
        if vertex is not None:
            self._color_vertex(vertex, VERTEX_BG_COLOR, VERTEX_FG_COLOR)

    def _color_vertex(self, vertex, color_bg, color_fg):
        self.canvas.itemconfig(f"vertex_{vertex.label}", fill=color_bg)
        self.canvas.itemconfig(f"text_{vertex.label}", fill=color_fg)

    # EDGE_METHODS
    def _draw_weight(self, edge, weight_color):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        mid_point = middle_point(vertex1, vertex2)
        self.canvas.create_text(mid_point[0], mid_point[1], fill=weight_color, font=("Arial", 14, "bold"),
                                text=edge.weight, anchor="center", tags=f'weight_{edge.weight}_{edge.label}')

    def _draw_all_edges(self, graph):
        for edge in graph.E:
            self._draw_edge(edge, EDGE_COLOR, EDGE_WIDTH)

    def _erase_edge(self, edge):
        self.canvas.delete(f"edge_{edge.label}")

    def _erase_weight(self, edge):
        self.canvas.delete(f'weight_{edge.weight}_{edge.label}')

    def _erase_edges(self, edges):
        for edge in edges:
            self._erase_edge(edge)
            self._erase_weight(edge)

    def hide_all_weights(self, graph):
        if graph is not None and graph.is_weighted:
            for edge in graph.E:
                self._erase_weight(edge)

    def draw_all_weights(self, graph):
        if graph.is_weighted:
            for edge in graph.E:
                self._draw_weight(edge, WEIGHT_COLOR)

    def draw_edge(self, edge):
        self._draw_edge(edge, EDGE_COLOR, EDGE_WIDTH)

    def _draw_edge(self, edge, color, width):
        if edge.digraph:
            self._draw_digraph_edge(edge, color, width)
        else:
            self._draw_graph_edge(edge, color, width)

    def _draw_graph_edge(self, edge, color, width):
        params = _prepare_draw_edge(edge, is_digraph=False)
        self._draw_canvas_line(color, width, params, edge.directed)

    def _draw_digraph_edge(self, edge, color, width):
        params = _prepare_draw_edge(edge, is_digraph=True)
        self._draw_canvas_line(color, width, params, edge.directed)

    def _draw_canvas_line(self, color, width, params, is_directed):
        if 'apex' in params:
            line = self.canvas.create_line(
                params['vertex1_x'], params['vertex1_y'],
                params['apex'][0], params['apex'][1],
                params['vertex2_x'] + params['end_line_points'][0],
                params['vertex2_y'] + params['end_line_points'][1],
                fill=color, width=width,
                tags=f"edge_{params['label']}", smooth=True)
        else:
            line = self.canvas.create_line(
                params['vertex1_x'], params['vertex1_y'],
                params['vertex2_x'] + params['end_line_points'][0],
                params['vertex2_y'] + params['end_line_points'][1],
                fill=color, width=width,
                tags=f"edge_{params['label']}", smooth=True)

        if is_directed:
            arrow_shape = (9, 9, 6)
            self.canvas.itemconfig(line, arrow=tkinter.LAST, arrowshape=arrow_shape)

    def _draw_edges_incidental(self, edges):
        for edge in edges:
            self._draw_edge(edge, edges.get(edge)["color"], edges.get(edge)["width"])

    def _erase_edges_incidental(self, edges, vertex):
        erased_edges_params = {}
        for edge in edges:
            if edge.vertex1 == vertex or edge.vertex2 == vertex:
                fill_color = self.canvas.itemcget(f"edge_{edge.label}", "fill")
                width = self.canvas.itemcget(f"edge_{edge.label}", "width")
                erased_edges_params[edge] = {"color": fill_color, "width": width}
                self._erase_edge(edge)
        return erased_edges_params

    def _erase_weights_incidental(self, edges, vertex):
        erased_weights_param = {}
        for edge in edges:
            if edge.vertex1 == vertex or edge.vertex2 == vertex:
                fill_color = self.canvas.itemcget(f'weight_{edge.weight}_{edge.label}', "fill")
                erased_weights_param[edge] = fill_color
                self._erase_weight(edge)
        return erased_weights_param

    def _draw_weights_incidental(self, edges):
        for edge in edges:
            self._draw_weight(edge, edges.get(edge))

    def _move_edges_incidental(self, edges, vertex):
        erased_edges_params = self._erase_edges_incidental(edges, vertex)
        self._draw_edges_incidental(erased_edges_params)
        erased_weight_params = self._erase_weights_incidental(edges, vertex)
        self._draw_weights_incidental(erased_weight_params)

    def color_edge(self, edge):
        if edge is not None:
            self._color_edge(edge)

    def _color_edge(self, edge):
        self.canvas.itemconfig(f"edge_{edge.label}", fill=EDGE_COLOR_CHANGE_BG, width=EDGE_WIDTH + 1.5)
        self.canvas.itemconfig(f'weight_{edge.weight}_{edge.label}', fill=WEIGHT_COLOR_CHANGE)
        self.canvas.tag_raise(f"edge_{edge.label}")
        self.canvas.tag_raise(f'weight_{edge.weight}_{edge.label}')
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
            self.draw_all_weights(graph)
            self._raise_all_vertexes(graph.V)

    def erase_all(self):
        self.canvas.delete('all')

    def draw_graph(self, graph):
        self._erase_edges(graph.E)
        self._draw_all_vertexes(graph)
        self._draw_all_edges(graph)
        self.draw_all_weights(graph)
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
        self._move_edges_incidental(graph.E, vertex)
        self._raise_all_vertexes(graph.V)
