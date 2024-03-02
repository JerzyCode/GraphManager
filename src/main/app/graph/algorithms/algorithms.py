from queue import Queue

from src.main.app.graph.algorithms.dijkstra_algorithm import dijkstra_algorithm
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.utils.constants import COLOR_DELAY


def _sort_edges_by_weights(edges):
    sorted_edges = sorted(edges, key=lambda e: e.weight)
    queue = Queue()
    for edge in sorted_edges:
        queue.put(edge)
    return queue


def binary_search(graph, drawer):
    visited = {}
    elements_to_color = list()
    delay = 0
    for v in graph.V:
        visited[v] = False
    queue = Queue()
    directed = isinstance(graph, DirectedGraph)
    for vertex in graph.V:
        if not visited[vertex]:
            bfs(queue, visited, vertex, directed, elements_to_color)
    for element in elements_to_color:
        drawer.color_element(element, delay)
        delay += COLOR_DELAY
    return elements_to_color


def bfs(queue, visited, vertex, directed, elements_to_color):
    visited[vertex] = True
    queue.put(vertex)
    elements_to_color.append(vertex)
    while not queue.empty():
        v = queue.get()
        for neigh in v.neighbors:
            if not visited[neigh]:
                elements_to_color.append(v.find_edge(neigh, directed))
                elements_to_color.append(neigh)
                queue.put(neigh)
                visited[neigh] = True


def depth_search(graph, drawer):
    directed = isinstance(graph, DirectedGraph)
    visited = {}
    elements_to_color = list()
    delay = 0
    for v in graph.V:
        visited[v] = False
    for vertex in graph.V:
        if not visited[vertex]:
            dfs(graph, vertex, visited, drawer, directed, elements_to_color)
    for element in elements_to_color:
        drawer.color_element(element, delay)
        delay += COLOR_DELAY
    return elements_to_color


def dfs(graph, vertex, visited, drawer, directed, elements_to_color):
    visited[vertex] = True
    elements_to_color.append(vertex)
    for neigh in vertex.neighbors:
        if not visited[neigh]:
            elements_to_color.append(vertex.find_edge(neigh, directed))
            dfs(graph, neigh, visited, drawer, directed, elements_to_color)


def is_graph_connected(graph):
    result = []
    visited = [False] * len(graph.V)
    dfs(graph, graph.V[0], visited, None, None, result)
    for v in visited:
        if not v:
            return False
    return True


def kruskal_algorithm(graph, drawer):
    if not graph.is_weighted:
        return
    tree = set()
    wood = set()
    delay = 0
    for vertex in graph.V:
        wood.add(frozenset({vertex}))
    queue = _sort_edges_by_weights(graph.E)
    while len(wood) > 1:
        edge = queue.get()
        sets = different_sets(edge.vertex1, edge.vertex2, wood)
        set_a = sets[0]
        set_b = sets[1]
        if len(set_a.intersection(set_b)) == 0:
            tree.add(edge)
            drawer.highlight_edge_kruskal(edge, delay)
            delay += 500
            wood.remove(set_a)
            wood.remove(set_b)
            wood.add(set_a.union(set_b))
    return tree


def different_sets(vertex1, vertex2, wood):
    set_a = set()
    set_b = set()
    for set1 in wood:
        if vertex1 in set1:
            set_a = set1
            break
    for set2 in wood:
        if vertex2 in set2:
            set_b = set2
            break
    return [set_a, set_b]


def run_dijkstra_algorithm(graph, start, drawer):
    dijkstra_algorithm(graph, start, drawer)
