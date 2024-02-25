from queue import Queue

from src.main.app.graph.directed_graph import DirectedGraph


def _sort_edges_by_weights(edges):
    sorted_edges = sorted(edges, key=lambda e: e.weight)
    queue = Queue()
    for edge in sorted_edges:
        queue.put(edge)
    return queue


def binary_search(graph, drawer):
    visited = {}
    for v in graph.V:
        visited[v] = False
    queue = Queue()
    directed = isinstance(graph, DirectedGraph)
    result = []
    for vertex in graph.V:
        if not visited[vertex]:
            bfs(queue, drawer, visited, vertex, directed, result)
    return result


def bfs(queue, drawer, visited, vertex, directed, result):
    delay = 0
    visited[vertex] = True
    queue.put(vertex)
    drawer.highlight_vertex_delay(vertex, delay)
    result.append(vertex)
    while not queue.empty():
        v = queue.get()
        for neigh in v.neighbors:
            if not visited[neigh]:
                drawer.highlight_edge_delay(v.find_edge(neigh, directed), delay)
                drawer.highlight_vertex_delay(neigh, delay)
                delay += 500
                result.append(neigh)
                queue.put(neigh)
                visited[neigh] = True


def depth_search(graph, drawer):
    directed = isinstance(graph, DirectedGraph)
    visited = {}
    result = []
    for v in graph.V:
        visited[v] = False
    for vertex in graph.V:
        if not visited[vertex]:
            dfs(graph, vertex, visited, drawer, directed, 0, result)
    return result


def dfs(graph, vertex, visited, drawer, directed, delay, result):
    visited[vertex] = True
    result.append(vertex)
    if drawer is not None:
        drawer.highlight_vertex_delay(vertex, delay)
    for neigh in vertex.neighbors:
        if not visited[neigh]:
            if drawer is not None:
                drawer.highlight_edge_delay(vertex.find_edge(neigh, directed), delay)
                delay += 500
            dfs(graph, neigh, visited, drawer, directed, delay, result)


def is_graph_connected(graph):
    result = []
    visited = [False] * len(graph.V)
    dfs(graph, graph.V[0], visited, None, None, 0, result)
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
