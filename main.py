import networkx as nx
from .const import JSONFILES
from .extract_text import extract_text
from .morphological_analysis import morphological_analysis
from .co_occurrence_network import co_occurrence_network

def main():
    texts = extract_text(JSONFILES)
    # 重複気にするならlist, 単語の出現回数が必要ならdict
    words = set()
    for text in texts:
        words = words | morphological_analysis(text)
    graph = nx.Graph()
    graph = co_occurrence_network(words, graph)


if __name__ == '__main__':
    main()
