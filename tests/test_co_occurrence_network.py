import pytest
import networkx as nx
from src.co_occurrence_network import (co_occurrence_network,
                                       _add_node_and_edge,
                                       _calc_npmi,
                                       _create_graph_in_CON)


def test_co_occurrence_network(create_jsonfile):
    graph = nx.Graph()
    graph = co_occurrence_network([create_jsonfile], graph)
    assert graph.nodes() == expected


def test_add_node_and_edge():
    words = {}
    expected = 1
    graph = nx.Graph()
    morphological_analysis._add_node_and_edge(words, graph)
    assert graph.nodes["とある単語v"]["count"] == expected


def test_calc_npmi():
    graph = nx.Graph()
    morphological_analysis._calc_npmi(graph)
    assert graph.nodes() == expected
