from app.graph.Edge import Edge
from app.utils.const import RADIUS


class Vertex:
    def __init__(self, label, x, y, canvas):
        self.label = label
        self.x = x
        self.y = y
        self.edges = []
        self.canvas = canvas
        self.canvas_tag = "vertex" + self.label
        self.draw_vertex()

    def draw_vertex(self):
        self.canvas.create_oval(self.x - RADIUS, self.y - RADIUS, self.x + RADIUS, self.y + RADIUS, fill="blue",
                                tags=self.canvas_tag)
        self.canvas.create_text(self.x, self.y, text=self.label, font=("Arial", 18), fill="white",
                                tags="vertex" + self.label)
        self.canvas.tag_bind(self.canvas_tag, "<ButtonPress-1>", self.start_move)
        self.canvas.tag_bind(self.canvas_tag, "<B1-Motion>", self.move)

    def add_edge(self, vertex):
        edge = Edge(self, vertex)
        edge.draw_edge()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.x = event.x
        self.y = event.y
        for edge in self.edges:
            edge.erase_edge()
            edge.draw_edge()
        self.canvas.move(self.canvas_tag, deltax, deltay)

    def raise_vertex(self):
        self.canvas_tag = "vertex" + self.label
