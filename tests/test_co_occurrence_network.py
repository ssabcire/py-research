from pytest import mark
import networkx as nx
from src.co_occurrence_network import (co_occurrence_network,
                                       _add_node_and_edge,
                                       _calc_npmi,
                                       _create_graph_in_CON)


def test_co_occurrence_network(create_jsonfiles):
    graph = nx.Graph()
    graph = co_occurrence_network(create_jsonfiles, graph)
    assert graph.nodes() == expected
