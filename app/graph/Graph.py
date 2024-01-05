import random
import threading
import time
from queue import Queue, PriorityQueue

from app.graph.Edge import Edge
from app.graph.Vertex import Vertex


class Graph:
    def __init__(self, matrix, is_directed, weights=None, max_width=None, max_height=None):
        self.matrix = matrix
        self.V = set()
        self.E = set()
        self.weights = weights
        self.is_directed = is_directed
        self.create_vertexes(max_width, max_height)
        self.create_edges()
        print(self.__str__())
        for vertex in self.V:
            string = 'vertex:' + vertex.label + ": "
            string += 'edges: '
            for ede in vertex.edges:
                string += str(ede) + ', '
            string += 'neighbors: '
            for neigh in vertex.neighbors:
                string += str(neigh) + ', '
            print(string)

        # TODO NIE DZIALA KOLOROWANIE/BFS I DFS

    def create_vertexes(self, max_width, max_height):
        size = len(self.matrix)
        self.V = list(range(size))
        for i in range(size):
            self.V[i] = Vertex(str(i + 1), max_width, max_height)

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

            if self.is_directed:
                self.V[i].add_neighbor(self.V[j], edge)
            else:
                self.V[i].add_neighbor(self.V[j], edge)
                self.V[j].add_neighbor(self.V[i], edge)
            self.E.add(edge)

    def __str__(self):
        edges = 'edges = '
        vertexes = 'vertexes = '
        for edge in self.E:
            edges += str(edge) + ', '
        for vertex in range(len(self.V)):
            vertexes += str(self.V[vertex]) + ', '

        return vertexes + '\n' + edges


def generate_graph(n, probability, is_weighted, is_directed, max_width, max_height):
    if not is_directed:
        return generate_undirected_graph(n, probability, is_weighted, max_width, max_height)
    else:
        return generate_directed_graph(n, probability, is_weighted, max_width, max_height)


def generate_undirected_graph(n, probability, is_weighted, max_width, max_height):
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
    return Graph(A, False, weights, max_width, max_height)


def generate_directed_graph(n, probability, is_weighted, max_width, max_height):
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
    return Graph(A, True, weights, max_width, max_height)


def generate_2d_array(n):
    return [[0] * n for _ in range(n)]


def binary_search(graph, drawer):
    visited = [False] * len(graph.V)
    queue = Queue()
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            bfs(graph, queue, drawer, visited, vertex)


def bfs(graph, queue, drawer, visited, vertex):
    visited[int(vertex.label) - 1] = True
    queue.put(vertex)
    drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    while not queue.empty():
        v = queue.get()
        print(str(v))
        for neigh in v.neighbors:
            if not visited[int(neigh.label) - 1]:
                drawer.color_edge(v.find_edge(neigh, graph.is_directed))
                drawer.canvas.after(500, drawer.color_vertex(neigh, graph))
                queue.put(neigh)
                visited[int(neigh.label) - 1] = True


def depth_search(graph, drawer):
    print('DFS')
    visited = [False] * len(graph.V)
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            dfs(graph, vertex, visited, drawer)


def dfs(graph, vertex, visited, drawer):
    visited[int(vertex.label) - 1] = True
    print(vertex)
    drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    for neigh in vertex.neighbors:
        if not visited[int(neigh.label) - 1]:
            drawer.color_edge(vertex.find_edge(neigh, graph.is_directed))
            dfs(graph, neigh, visited, drawer)
