import sqlite3

from src.main.app.data import queries
from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph
from src.main.app.utils import mapper as graph_mapper
from src.main.app.utils.logger import setup_logger

logger = setup_logger("DB")
global cursor


def start_database(url):
    global cursor
    logger.debug("Starting database...")
    connection = sqlite3.connect(url)
    cursor = connection.cursor()
    cursor.execute(queries.CREATE_GRAPH_TABLE_QUERY)
    cursor.execute(queries.CREATE_VERTEX_TABLE_QUERY)
    cursor.execute(queries.CREATE_EDGE_TABLE_QUERY)
    cursor.execute(queries.CREATE_SAVE_TABLE_QUERY)


def _save_edge(save_name, edge):
    edge_data = [save_name, edge.vertex1.label, edge.vertex2.label, edge.weight]
    cursor.execute(queries.SAVE_EDGE_QUERY, edge_data)


def _save_vertex(save_name, vertex):
    vertex_data = [save_name, vertex.label, vertex.x, vertex.y]
    cursor.execute(queries.SAVE_VERTEX_QUERY, vertex_data)


def save_graph(graph, save_name):
    logger.debug("Saving graph..., save_name=" + save_name)
    if graph is None:
        logger.debug("Graph is None")
        return
    graph_data = [save_name, graph.is_weighted, isinstance(graph, DirectedGraph), isinstance(graph, Digraph)]
    cursor.execute(queries.SAVE_GRAPH_QUERY, graph_data)
    for vertex in graph.V:
        _save_vertex(save_name, vertex)
    for edge in graph.E:
        _save_edge(save_name, edge)
    cursor.execute(queries.NEW_SAVE_QUERY, (save_name,))
    cursor.connection.commit()


def _update_vertexes(vertexes, new_save_name, old_save_name):
    vertex_data = [old_save_name]
    cursor.execute(queries.CLEAR_VERTEX_TABLE_BY_NAME_QUERY, vertex_data)
    for vertex in vertexes:
        _save_vertex(new_save_name, vertex)
    cursor.connection.commit()


def _update_edges(edges, new_save_name, old_save_name):
    edges_data = [old_save_name]
    cursor.execute(queries.CLEAR_EDGE_TABLE_BY_NAME_QUERY, edges_data)
    for edge in edges:
        _save_edge(new_save_name, edge)
    cursor.connection.commit()


def update_graph(graph, old_save_name, save_name):
    logger.debug("Update graph..., new_save_name=" + save_name)
    update_graph_data = [save_name, graph.is_weighted, isinstance(graph, DirectedGraph), isinstance(graph, Digraph), old_save_name]
    cursor.execute(queries.UPDATE_GRAPH_QUERY, update_graph_data)
    _update_vertexes(graph.V, save_name, old_save_name)
    _update_edges(graph.E, save_name, old_save_name)
    cursor.execute(queries.UPDATE_SAVE_QUERY, (save_name, old_save_name))
    cursor.connection.commit()


def delete_save(save_name):
    logger.debug("Deleting save..., save_name=" + save_name)
    cursor.execute(queries.CLEAR_VERTEX_TABLE_BY_NAME_QUERY, (save_name,))
    cursor.execute(queries.CLEAR_EDGE_TABLE_BY_NAME_QUERY, (save_name,))
    cursor.execute(queries.CLEAR_GRAPH_TABLE_BY_NAME_QUERY, (save_name,))
    cursor.execute(queries.CLEAR_SAVE_TABLE_BY_NAME_QUERY, (save_name,))
    cursor.connection.commit()


def check_if_exist(save_name):
    res = cursor.execute(queries.SELECT_SAVE_BY_SAVE_NAME_QUERY, (save_name,))
    return res.fetchone() is not None


def clear_tables():
    cursor.execute(queries.CLEAR_GRAPH_TABLE_QUERY)
    cursor.execute(queries.CLEAR_EDGE_TABLE_QUERY)
    cursor.execute(queries.CLEAR_VERTEX_TABLE_QUERY)
    cursor.execute(queries.DROP_EDGE_TABLE_QUERY)
    cursor.execute(queries.DROP_GRAPH_TABLE_QUERY)
    cursor.execute(queries.DROP_VERTEX_TABLE_QUERY)
    cursor.execute(queries.DROP_SAVE_TABLE_QUERY)
    cursor.connection.commit()


def get_vertexes(save_name):
    vertexes = []
    vertex_data_list = cursor.execute(queries.SELECT_VERTEXES_BY_SAVE_NAME_QUERY, (save_name,)).fetchall()
    for vertex_data in vertex_data_list:
        vertexes.append(graph_mapper.get_vertex_from_vertex_data(vertex_data))
    return vertexes


def get_edges(save_name, vertexes, is_directed, is_digraph):
    edges = []
    edge_data_list = cursor.execute(queries.SELECT_EDGES_BY_SAVE_NAME_QUERY, (save_name,)).fetchall()
    for edge_data in edge_data_list:
        edges.append(graph_mapper.get_edge_from_edge_data(edge_data, vertexes, is_directed, is_digraph))
    return edges


def get_graph(save_name):
    graph_data = cursor.execute(queries.SELECT_GRAPH_BY_SAVE_NAME_QUERY, (save_name,)).fetchone()
    if graph_data is None:
        logger.debug("There is no save with name=" + str(save_name))
        return
    graph = graph_mapper.get_graph_from_graph_data(graph_data)
    vertexes = get_vertexes(save_name)
    for vertex in vertexes:
        graph.add_vertex(vertex)
    edges = get_edges(save_name, vertexes, is_directed=isinstance(graph, DirectedGraph), is_digraph=isinstance(graph, Digraph))
    for edge in edges:
        graph.add_edge(edge.vertex1, edge.vertex2, is_directed=isinstance(graph, DirectedGraph), is_digraph=isinstance(graph, Digraph),
                       weight=edge.weight)
    return graph


def get_all_saves():
    saves_data = cursor.execute(queries.SELECT_ALL_SAVES).fetchall()
    saves = []
    for save_data in saves_data:
        saves.append(save_data[0])
    return saves
