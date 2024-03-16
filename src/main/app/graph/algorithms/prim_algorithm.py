import heapq

from src.main.app.graph.edge import Edge


def prim_algorithm(graph, drawer):
    from src.main.app.graph.algorithms.algorithms import is_graph_connected
    if not graph.is_weighted or not is_graph_connected(graph) or len(graph.V) == 0:
        return
    start_vertex = graph.V[0]
    mst = []
    edges_heap = []
    for_drawer = [start_vertex]
    visited = set()

    for edge in start_vertex.edges:
        heapq.heappush(edges_heap, (edge.weight, edge.label, edge))
    visited.add(start_vertex)

    while edges_heap:
        weight, _, edge = heapq.heappop(edges_heap)
        new_vertex = None

        if edge.vertex1 not in visited:
            new_vertex = edge.vertex1
        elif edge.vertex2 not in visited:
            new_vertex = edge.vertex2

        if new_vertex is not None:
            visited.add(new_vertex)
            for_drawer.append(edge)
            for_drawer.append(new_vertex)
            mst.append(edge)
            for next_edge in new_vertex.edges:
                if next_edge.vertex1 not in visited or next_edge.vertex2 not in visited:
                    heapq.heappush(edges_heap, (next_edge.weight, next_edge.label, next_edge))
    draw_prim(drawer, for_drawer)
    return mst


def draw_prim(drawer, for_drawer):
    delay = 500
    for element in for_drawer:
        if isinstance(element, Edge):
            drawer.highlight_edge_delay(element, delay)
        else:
            drawer.highlight_vertex_delay(element, delay)
        delay += 500
