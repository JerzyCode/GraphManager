import random
import threading
import time
from queue import Queue, PriorityQueue

from app.graph.Edge import Edge
from app.graph.Vertex import Vertex


class Graph:
    def __init__(self, matrix, canvas, is_directed):
        self.matrix = matrix
        self.V = set()
        self.E = set()
        self.is_directed = is_directed
        self.canvas = canvas
        self.create_vertexes()
        self.create_edges()

    def create_vertexes(self):
        size = len(self.matrix)
        self.V = list(range(size))
        for i in range(size):
            self.V[i] = Vertex(str(i + 1), self.canvas)

    def create_edges(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(i, size):
                if i != j and self.matrix[i][j] == 1:
                    # self.V[i].add_edge(self.V[j])
                    self.V[i].add_neighbor(self.V[j])
                    self.E.add(Edge(self.V[i], self.V[j], self.is_directed))

    def find_edge(self, edge_label):
        for edge in self.E:
            v1 = edge.vertex1.label
            v2 = edge.vertex2.label
            splited = edge_label.split('_')
            if (v1 == splited[0] and v2 == splited[1]) or (v2 == splited[0] and v1 == splited[1]):
                return edge
            # if edge_label == edge.label or edge_label[::-1] == edge.label:
            #     return edge
        return None

    def find_vertex(self, vertex_label):
        vertex = self.V[int(vertex_label) - 1]
        if vertex is not None:
            return vertex
        return None


def generate_graph(n, canvas, probability, is_directed):
    if probability < 0 or probability > 1:
        probability = 0.5
    A = generate_2d_array(n)
    probability = int(probability * 100)
    for i in range(n):
        for j in range(i + 1, n):
            if i != j:
                rand = random.randint(1, 100)
                if not is_directed:
                    if rand <= probability:
                        A[i][j] = 1
                        A[j][i] = 1
                else:
                    if rand <= probability:
                        A[i][j] = 1
                        A[j][i] = 0
                    # rand = random.randint(1, 100)
                    # if rand <= probability:
                    #     A[j][i] = 1
    return Graph(A, canvas, is_directed)


def generate_2d_array(n):
    return [[0] * n for _ in range(n)]


def depth_search(graph, drawer):
    print('DFS')
    visited = [False] * len(graph.V)
    for i in range(len(graph.V)):
        if not visited[i]:
            dfs(graph, i, visited, drawer)


def dfs(graph, vertex, visited, drawer):
    matrix = graph.matrix
    visited[vertex] = True
    drawer.canvas.after(500, drawer.color_vert(vertex + 1))
    for i in range(len(matrix)):
        if not visited[i] and matrix[vertex][i] == 1:
            drawer.color_edge(str((vertex + 1)) + '_' + str(i + 1))
            dfs(graph, i, visited, drawer)


def binary_search(graph, drawer):
    visited = [False] * len(graph.V)
    queue = Queue()
    for i in range(len(graph.V)):
        if not visited[i]:
            bfs(graph, queue, drawer, visited, i)


def bfs(graph, queue, drawer, visited, vertex):
    visited[vertex] = True
    queue.put(vertex)
    drawer.canvas.after(500, drawer.color_vert(vertex + 1))
    while not queue.empty():
        v = queue.get()
        for i in range(len(graph.V)):
            if not visited[i] and graph.matrix[v][i] == 1:
                drawer.color_edge(str((v + 1)) + '_' + str(i + 1))
                drawer.canvas.after(500, drawer.color_vert(i + 1))
                queue.put(i)
                visited[i] = True
