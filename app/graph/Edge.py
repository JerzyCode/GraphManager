from app.utils.const import RADIUS


class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        vertex1.edges.append(self)
        vertex2.edges.append(self)



