from app.utils.const import RADIUS


class Edge:
    def __init__(self, vertex1, vertex2):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.label = vertex1.label+vertex2.label
        vertex1.edges.add(self)
        vertex2.edges.add(self)

    def __eq__(self, other):
        return (
            (self.vertex1.label == other.vertex1.label and self.vertex2.label == other.vertex2.label) or
            (self.vertex1.label == other.vertex2.label and self.vertex2.label == other.vertex1.label)
        )

    def __hash__(self):
        return hash((self.vertex1.label, self.vertex2.label))

    def __str__(self):
        return self.vertex1.label + self.vertex2.label
