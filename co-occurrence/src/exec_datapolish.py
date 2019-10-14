def ccc(graph: nx.Graph, s: str):
    '''
    クリーク数と孤立頂点数を表示
    '''
    # 無向グラフから極大クリークを求める cliques=イテレータ、リスト
    cliques = nx.find_cliques(graph)
    cliques_cnt = i_vertex_cnt = 0
    for clique in cliques:
        if len(clique) > 1:
            cliques_list.append(clique)
        i_vertex.append(clique)
    print(s, 'クリーク数 = ', len(cliques_cnt))
    print(s, '孤立頂点数 = ', len(i_vertex_cnt))


def ccc_data_polish(graph: nx.Graph, s: str):
    '''
    クリーク数と孤立頂点数とかを使ってデータ研磨などを行うためのメソッド。途中
    '''
    # 無向グラフから極大クリークを求める cliques=イテレータ、リスト
    cliques = nx.find_cliques(graph)
    cliques_list = list()
    i_vertex = list()
    for clique in cliques:
        if len(clique) > 1:
            cliques_list.append(clique)
        i_vertex.append(clique)
    print(s, 'クリーク数 = ', len(cliques_list))
    print(s, '孤立頂点数 = ', len(i_vertex))


def exec_data_polish():
        # 2値化を行う
    b_graph = binarize_graph(graph, 'npmi', 0.7)
    ccc(b_graph, '2値化')
    print("2値化したときのedge数 = ", len(b_graph.edges()))
