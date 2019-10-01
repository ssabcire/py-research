import itertools
import networkx as nx
from .const import JSONFILES
from .extract_text import extract_text
from .morphological_analysis import morphological_analysis
# import as dp


def co_occurrence_network(jsonfiles, graph: nx.Graph) -> nx.Graph:
    '''
    共起ネットワークを作成
    '''
    for filename in jsonfiles:
        text = extract_text(filename)
        words = morphological_analysis(text)
        _add_node_and_edge(words, graph)
    _calc_npmi(graph)
    return graph


def _add_node_and_edge(words: set, graph: nx.Graph):
    '''
    Graphにnodeとedgeを付与
    param words: 1ツイートに含まれる単語
    '''
    for v in words:
        if v in graph.nodes():
            graph.nodes[v]["count"] += 1
        else:
            graph.add_node(v, count=1)
    for u, v in itertools.combinations(words, 2):
        if graph.has_edge(u, v):
            graph[u][v]['count'] += 1
        else:
            graph.add_edge(u, v, count=1)


def _calc_npmi(graph: nx.Graph):
    '''
    共起の強さを測るため、相互情報量を求める
    '''
    total_num_of_tweet = len(JSONFILES)
    for v in graph.nodes():
        graph.nodes[v]['probability'] = \
            graph.nodes[v]['count'] / total_num_of_tweet
    for u, v in graph.edges():
        graph[u][v]['probability'] = graph[u][v]['count'] / total_num_of_tweet
    # PMI計算
    for u, v in graph.edges():
        graph[u][v]['npmi'] = dp.npmi(
            graph[u][v]['probability'],
            graph.nodes[u]['probability'],
            graph.nodes[v]['probability']
        )


def _create_graph_in_CON():
    graph = nx.Graph()
    graph = co_occurrence_network(JSONFILES, graph)


if __name__ == '__main__':
    _create_graph_in_CON()
