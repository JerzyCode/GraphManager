from app.utils.const import RADIUS


class Edge:
    def __init__(self, vertex1, vertex2, directed, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.directed = directed
        self.weight = weight
        self.label = vertex1.label + '_' + vertex2.label
        vertex1.edges.add(self)
        vertex2.edges.add(self)

    def __eq__(self, other):
        # if not self.directed:
        #     return (
        #             (self.label == other.label) or (self.label[::-1] == other.label)
        #     )
        # else:
        return self.label == other.label

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return self.label
