class Edge:
    def __init__(self, vertex1, vertex2, directed, digraph, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.directed = directed
        self.digraph = digraph
        self.weight = weight
        self.label = vertex1.label + '_' + vertex2.label

    def __eq__(self, other):
        if self.directed:
            return self.label == other.label
        else:
            return self.label == other.label or self.label == other.label[::-1]

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return self.label
