import sqlite3
from unittest import TestCase

import src.main.app.data.database as sut
import tests.main.app.graph.graph_factory as factory
from src.main.app.data import queries
from src.main.app.graph.digraph import Digraph
from src.main.app.graph.directed_graph import DirectedGraph


class DatabaseTest(TestCase):

    def setUp(self):
        self.connection = sqlite3.connect('../database/test_database.db')
        self.cursor = self.connection.cursor()
        sut.cursor = self.cursor

    def tearDown(self):
        self.clear_test_db()
        self.connection.close()

    def check_if_table_exists(self, table_name):
        self.cursor.execute(queries.CHECK_IF_TABLE_EXISTS_BY_NAME, (table_name,))
        return self.cursor.fetchone()

    def drop_test_db(self):
        self.cursor.execute(queries.DROP_EDGE_TABLE_QUERY)
        self.cursor.execute(queries.DROP_GRAPH_TABLE_QUERY)
        self.cursor.execute(queries.DROP_VERTEX_TABLE_QUERY)
        self.cursor.execute(queries.DROP_SAVE_TABLE_QUERY)
        self.cursor.connection.commit()

    def clear_test_db(self):
        self.cursor.execute(queries.CLEAR_EDGE_TABLE_QUERY)
        self.cursor.execute(queries.CLEAR_GRAPH_TABLE_QUERY)
        self.cursor.execute(queries.CLEAR_VERTEX_TABLE_QUERY)
        self.cursor.execute(queries.CLEAR_SAVE_TABLE_QUERY)
        self.cursor.connection.commit()

    def test_start_database(self):
        # given
        # when
        sut.start_database('../database/test_database.db')
        # then
        self.assertIsNotNone(self.check_if_table_exists('edge_table'))
        self.assertIsNotNone(self.check_if_table_exists('graph_table'))
        self.assertIsNotNone(self.check_if_table_exists('save_table'))
        self.assertIsNotNone(self.check_if_table_exists('vertex_table'))

    def test_save_graph(self):
        # given
        save_name = 'test_save_1'
        graph = factory.generate_test_weighted_directed_graph()
        # when
        sut.save_graph(graph, save_name)
        # then
        edge_count = self.cursor.execute(queries.COUNT_EDGES_QUERY, (save_name,)).fetchone()[0]
        save_count = self.cursor.execute(queries.COUNT_SAVES_QUERY, (save_name,)).fetchone()[0]
        vertex_count = self.cursor.execute(queries.COUNT_VERTEXES_QUERY, (save_name,)).fetchone()[0]
        graph_count = self.cursor.execute(queries.COUNT_GRAPHS_QUERY, (save_name,)).fetchone()[0]
        db_graph_directed = self.cursor.execute(queries.SELECT_DIRECTED_QUERY, (save_name,)).fetchone()[0]
        db_graph_digraph = self.cursor.execute(queries.SELECT_DIGRAPH_QUERY, (save_name,)).fetchone()[0]
        db_graph_weighted = self.cursor.execute(queries.SELECT_WEIGHTED_QUERY, (save_name,)).fetchone()[0]
        saved_name = self.cursor.execute(queries.SELECT_SAVE_BY_NAME_QUERY, (save_name,)).fetchone()[0]
        self.assertEqual(len(graph.E), edge_count)
        self.assertEqual(len(graph.V), vertex_count)
        self.assertEqual(saved_name, save_name)
        self.assertEqual(1, save_count)
        self.assertEqual(1, graph_count)
        self.assertEqual(db_graph_directed, isinstance(graph, DirectedGraph))
        self.assertEqual(db_graph_digraph, isinstance(graph, Digraph))
        self.assertEqual(db_graph_weighted, graph.is_weighted)

    def test_upgrade_graph(self):
        # given
        save_name = 'test_save_1'
        new_save_name = 'test_save_2'
        graph = factory.generate_test_weighted_directed_graph()
        sut.save_graph(graph, save_name)
        graph.delete_vertex(graph.V[2])
        # when
        sut.update_graph(graph, save_name, new_save_name)
        # then
        edge_count = self.cursor.execute(queries.COUNT_EDGES_QUERY, (new_save_name,)).fetchone()[0]
        save_count = self.cursor.execute(queries.COUNT_SAVES_QUERY, (new_save_name,)).fetchone()[0]
        vertex_count = self.cursor.execute(queries.COUNT_VERTEXES_QUERY, (new_save_name,)).fetchone()[0]
        graph_count = self.cursor.execute(queries.COUNT_GRAPHS_QUERY, (new_save_name,)).fetchone()[0]
        db_graph_directed = self.cursor.execute(queries.SELECT_DIRECTED_QUERY, (new_save_name,)).fetchone()[0]
        db_graph_digraph = self.cursor.execute(queries.SELECT_DIGRAPH_QUERY, (new_save_name,)).fetchone()[0]
        db_graph_weighted = self.cursor.execute(queries.SELECT_WEIGHTED_QUERY, (new_save_name,)).fetchone()[0]
        saved_name = self.cursor.execute(queries.SELECT_SAVE_BY_NAME_QUERY, (new_save_name,)).fetchone()[0]
        self.assertEqual(saved_name, new_save_name)
        self.assertEqual(len(graph.E), edge_count)
        self.assertEqual(len(graph.V), vertex_count)
        self.assertEqual(1, save_count)
        self.assertEqual(1, graph_count)
        self.assertEqual(db_graph_directed, isinstance(graph, DirectedGraph))
        self.assertEqual(db_graph_digraph, isinstance(graph, Digraph))
        self.assertEqual(db_graph_weighted, graph.is_weighted)
