CREATE_SAVE_TABLE_QUERY = '''CREATE TABLE if not exists save_table 
(
 save_name TEXT UNIQUE
 )'''

CREATE_GRAPH_TABLE_QUERY = '''CREATE TABLE if not exists graph_table 
(
 save_name TEXT UNIQUE,
 weighted BOOLEAN,
 directed BOOLEAN,
 digraph BOOLEAN)'''

CREATE_VERTEX_TABLE_QUERY = '''CREATE TABLE if not exists vertex_table (
  save_name TEXT,
  label TEXT,
  x REAL,
  y REAL,
  FOREIGN KEY (save_name) REFERENCES graph_table (save_name)
)'''

CREATE_EDGE_TABLE_QUERY = '''CREATE TABLE if not exists edge_table (
  save_name TEXT,
  vertex1_label TEXT,
  vertex2_label TEXT,
  weight REAL,
  FOREIGN KEY (save_name) REFERENCES graph_table (save_name),
  FOREIGN KEY (vertex1_label) REFERENCES vertex_table (label),
  FOREIGN KEY (vertex2_label) REFERENCES vertex_table (label)
)'''

NEW_SAVE_QUERY = '''
INSERT INTO save_table (save_name) VALUES (?)'''

SAVE_EDGE_QUERY = '''
INSERT INTO edge_table (save_name, vertex1_label, vertex2_label, weight) 
VALUES (?, ?, ?, ?)'''

SAVE_VERTEX_QUERY = '''
INSERT INTO vertex_table (save_name,label, x, y) 
VALUES (?, ?, ?, ?)'''

SAVE_GRAPH_QUERY = '''
INSERT INTO graph_table (save_name, weighted, directed, digraph) 
VALUES (?, ?, ?, ?)'''

DELETE_VERTEXES_BY_GRAPH_QUERY = '''
DELETE FROM vertex_table WHERE save_name = (?)
'''

DELETE_EDGES_BY_GRAPH_QUERY = '''
DELETE FROM edge_table WHERE save_name = (?)
'''

UPDATE_SAVE_QUERY = '''
UPDATE save_table
SET
  save_name = ?
WHERE save_name = ?;
'''

UPDATE_GRAPH_QUERY = '''
UPDATE graph_table
SET
  save_name = ?,
  weighted = ?,
  directed = ?,
  digraph = ?
WHERE save_name = ?;'''

UPDATE_VERTEX_QUERY = '''
UPDATE vertex_table
SET
  save_name = ?,
  x = ?,
  y = ?
WHERE save_name = ?;'''

UPDATE_EDGE_QUERY = '''
UPDATE edge_table
SET
  save_name = ?,
WHERE save_name = ?;'''

CLEAR_EDGE_TABLE_BY_NAME_QUERY = 'DELETE FROM edge_table WHERE save_name = ?'
CLEAR_VERTEX_TABLE_BY_NAME_QUERY = 'DELETE FROM vertex_table WHERE save_name = ?'
CLEAR_GRAPH_TABLE_BY_NAME_QUERY = 'DELETE FROM graph_table WHERE save_name = ?'

CLEAR_GRAPH_TABLE_QUERY = 'DELETE FROM graph_table'
CLEAR_VERTEX_TABLE_QUERY = 'DELETE FROM vertex_table'
CLEAR_EDGE_TABLE_QUERY = 'DELETE FROM edge_table'

DROP_GRAPH_TABLE_QUERY = 'DROP TABLE if exists graph_table'
DROP_VERTEX_TABLE_QUERY = 'DROP TABLE if exists vertex_table'
DROP_EDGE_TABLE_QUERY = 'DROP TABLE if exists edge_table'
DROP_SAVE_TABLE_QUERY = 'DROP TABLE if exists save_table'

SELECT_GRAPH_QUERY = "SELECT 1 FROM graph_table WHERE save_name = (?);"
