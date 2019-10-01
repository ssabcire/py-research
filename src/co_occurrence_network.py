import itertools
import networkx as nx
from .const import JSONFILES
from .extract_text import extract_text
from .morphological_analysis import morphological_analysis
# import as dp


def co_occurrence_network(words: set, graph: nx.Graph) -> nx.Graph:
    '''
    共起ネットワークを作成
    '''
    _add_node_and_edge(words, graph)
    _calc_npmi(graph)
    return graph


def _add_node_and_edge(words: set, graph: nx.Graph):
    # 疑問箇所。とくにnodeとedge
    '''
    Graphにnodeとedgeを付与
    '''
    graph.add_nodes_from(words, count=1)
    graph.add_nodes_from(
        # タプルに問題ありそう
        [(node, {'count': attr}) for (node, attr) in words.items()]
    )
    for u, v in itertools.combinations(words, 2):
        if graph.has_edge(u, v):
            graph[u][v]['count'] += 1
        else:
            graph.add_edge(u, v, count=1)


def _calc_npmi(graph: nx.Graph):
    '''
    共起の強さを測るため、相互情報量を求める。
    '''
    node_sum = 0    # node_sum違う恐れあり
    for v in graph.nodes():
        node_sum += graph.nodes[v]['count']
    for v in graph.nodes():
        graph.nodes[v]['probability'] = graph.nodes[v]['count'] / node_sum

    edge_sum = 0
    for u, v in graph.edges():      # edge_sum違う恐れあり
        edge_sum += graph[u][v]['count']
    for u, v in graph.edges():
        graph[u][v]['probability'] = graph[u][v]['count'] / edge_sum

    for u, v in graph.edges():
        graph[u][v]['npmi'] = dp.npmi(
            graph[u][v]['probability'],
            graph.nodes[u]['probability'],
            graph.nodes[v]['probability']
        )


def _create_graph_in_CON():
    texts = extract_text(JSONFILES)
    # 重複気にするならlist, 単語の出現回数を求めたいならdict
    words = set()
    for text in texts:
        words = words | morphological_analysis(text)
    graph = nx.Graph()
    graph = co_occurrence_network(words, graph)
    # 以下でグラフ


if __name__ == '__main__':
    _create_graph_in_CON()
