from pytest import mark
import networkx as nx
from src.co_occurrence_network import (co_occurrence_network,
                                       _add_node_and_edge,
                                       _calc_npmi,
                                       _create_graph_in_CON)
from src.extract_text import extract_text
from src.morphological_analysis import morphological_analysis


# def test_co_occurrence_network(create_jsonfiles):
#     # expected =
#     graph = nx.Graph()
#     graph = co_occurrence_network(create_jsonfiles, graph)
#     assert graph.nodes() == expected


def _add_nodes(jsonfiles, graph: nx.Graph) -> nx.Graph:
    for filename in jsonfiles:
        text = extract_text(filename)
        print(text)
        words = morphological_analysis(text)
        print(words)
        _add_node_and_edge(words, graph)
    return graph


def test_add_nodes(create_jsonfiles):
    expected = ["野球", "好き", "嫌い"]
    graph = nx.Graph()
    _add_nodes(create_jsonfiles, graph)
    for v in graph.nodes():
        if v not in expected:
            assert False, "含まれてない値: {0}".format(v)
    assert False


# def test_add_nodes2(create_jsonfiles):
#     graph = nx.Graph()
#     _add_nodes(create_jsonfiles, graph)
#     expected = {("野球", "好き")}
#     for u, v in graph.edges():
#         if (u, v) in expected:
#             assert True
#         else:
#             assert False, "エラーだった値: {0}, {1}".format(u, v)
