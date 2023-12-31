from app.graph.Edge import Edge
from app.graph.Vertex import Vertex


class Graph:
    def __init__(self, matrix, canvas):
        self.matrix = matrix
        self.V = {}
        self.E = set()
        self.canvas = canvas
        self.create_vertexes()
        self.create_edges()

        for i in range(len(self.V)):
            print(self.V[i])
        for edge in self.E:
            print(edge)



    def create_vertexes(self):
        size = len(self.matrix)
        for i in range(size):
            self.V[i] = Vertex(str(i + 1), self.canvas)

    def create_edges(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(i,size):
                if i != j and self.matrix[i][j] == 1:
                    self.V[i].add_edge(self.V[j])
                    self.E.add(Edge(self.V[i], self.V[j]))
        # for edge in self.E:
        #     print(edge)
        #
        # for i in range(size):
        #     print(self.V[i].label)
        #     for edge in self.V[i].edges:
        #         print(edge)
