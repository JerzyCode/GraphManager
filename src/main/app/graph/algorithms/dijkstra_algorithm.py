import sys

from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.graph.edge import Edge
from src.main.app.graph.vertex import Vertex

max_size = sys.maxsize / 2


def _is_valid_graph(graph):
    if not graph.is_weighted or len(graph.V) == 0:
        return False
    for edge in graph.E:
        if edge.weight < 0:
            return False
    return True


def _differ_in_weights(graph):
    edge_weight = {}
    for edge in graph.E:
        if edge.weight not in edge_weight.values():
            edge_weight[edge] = edge.weight
        else:
            edge_weight[edge] = edge.weight + 0.01
    return edge_weight


def _minimum_distance_vertex(graph, distance, done_vertexes, start):
    min_distance = 1e7
    min_vertex = None
    for vertex in graph.V:
        if distance[vertex] < min_distance and not done_vertexes[vertex]:
            min_distance = distance[vertex]
            min_vertex = vertex
    if min_vertex is None:
        return start
    return min_vertex


def _draw_dijkstra(drawer, for_drawer):
    delay = 0
    for element in for_drawer:
        if isinstance(element[0], Vertex):
            vertex = element[0]
            if element[2] == 'set_vertex':
                drawer.highlight_vertex_delay(vertex, delay)
                drawer.draw_dijkstra_distance(vertex, element[1], delay)
            else:
                drawer.draw_dijkstra_distance(vertex, element[1], delay)
                delay += 500
        if isinstance(element[0], Edge):
            edge = element[0]
            if element[1] == 'color':
                drawer.highlight_edge_delay(edge, delay)
            else:
                drawer.refresh_edge_delay(edge, delay)
            delay += 500


def dijkstra_algorithm(graph, start, drawer):
    if not _is_valid_graph(graph):
        return
    weights = _differ_in_weights(graph)
    for_drawer = []
    prev_edge = {}
    done_vertexes = {}
    distance = {start: 0}
    for_drawer.append([start, distance[start], None])
    for vertex in graph.V:
        done_vertexes[vertex] = False
        if vertex != start:
            distance[vertex] = max_size
            prev_edge[vertex] = None
            for_drawer.append([vertex, distance[vertex], None])

    for count in range(len(graph.V)):
        min_dist_vertex = _minimum_distance_vertex(graph, distance, done_vertexes, start)
        done_vertexes[min_dist_vertex] = True
        for_drawer.append([min_dist_vertex, distance[min_dist_vertex], 'set_vertex'])
        for neigh in min_dist_vertex.neighbors:
            edge = min_dist_vertex.find_edge(neigh, isinstance(graph, DirectedGraph))
            if edge is not None and distance[neigh] > distance[min_dist_vertex] + weights[edge]:
                distance[neigh] = distance[min_dist_vertex] + weights[edge]
                for_drawer.append([prev_edge[neigh], 'uncolor', None])
                prev_edge[neigh] = edge
                for_drawer.append([prev_edge[neigh], 'color', None])
                for_drawer.append([neigh, distance[neigh], None])
    _draw_dijkstra(drawer, for_drawer)

    return {'draws': for_drawer, 'paths': prev_edge, 'weights': distance}
