import sys
from queue import Queue

from src.main.app.utils.algorithms import kruskal_algorithm


def ex_4(graph, start_label, drawer, max_count):
    tree = set()
    queue = Queue()
    counter = 0
    cost = {}
    prev = {}
    start = None
    for vertex in graph.V:
        if vertex.label == start_label:
            start = vertex
            break

    print('start is = ', str(start))

    # TODO NIE DZIALA ALGORYTM PRIMA, TRZEBA NAD NIM POMYŚLEĆ
    # trzeba zrobic tak ze brane najpierw sa wierzcholki ktore maja namniejszy koszt

    for vertex in graph.V:
        if vertex != start:
            if vertex in start.neighbors:
                edge = vertex.find_edge(start, is_directed=False)
                cost[vertex.label] = edge.weight
                prev[vertex.label] = start
            else:
                cost[vertex.label] = sys.maxsize
                prev[vertex.label] = None
    queue = sort_vertexes_by_costs(graph.V, cost)
    while queue.not_empty and counter < max_count:
        vertex = queue.get()
        if prev[vertex.label] is not None:
            print('shop in = ', str(prev[vertex.label]))
            edge_to_add = prev[vertex.label].find_edge(vertex, is_directed=False)
            tree.add(edge_to_add)
            drawer.canvas.after(600, drawer.color_edge_kruskal(edge_to_add, graph))
            counter = counter + 1
            for neighbor in vertex.neighbors:
                edge = vertex.find_edge(neighbor, is_directed=False)
                if neighbor in queue.queue and cost[neighbor.label] > edge.weight:
                    cost[neighbor.label] = edge.weight
                    prev[neighbor.label] = vertex


def sort_vertexes_by_costs(vertexes, costs):
    vertexes = sorted(vertexes, key=lambda vertex: costs[vertex.label])
    queue = Queue()
    for vertex in vertexes:
        queue.put(vertex)
    return queue


def ex_4(graph, drawer):
    tree = kruskal_algorithm(graph, drawer)
    counter = 0
    edges = tree
    visited = [False] * len(graph)
    for vertex in graph.V:
        if not visited[int(vertex.label) - 1]:
            counter = counter + 1
            dfs(edges, vertex, visited, drawer, False)

def dfs(edges, vertex, visited, drawer, directed):
    visited[int(vertex.label) - 1] = True
    # if drawer is not None:
        # drawer.canvas.after(500, drawer.color_vertex(vertex, edges))
    for neigh in vertex.neighbors:
        if not visited[int(neigh.label) - 1]:
            if drawer is not None:
                drawer.color_edge(vertex.find_edge(neigh, directed))
            dfs(edges, neigh, visited, drawer, directed)