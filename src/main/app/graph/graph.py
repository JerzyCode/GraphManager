from abc import abstractmethod
from queue import Queue

from src.main.app.graph.vertex import Vertex


class Graph:
    def __init__(self, matrix, max_width=None, max_height=None):
        self.matrix = matrix
        self.V = []
        self.E = set()
        self._create_vertexes(max_width, max_height)

    def _create_vertexes(self, max_width, max_height):
        size = len(self.matrix)
        for i in range(size):
            self.V.append(Vertex(str(i + 1), max_width, max_height))

    @abstractmethod
    def __create_edges__(self):
        pass

    def __str__(self):
        string = ''
        for vertex in self.V:
            string = 'vertex:' + vertex.label + ": "
            string += 'edges: '
            for ede in vertex.edges:
                string += str(ede) + ', '
            string += 'neighbors: '
            for neigh in vertex.neighbors:
                string += str(neigh) + ', '
            print(string)
        return string


def binary_search(graph, drawer):
    from src.main.app.graph.directed_graph import DirectedGraph
    visited = [False] * len(graph.V)
    queue = Queue()
    directed = isinstance(graph, DirectedGraph)
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            bfs(graph, queue, drawer, visited, vertex, directed)


def bfs(graph, queue, drawer, visited, vertex, directed):
    visited[int(vertex.label) - 1] = True
    queue.put(vertex)
    drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    while not queue.empty():
        v = queue.get()
        for neigh in v.neighbors:
            if not visited[int(neigh.label) - 1]:
                drawer.color_edge(v.find_edge(neigh, directed))
                drawer.canvas.after(500, drawer.color_vertex(neigh, graph))
                queue.put(neigh)
                visited[int(neigh.label) - 1] = True


def depth_search(graph, drawer):
    from src.main.app.graph.directed_graph import DirectedGraph
    print('DFS')
    directed = isinstance(graph, DirectedGraph)
    visited = [False] * len(graph.V)
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            dfs(graph, vertex, visited, drawer, directed)


def dfs(graph, vertex, visited, drawer, directed):
    visited[int(vertex.label) - 1] = True
    drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    for neigh in vertex.neighbors:
        if not visited[int(neigh.label) - 1]:
            drawer.color_edge(vertex.find_edge(neigh, directed))
            dfs(graph, neigh, visited, drawer, directed)
