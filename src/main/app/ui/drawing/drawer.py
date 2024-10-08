from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex

from src.main.app.utils.logger import setup_logger

logger = setup_logger("Drawer")


class Drawer:

    def __init__(self, canvas, edge_drawer, vertex_drawer):
        self.graph = None
        self.canvas = canvas
        self.edge_drawer = edge_drawer
        self.vertex_drawer = vertex_drawer
        self.grid_lines = []

    def erase_vertex_and_incidental_edges(self, vertex):
        self.edge_drawer.erase_edges_incidental(vertex, self.graph)
        self.vertex_drawer.erase_vertex(vertex)

    def highlight_edge_algorithm(self, edge):
        self.edge_drawer.highlight_edge_color(edge)
        edge.is_highlighted_by_algorithm = True

    def _highlight_vertex_algorithm(self, vertex):
        self.vertex_drawer.highlight_vertex_color(vertex)
        vertex.is_highlighted_by_algorithm = True

    def highlight_vertex_delay(self, vertex, delay):
        self.canvas.after(delay, lambda: self._highlight_vertex_algorithm(vertex))

    def refresh_vertex_delay(self, vertex, delay):
        self.vertex_drawer.refresh_vertex_delay(vertex, delay)

    def refresh_edge_delay(self, edge, delay):
        self.canvas.after(delay, lambda: self.edge_drawer.refresh_edge_color(edge))

    def highlight_edge_delay(self, edge, delay):
        self.canvas.after(delay, lambda: self.highlight_edge_algorithm(edge))

    def highlight_edge_kruskal(self, edge, delay):
        self.highlight_vertex_delay(edge.vertex1, delay)
        self.highlight_vertex_delay(edge.vertex2, delay)
        if edge is not None:
            self.highlight_edge_delay(edge, delay)

    def draw_dijkstra_distance(self, vertex, distance, delay):
        self.canvas.after(delay, lambda: self.vertex_drawer.draw_current_distance(vertex, int(distance)))

    def erase_dijkstra_distance(self, vertex, delay):
        self.canvas.after(delay, lambda: self.vertex_drawer.erase_current_distance(vertex))

    def color_element(self, element, delay):
        if isinstance(element, Vertex):
            self.highlight_vertex_delay(element, delay)
        elif isinstance(element, Edge):
            self.highlight_edge_delay(element, delay)

    def refresh_all(self, graph):
        if graph is None:
            return
        for vertex in graph.V:
            vertex.is_highlighted_by_algorithm = False
            self.vertex_drawer.erase_current_distance(vertex)
        for edge in graph.E:
            edge.is_highlighted_by_algorithm = False
        if graph is not None:
            self.vertex_drawer.erase_all_vertexes(graph.V)
            self.edge_drawer.erase_all_edges(graph.E)
            self.draw_graph(graph)

    def erase_all(self):
        self.canvas.delete('all')

    def erase_all_no_grid(self):
        if self.graph is not None:
            self.vertex_drawer.erase_all_vertexes(self.graph.V)
            self.edge_drawer.erase_all_edges(self.graph.E)

    def draw_graph(self, graph):
        self.graph = graph
        self.edge_drawer.draw_all_edges(graph)
        self.vertex_drawer.draw_all_vertexes(graph.V)

    def draw_grid(self, width, height):
        line_distance = 50

        # horizontal lines
        for x in range(0, width, line_distance):
            line_id = self.canvas.create_line(x, 0, x, height, fill='gray')
            self.grid_lines.append(line_id)
        # vertical lines
        for y in range(0, height, line_distance):
            line_id = self.canvas.create_line(0, y, width, y, fill='gray')
            self.grid_lines.append(line_id)
        if self.graph is not None:
            self.edge_drawer.raise_all_edges(self.graph.E)
            self.vertex_drawer.raise_all_vertexes(self.graph.V)

    def erase_grid(self):
        for line_id in self.grid_lines:
            self.canvas.delete(line_id)
        self.grid_lines.clear()
