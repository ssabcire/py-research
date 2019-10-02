from __future__ import absolute_import, print_function, division, unicode_literals

import networkx

if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
    neighbors = networkx.Graph.neighbors
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter
    neighbors = networkx.Graph.neighbors_iter


def is_identical_graph(g, h):
    """
    decide whether given two graph, g and h, are identical graph.
    :param g: graph
    :param h: graph
    :return: True iff g and h are identical
    """

    if g.number_of_nodes() != h.number_of_nodes() or g.number_of_edges() != h.number_of_edges():
        return False

    for v in nodes(g):
        if (not h.has_node(v)) or g.degree(v) != h.degree(v):
            return False

    for v in nodes(g):
        for u in neighbors(g, v):
            if not h.has_edge(u, v):
                return False

    return True


is_identical_graph.__annotations__ = {'g': networkx.Graph, 'h': networkx.Graph,
                                      'return': bool}
