import networkx as nx
from .const import JSONFILES
from .co_occurrence_network import co_occurrence_network


def main():
    graph = nx.Graph()
    graph = co_occurrence_network(graph)
    # 以下でデータ研磨


if __name__ == '__main__':
    main()
