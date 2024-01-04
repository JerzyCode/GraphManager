import random
import threading
import time
from queue import Queue, PriorityQueue

from app.graph.Edge import Edge
from app.graph.Vertex import Vertex


class Graph:
    def __init__(self, matrix, canvas, is_directed, weights=None):
        self.matrix = matrix
        self.V = set()
        self.E = set()
        self.is_weights = weights
        self.weights = weights
        self.is_directed = is_directed
        self.canvas = canvas
        self.create_vertexes()
        self.create_edges()
        print(str(self))

    def create_vertexes(self):
        size = len(self.matrix)
        self.V = list(range(size))
        for i in range(size):
            self.V[i] = Vertex(str(i + 1), self.canvas)

    def create_edges(self):
        if not self.is_directed:
            self.create_edges_undirected()
        else:
            self.create_edges_directed()

    def create_edges_undirected(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(i, size):
                self.take_edges_from_matrix(i, j)

    def create_edges_directed(self):
        size = len(self.matrix)
        for i in range(size):
            for j in range(size):
                self.take_edges_from_matrix(i, j)

    def take_edges_from_matrix(self, i, j):
        if i != j and self.matrix[i][j] == 1:
            if len(self.weights) > 0:
                edge = Edge(self.V[i], self.V[j], self.is_directed, weight=self.weights[i][j])
            else:
                edge = Edge(self.V[i], self.V[j], self.is_directed, 0)

            self.V[i].add_neighbor(self.V[j])
            self.E.add(edge)

    def find_edge(self, edge_label):
        if self.is_directed:
            for edge in self.E:
                v1 = edge.vertex1.label
                v2 = edge.vertex2.label
                if edge_label == v1 + '_' + v2:
                    return edge
        else:
            for edge in self.E:
                v1 = edge.vertex1.label
                v2 = edge.vertex2.label
                splited = edge_label.split('_')
                if (v1 == splited[0] and v2 == splited[1]) or (v2 == splited[0] and v1 == splited[1]):
                    return edge
        return None

    def find_vertex(self, vertex_label):
        vertex = self.V[int(vertex_label) - 1]
        if vertex is not None:
            return vertex
        return None

    def __str__(self):
        edges = 'edges = '
        vertexes = 'vertexes = '
        for edge in self.E:
            edges += str(edge) + ', '
        for vertex in range(len(self.V)):
            vertexes += str(self.V[vertex]) + ', '

        return vertexes + '\n' + edges


def generate_graph(n, canvas, probability, is_weighted, is_directed):
    if not is_directed:
        return generate_undirected_graph(n, canvas, probability, is_weighted)
    else:
        return generate_directed_graph(n, canvas, probability, is_weighted)


def generate_undirected_graph(n, canvas, probability, is_weighted):
    if probability < 0 or probability > 1:
        probability = 0.5
    A = generate_2d_array(n)
    probability = int(probability * 100)
    num_of_edges = 0
    weights = {}
    for i in range(n):
        for j in range(i, n):
            if i != j:
                rand = random.randint(1, 100)
                if rand <= probability:
                    num_of_edges += 1
                    A[i][j] = 1
                    A[j][i] = 1
                # if is_weighted:
                #     weights[i][j] = rand
    return Graph(A, canvas, False, weights)


def generate_directed_graph(n, canvas, probability, is_weighted):
    if probability < 0 or probability > 1:
        probability = 0.5
    A = generate_2d_array(n)
    probability = int(probability * 40)
    num_of_edges = 0
    weights = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                rand = random.randint(1, 100)
                if rand <= probability:
                    num_of_edges += 1
                    A[i][j] = 1
    return Graph(A, canvas, True, weights)


def generate_2d_array(n):
    return [[0] * n for _ in range(n)]


def depth_search(graph, drawer):
    print('DFS')
    visited = [False] * len(graph.V)
    for i in range(len(graph.V)):
        if not visited[i]:
            dfs(graph, i, visited, drawer)


def dfs(graph, vertex, visited, drawer):
    print('DFS')
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
