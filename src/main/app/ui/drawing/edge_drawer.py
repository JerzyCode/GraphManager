import tkinter

from src.main.app.graph.digraph import Digraph
from src.main.app.utils.constants import *

global edge_color, edge_color_changed, weight_color, weight_color_changed


def change_edge_appearance_mode(new_appearance_mode: str):
    global edge_color, edge_color_changed, weight_color, weight_color_changed
    if new_appearance_mode == "Light":
        edge_color = EDGE_COLOR_LIGHT
        edge_color_changed = EDGE_COLOR_CHANGE_LIGHT

        weight_color = WEIGHT_COLOR_LIGHT
        weight_color_changed = WEIGHT_COLOR_CHANGE_LIGHT

    elif new_appearance_mode == "Dark":
        edge_color = EDGE_COLOR_DARK
        edge_color_changed = EDGE_COLOR_CHANGE_DARK

        weight_color = WEIGHT_COLOR_DARK
        weight_color_changed = WEIGHT_COLOR_CHANGE_DARK


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


class EdgeDrawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_edge_params(self, edge, graph, color, width, previous_weight_color):
        self.draw_edge(edge, graph)
        self.change_edge_params(edge, color, width, previous_weight_color)

    def draw_edge(self, edge, graph):
        if isinstance(graph, Digraph):
            self._draw_digraph_edge(edge)
        else:
            self._draw_graph_edge(edge)

    def _draw_weight(self, edge):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        mid_point = middle_point(vertex1, vertex2)
        self.canvas.create_text(mid_point[0], mid_point[1], fill=weight_color, font=("Arial", WEIGHT_FONT_SIZE, "bold"),
                                text=edge.weight, anchor="center", tags=f'weight_{edge.weight}_{edge.label}')

    def _draw_graph_edge(self, edge):
        params = _prepare_draw_edge(edge, is_digraph=False)
        line = self.canvas.create_line(
            params['vertex1_x'], params['vertex1_y'],
            params['vertex2_x'] + params['end_line_points'][0],
            params['vertex2_y'] + params['end_line_points'][1],
            fill=edge_color, width=EDGE_WIDTH,
            tags=f"edge_{params['label']}", smooth=True)
        if edge.weight is not None:
            self._draw_weight(edge)
        if edge.directed:
            arrow_shape = (9, 9, 6)
            self.canvas.itemconfig(line, arrow=tkinter.LAST, arrowshape=arrow_shape)

    def _draw_digraph_edge(self, edge):
        params = _prepare_draw_edge(edge, is_digraph=True)
        line = self.canvas.create_line(
            params['vertex1_x'], params['vertex1_y'],
            params['apex'][0], params['apex'][1],
            params['vertex2_x'] + params['end_line_points'][0],
            params['vertex2_y'] + params['end_line_points'][1],
            fill=edge_color, width=EDGE_WIDTH,
            tags=f"edge_{params['label']}", smooth=True)
        if edge.weight is not None:
            self._draw_weight(edge)
        if edge.directed:
            arrow_shape = (9, 9, 6)
            self.canvas.itemconfig(line, arrow=tkinter.LAST, arrowshape=arrow_shape)

    def erase_edge(self, edge):
        self.canvas.delete(f"edge_{edge.label}")
        if edge.weight is not None:
            self.canvas.delete(f'weight_{edge.weight}_{edge.label}')

    def change_edge_params(self, edge, color, width, previous_weight_color):
        self.canvas.itemconfig(f"edge_{edge.label}", fill=color, width=width)
        self.canvas.tag_raise(f"edge_{edge.label}")
        if edge.weight is not None:
            self.canvas.itemconfig(f'weight_{edge.weight}_{edge.label}', fill=previous_weight_color)
            self.canvas.tag_raise(f'weight_{edge.weight}_{edge.label}')

    def erase_edges_incidental(self, vertex, graph):
        erased_edges_params = {}
        for edge in graph.E:
            if edge.vertex1 == vertex or edge.vertex2 == vertex:
                fill_color_edge = self.canvas.itemcget(f"edge_{edge.label}", "fill")
                width = self.canvas.itemcget(f"edge_{edge.label}", "width")
                erased_edges_params[edge] = {"color": fill_color_edge, "width": width, "weight_color": None}
                if edge.weight is not None:
                    fill_color_weight = self.canvas.itemcget(f'weight_{edge.weight}_{edge.label}', "fill")
                    erased_edges_params[edge]["weight_color"] = fill_color_weight
                self.erase_edge(edge)
        return erased_edges_params

    def _draw_edges_incidental(self, graph, edges):
        for edge in edges:
            params = edges.get(edge)
            self.draw_edge_params(edge, graph, params["color"], params["width"], params["weight_color"])

    def move_edge_incidental(self, vertex, graph):
        erased_edges_params = self.erase_edges_incidental(vertex, graph)
        self._draw_edges_incidental(graph, erased_edges_params)
