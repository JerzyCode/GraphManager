from queue import Queue

from src.main.app.graph.directed_graph import DirectedGraph


def sort_edges_by_weights(edges):
    sorted_edges = sorted(edges, key=lambda edge: edge.weight)
    queue = Queue()
    for edge in sorted_edges:
        queue.put(edge)
    return queue


def binary_search(graph, drawer):
    visited = [False] * len(graph.V)
    queue = Queue()
    directed = isinstance(graph, DirectedGraph)
    result = []
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            bfs(graph, queue, drawer, visited, vertex, directed, result)
    return result


def bfs(graph, queue, drawer, visited, vertex, directed, result):
    visited[int(vertex.label) - 1] = True
    queue.put(vertex)
    drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    result.append(vertex)
    while not queue.empty():
        v = queue.get()
        for neigh in v.neighbors:
            if not visited[int(neigh.label) - 1]:
                drawer.color_edge(v.find_edge(neigh, directed))
                drawer.canvas.after(500, drawer.color_vertex(neigh, graph))
                result.append(neigh)
                queue.put(neigh)
                visited[int(neigh.label) - 1] = True


def depth_search(graph, drawer):
    print('DFS')
    directed = isinstance(graph, DirectedGraph)
    visited = [False] * len(graph.V)
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            dfs(graph, vertex, visited, drawer, directed)


def dfs(graph, vertex, visited, drawer, directed):
    visited[int(vertex.label) - 1] = True
    if drawer is not None:
        drawer.canvas.after(500, drawer.color_vertex(vertex, graph))
    for neigh in vertex.neighbors:
        if not visited[int(neigh.label) - 1]:
            if drawer is not None:
                drawer.color_edge(vertex.find_edge(neigh, directed))
            dfs(graph, neigh, visited, drawer, directed)


def is_graph_connected(graph):
    visited = [False] * len(graph.V)
    dfs(graph, graph.V[0], visited, None, None)
    for v in visited:
        if not v:
            return False

    return True


def kruskal_algorithm(graph, drawer):
    if not is_graph_connected(graph):
        print('not connected')
        return
    tree = set()
    wood = set()
    for vertex in graph.V:
        wood.add(frozenset({vertex}))
    queue = sort_edges_by_weights(graph.E)
    while len(wood) > 1:
        edge = queue.get()
        sets = different_sets(edge.vertex1, edge.vertex2, wood)
        set_a = sets[0]
        set_b = sets[1]
        if len(set_a.intersection(set_b)) == 0:
            tree.add(edge)
            drawer.canvas.after(600, drawer.color_edge_kruskal(edge, graph))
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
