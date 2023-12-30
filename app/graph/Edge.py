from app.utils.const import RADIUS


class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.edge_canvas_id = f"{vertex1.label}_{vertex2.label}_edge"
        self.add_edge_to_vertexes()
        self.canvas = vertex1.canvas

    def draw_edge(self):
        vertex1 = self.vertex1
        vertex2 = self.vertex2
        self.canvas.create_line(vertex1.x, vertex1.y, vertex2.x, vertex2.y, fill="black", width=5,
                                tags=self.edge_canvas_id)
        self.canvas.tag_raise(vertex1.canvas_tag)
        self.canvas.tag_raise(vertex2.canvas_tag)


    def erase_edge(self):
        self.canvas.delete(self.edge_canvas_id)

    def add_edge_to_vertexes(self):
        self.vertex1.edges.append(self)
        self.vertex2.edges.append(self)
