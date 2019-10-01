import pytest
import networkx as nx
import morphological_analysis


def test_co_occurrence_network():
    expected = []
    words = {}
    graph = nx.Graph()
    morphological_analysis.co_occurrence_network(words, graph)
    graph.nodes() == expected


def test_add_node_and_edge():
    expected = []
    words = {}
    graph = nx.Graph()
    morphological_analysis._add_node_and_edge(words, graph)
    graph.nodes() == expected


def _calc_npmi():
    expected = []
    words = {}
    graph = nx.Graph()
    morphological_analysis._calc_npmi(words, graph)
    graph.nodes() == expected
