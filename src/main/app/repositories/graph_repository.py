graphs = []


def create_graph(graph, save_name):
    graphs.append({save_name: graph})


def delete_graph_by_save_name(save_name):
    global graphs
    graphs = [graph for graph in graphs if save_name not in graph]


def update_graph_save(old_save_name, new_save_name, new_graph):
    global graphs
    for i, graph in enumerate(graphs):
        if old_save_name in graph:
            graphs[i] = {new_save_name: new_graph}
            break


def is_save_name_in_repository(save_name):
    for graph in graphs:
        if save_name in graph:
            return True
    return False


def get_save_names():
    keys = []
    for graph in graphs:
        keys.extend(graph.keys())
    return keys


def get_graph_by_save_name(save_name):
    for graph in graphs:
        if save_name in graph:
            return graph[save_name]
    return None
