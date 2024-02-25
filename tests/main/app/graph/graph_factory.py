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


def generate_test_empty_graph_weighted():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    return Graph([], is_weighted=True, max_width=max_width, max_height=max_height)


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


def generate_test_kruskal_graph():
    max_width = rd.randint(150, 500)
    max_height = rd.randint(150, 500)
    graph = UndirectedGraph([], is_weighted=True, max_width=max_width, max_height=max_height)
    graph_components = _create_kruskal_edges_and_vertexes()
    vertexes = graph_components['vertexes']
    edges = graph_components['edges']
    for vertex in vertexes:
        graph.add_vertex(vertex)
    for edge in edges:
        graph.add_edge(edge.vertex1, edge.vertex2, edge.directed, edge.digraph, edge.weight)
    return graph


def _create_kruskal_edges_and_vertexes():
    vertex1 = generate_test_vertex('1')
    vertex2 = generate_test_vertex('2')
    vertex3 = generate_test_vertex('3')
    vertex4 = generate_test_vertex('4')
    vertex5 = generate_test_vertex('5')
    vertex6 = generate_test_vertex('6')
    vertex7 = generate_test_vertex('7')
    vertex8 = generate_test_vertex('8')
    edge1_2 = Edge(vertex1, vertex2, False, False, 2)
    edge1_3 = Edge(vertex1, vertex3, False, False, 6)
    edge1_4 = Edge(vertex1, vertex4, False, False, 4)
    edge1_5 = Edge(vertex1, vertex5, False, False, 32)
    edge2_5 = Edge(vertex2, vertex5, False, False, 133)
    edge2_6 = Edge(vertex2, vertex6, False, False, 4)
    edge2_4 = Edge(vertex2, vertex4, False, False, 1)
    edge6_4 = Edge(vertex6, vertex4, False, False, 12)
    edge4_8 = Edge(vertex4, vertex8, False, False, 5)
    edge2_7 = Edge(vertex2, vertex7, False, False, 3)
    edge3_7 = Edge(vertex3, vertex7, False, False, 2)
    edge8_2 = Edge(vertex3, vertex7, False, False, 5)
    vertexes = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7, vertex8]
    edges = [edge1_2, edge1_3, edge1_4, edge1_5, edge1_4, edge2_5, edge2_6, edge2_4, edge6_4, edge4_8, edge2_7, edge3_7, edge8_2]
    res = {'vertexes': vertexes, 'edges': edges}
    return res
