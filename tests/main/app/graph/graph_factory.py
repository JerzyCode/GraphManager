import random as rd

from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.edge import Edge
from src.main.app.graph.graph import Graph
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.graph.vertex import Vertex

undirected_graph_matrix_bfs = [
    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 1, 0, 0, 0]]

directed_graph_matrix_bfs = [
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]

graph_not_connected_matrix = [
    [0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0]
]


def generate_test_vertex(label: str):
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return Vertex(label, max_width, max_height)


def generate_test_empty_undirected_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return UndirectedGraph([], is_weighted=False, max_width=max_width, max_height=max_height)


def generate_test_empty_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return Graph([], is_weighted=False, max_width=max_width, max_height=max_height)


def generate_test_two_vertex_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    graph = Graph([], is_weighted=False, max_width=max_width, max_height=max_height)
    vertex1 = generate_test_vertex("1")
    vertex2 = generate_test_vertex("2")
    edge = Edge(vertex1, vertex2, directed=False, digraph=False, weight=None)
    graph.E.add(edge)
    graph.V.append(vertex1)
    graph.V.append(vertex2)
    return graph


def generate_test_two_vertex_directed_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    graph = DirectedGraph([], is_weighted=False, max_width=max_width, max_height=max_height)
    vertex1 = generate_test_vertex("1")
    vertex2 = generate_test_vertex("2")
    edge = Edge(vertex1, vertex2, directed=True, digraph=False, weight=None)
    graph.E.add(edge)
    graph.V.append(vertex1)
    graph.V.append(vertex2)
    return graph


def generate_test_undirected_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return UndirectedGraph(undirected_graph_matrix_bfs, is_weighted=False, max_width=max_width, max_height=max_height)


def generate_test_directed_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return DirectedGraph(directed_graph_matrix_bfs, is_weighted=False, max_width=max_width, max_height=max_height)


def generate_test_no_connected_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return UndirectedGraph(graph_not_connected_matrix, is_weighted=False, max_width=max_width, max_height=max_height)
