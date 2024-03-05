from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.edge import Edge
from src.main.app.graph.undirected_graph import UndirectedGraph
from src.main.app.graph.vertex import Vertex


def get_vertex_from_vertex_data(vertex_data):
    vertex_label = vertex_data[1]
    vertex_x = vertex_data[2]
    vertex_y = vertex_data[3]
    return Vertex(vertex_label, x=vertex_x, y=vertex_y)


def get_edge_from_edge_data(edge_data, vertexes, is_directed, is_digraph):
    edge_vertex1_label = edge_data[1]
    edge_vertex2_label = edge_data[2]
    edge_weight = edge_data[3]
    vertex1 = find_vertex_by_label(edge_vertex1_label, vertexes)
    vertex2 = find_vertex_by_label(edge_vertex2_label, vertexes)
    return Edge(vertex1, vertex2, directed=is_directed, digraph=is_digraph, weight=int(edge_weight))


def get_graph_from_graph_data(graph_data):
    is_weighted = graph_data[1]
    is_directed = graph_data[2]
    is_digraph = graph_data[3]
    if is_digraph:
        return Digraph(is_weighted=is_weighted)
    elif is_directed:
        return DirectedGraph(is_weighted=is_weighted)
    else:
        return UndirectedGraph(is_weighted=is_weighted)


def find_vertex_by_label(vertex_label, vertexes):
    for vertex in vertexes:
        if vertex.label == vertex_label:
            return vertex
