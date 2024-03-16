class Edge:
    def __init__(self, vertex1, vertex2, directed=False, digraph=False, weight=None):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.directed = directed
        self.digraph = digraph
        self.weight = weight
        self.label = vertex1.label + '_' + vertex2.label
        self.is_highlighted_by_algorithm = False

    def __eq__(self, other):
        if self.directed:
            return self.label == other.label
        else:
            return self.label == other.label or self.label == other.label[::-1]

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        string = f'Edge(label={self.label}'
        if self.weight is not None:
            string += f', weight={self.weight})'
        else:
            string += ')'
        return string
