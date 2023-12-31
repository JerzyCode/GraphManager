from app.graph.Edge import Edge
from app.utils.const import RADIUS


class Drawer:
    def __init__(self, vertex, x, y, canvas):
        self.vertex = vertex
        self.x = x
        self.y = y
        self.label = self.vertex.label
        self.edges = vertex.edges
        self.canvas = canvas
        self.canvas_tag = "vertex" + self.label
        self.draw_vertex()
        self.draw_edges()

    def draw_vertex(self):
        self.canvas.create_oval(self.x - RADIUS, self.y - RADIUS, self.x + RADIUS, self.y + RADIUS, fill="blue",
                                tags=self.canvas_tag)
        self.canvas.create_text(self.x, self.y, text=self.label, font=("Arial", 18), fill="white",
                                tags="vertex" + self.label)
        self.canvas.tag_bind(self.canvas_tag, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.canvas_tag, "<B1-Motion>", self.move)

    def draw_edge(self, edge):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        self.canvas.create_line(
            vertex1.drawer.x,
            vertex1.drawer.y,
            vertex2.drawer.x,
            vertex2.drawer.y,
            fill="black", width=5,
            tags=vertex1.label + "" + vertex2.label)
        self.canvas.tag_raise(vertex1.drawer.canvas_tag)
        self.canvas.tag_raise(vertex2.drawer.canvas_tag)

    def draw_edges(self):
        edges = self.vertex.edges
        for edge in edges:
            self.draw_edge(edge)

    def erase_edges(self):
        edges = self.vertex.edges
        for edge in edges:
            vertex1 = edge.vertex1
            vertex2 = edge.vertex2
            self.canvas.delete(vertex1.label + "" + vertex2.label)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.x = event.x
        self.y = event.y
        self.erase_edges()
        self.draw_edges()
        self.canvas.move(self.canvas_tag, deltax, deltay)

    def raise_vertex(self):
        self.canvas_tag = "vertex" + self.label
