from app.graph.Edge import Edge
from app.utils.const import RADIUS


class Drawer:
    def __init__(self, graph, canvas):
        self.graph = graph
        self.canvas = canvas
        self.draw_all_vertexes()
        self.draw_edges()


    def draw_vertex(self, vertex):
        self.canvas.create_oval(vertex.x - RADIUS, vertex.y - RADIUS, vertex.x + RADIUS, vertex.y + RADIUS,
                                fill="black",
                                outline="yellow",width=4,
                                tags=f"vertex_{vertex.label}")

        self.canvas.create_text(vertex.x, vertex.y, text=vertex.label,
                                font=("Arial", 18), fill="yellow",
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
            self.draw_vertex(V[i])

    def draw_edge(self, edge, color):
        vertex1 = edge.vertex1
        vertex2 = edge.vertex2
        self.canvas.create_line(
            vertex1.x,
            vertex1.y,
            vertex2.x,
            vertex2.y,
            fill=color, width=3,
            tags=f"edge_{edge.label}")
        self.canvas.tag_raise(f"vertex_{vertex1.label}")
        self.canvas.tag_raise(f"vertex_{vertex2.label}")
        self.canvas.tag_raise(f"text_{vertex1.label}")
        self.canvas.tag_raise(f"text_{vertex2.label}")

    def draw_edges(self):
        edges = self.graph.E
        for edge in edges:
            self.draw_edge(edge, "black")

    def erase_edges(self):
        edges = self.graph.E
        for edge in edges:
            self.canvas.delete(f"edge_{edge.label}")

    def start_move(self, event, vertex):
        vertex.x = event.x
        vertex.y = event.y
        print(vertex)

    def move(self, event, vertex):
        deltax = event.x - vertex.x
        deltay = event.y - vertex.y
        vertex.x = event.x
        vertex.y = event.y
        self.erase_edges()
        self.canvas.move(f"vertex_{vertex.label}", deltax, deltay)
        self.canvas.move(f"text_{vertex.label}", deltax, deltay)
        self.draw_edges()

    def color_edge(self, edge_label):
        edge = self.graph.find_edge(edge_label)
        if edge is not None:
            self.canvas.delete(edge_label)
            self.draw_edge(edge, 'red')

