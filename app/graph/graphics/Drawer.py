from app.utils.const import *


class Drawer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas
        self.draw_all_vertexes()
        self.draw_all_edges()

    def draw_vertex(self, vertex, back_color, font_color):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS,
                                fill=back_color,
                                outline=font_color, width=2,
                                tags=f"vertex_{vertex.label}")

        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label,
                                font=("Arial", VERTEX_FONT_SIZE), fill=font_color,
                                tags=f"text_{vertex.label}")

        self.canvas.tag_bind(f"vertex_{vertex.label}", "<ButtonPress-1>",
                             lambda event, v=vertex: self.start_move(event, v))
        self.canvas.tag_bind(f"vertex_{vertex.label}", "<B1-Motion>", lambda event, v=vertex: self.move(event, v))
        self.canvas.tag_bind(f"text_{vertex.label}", "<ButtonPress-1>",
                             lambda event, v=vertex: self.start_move(event, v))
        self.canvas.tag_bind(f"text_{vertex.label}", "<B1-Motion>", lambda event, v=vertex: self.move(event, v))

    def draw_all_vertexes(self):
        V = self.graph.V
        for i in range(len(V)):
            self.draw_vertex(V[i], VERTEX_BG_COLOR, VERTEX_FG_COLOR)

    def draw_edge(self, edge, color, width):
        self.draw_edge_by_vertexes(edge.vertex1, edge.vertex2, color, width)

    def draw_edge_by_vertexes(self, vertex1, vertex2, color, width):
        if not self.graph.is_digraph:
            label = vertex1.label + '_' + vertex2.label
            self.canvas.create_line(
                vertex1.x,
                vertex1.y,
                vertex2.x,
                vertex2.y,
                fill=color, width=width,
                tags=f"edge_{label}")
            self.raise_vertexes()
        else:
            print('digraph edge drawing')


    def raise_vertexes(self):
        V = self.graph.V
        for i in range(len(V)):
            vert = V[i]
            self.canvas.tag_raise(f"vertex_{vert.label}")
            self.canvas.tag_raise(f"text_{vert.label}")

    def draw_all_edges(self):
        edges = self.graph.E
        for edge in edges:
            self.draw_edge(edge, VERTEX_FG_COLOR, EDGE_WIDTH)

    def erase_edges(self):
        edges = self.graph.E
        for edge in edges:
            self.canvas.delete(f"edge_{edge.label}")

    def start_move(self, event, vertex):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return
        vertex.x = event.x
        vertex.y = event.y
        print(vertex)

    def move(self, event, vertex):
        if (event.x <= RADIUS or event.x >= self.canvas.winfo_width() - RADIUS
                or event.y <= RADIUS or event.y >= self.canvas.winfo_height() - RADIUS):
            return
        deltax = event.x - vertex.x
        deltay = event.y - vertex.y
        vertex.x = event.x
        vertex.y = event.y
        self.erase_edges()
        self.canvas.move(f"vertex_{vertex.label}", deltax, deltay)
        self.canvas.move(f"text_{vertex.label}", deltax, deltay)
        self.draw_all_edges()

    def color_edge(self, edge_label):
        edge = self.graph.find_edge(edge_label)
        print('color_edge:'+str(edge))
        if edge is not None:
            self.canvas.delete(f"edge_{edge.label}")
            self.canvas.tag_raise(f"edge_{edge.label}")
            self.draw_edge(edge, EDGE_COLOR_CHANGE_BG, EDGE_WIDTH + 1.5)
            self.canvas.update_idletasks()

    def color_vert(self, vert_label):
        vert = self.graph.find_vertex(vert_label)
        if vert is not None:
            self.canvas.delete(f"vertex_{vert.label}")
            self.canvas.delete(f"text_{vert.label}")
            self.draw_vertex(vert, VERTEX_COLOR_CHANGE_BG, VERTEX_COLOR_CHANGE_FG)
            self.canvas.update_idletasks()

    def refresh_all(self):
        for vertex in self.graph.V:
            self.canvas.delete(f"vertex_{vertex.label}")
            self.canvas.delete(f"text_{vertex.label}")

        for edge in self.graph.E:
            self.canvas.delete(f"edge_{edge.label}")
        self.draw_all_edges()
        self.draw_all_vertexes()
