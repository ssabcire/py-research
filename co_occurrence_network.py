import itertools
import networkx as nx
# import as dp


def co_occurence_network(words: set, graph: nx.Graph) -> nx.Graph:
    '''
    共起ネットワークを作成
    '''
    _add_node_and_edge(words, graph)
    _add_node_probability(graph)
    _add_edge_probability(graph)
    _add_npmi(graph)
    return graph

#疑問箇所。とくにnodeとedge
def _add_node_and_edge(words: set, graph: nx.Graph):
    '''
    Graphにnodeとedgeを付与
    '''
    graph.add_nodes_from(words, count=1)
    for u, v in itertools.combinations(words, 2):
        if graph.has_edge(u, v):
            graph[u][v]['count'] += 1
        else:
            graph.add_edge(u, v, count=1)


def _add_node_probability(graph: nx.Graph):
    '''
    各ノードの出現確率を計算
    '''
    node_sum = 0
    for v in graph.nodes():
        # node_sum違う恐れあり
        node_sum += graph.nodes[v]['count']
    for v in graph.nodes():
        graph.nodes[v]['probability'] = graph.nodes[v]['count'] / node_sum


def _add_edge_probability(graph: nx.Graph):
    '''
    各エッジの出現確率を計算
    '''
    edge_sum = 0
    for u, v in graph.edges():
        # edge_sum違う恐れあり
        edge_sum += graph[u][v]['count']
    for u, v in graph.edges():
        graph[u][v]['probability'] = graph[u][v]['count'] / edge_sum


def _add_npmi(graph: nx.Graph):
    for u, v in graph.edges():
        graph[u][v]['npmi'] = dp.npmi(
            graph[u][v]['probability'],
            graph.nodes[u]['probability'],
            graph.nodes[v]['probability']
        )
