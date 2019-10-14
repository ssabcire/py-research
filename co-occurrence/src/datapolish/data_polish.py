# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
Module fo data polish algorithm with Networkx grpah

"""

from __future__ import absolute_import, print_function, division, unicode_literals
from builtins import dict, range

from collections import deque
from typing import Any, Dict, Callable, Deque

import networkx

from .similarity import jaccard, pmi, npmi
from .graph import closed_neighbors, is_identical_graph

if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
    neighbors = networkx.Graph.neighbors
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter
    neighbors = networkx.Graph.neighbors_iter


def neighbor_intersection(input_graph, u):
    """
    Return dict of the number of common closed neighbors
    between each node v and a given node u in a given graph input_graph.
    :param input_graph:   Input graph
    :param u:   A node of graph input_graph
    :return:    A dictionary s.t.
                key: node of input_graph
                value: # of common neighbors between node v and node u
    """
    intersection = dict()  # Dict
    for w in closed_neighbors(input_graph, u):
        for v in filter(lambda _: _ < u, closed_neighbors(input_graph, w)):
            if v in intersection:
                intersection[v] += 1
            else:
                intersection[v] = 1
    return intersection


neighbor_intersection.__annotations__ = {'input_graph': networkx.Graph, 'u': Any, 'return': Dict}


def sim_intersection(input_graph, u, v, size_intersection):
    """
    report size of intersection directly as the similarity value of neighbors between
    :param input_graph: an input graph
    :param u: a vertex in input_graph   (not used in this function, but necessary to unify parameters )
    :param v: a vertex in input_graph   (not used in this function, but necessary to unify parameters )
    :param size_intersection:   size of intersection of N[u] and N[v], i.e., # of common (closed) neighbors of u and v
    :return:  a similarity value  (size_intersection, the number of common closed neighbors of u and v in input_graph)
    """
    del input_graph, u, v  # ignored parameters
    return size_intersection


sim_intersection.__annotations__ = {'input_graph': networkx.Graph, 'u': Any, 'v': any, 'size_intersection': float,
                                    'return': float}


def sim_jaccard(input_graph, u, v, size_intersection):
    """
    calculate Jaccard coefficient between N[u] and N[v] in given graph input_graph
    :param input_graph: an input graph
    :param u: a vertex in input_graph
    :param v: a vertex in input_graph
    :param size_intersection:   size of intersection of N[u] and N[v], i.e., # of common (closed) neighbors of u and v
    :return:    a similarity value  (Jaccard coefficient of N[u] and N[v])
    """
    return jaccard(size_intersection, 1 + input_graph.degree(u), 1 + input_graph.degree(v))


sim_jaccard.__annotations__ = {'input_graph': networkx.Graph, 'u': Any, 'v': any, 'size_intersection': float,
                               'return': float}


def sim_pmi(input_graph, u, v, size_intersection):
    """
    calculate pmi (pointwise mutual infomation) between vertex u and v in graph input_graph
    :param input_graph: an input graph
    :param u: a vertex in input_graph
    :param v: a vertex in input_graph
    :param size_intersection:   size of intersection of N[u] and N[v], i.e., # of common (closed) neighbors of u and v
    :return:
    """
    n = input_graph.number_of_nodes()
    return pmi(size_intersection / n, (1 + input_graph.degree(u)) / n, (1 + input_graph.degree(v)) / n)


sim_pmi.__annotations__ = {'input_graph': networkx.Graph, 'u': Any, 'v': any, 'size_intersection': float,
                           'return': float}


def sim_npmi(input_graph, u, v, size_intersection):
    """
    calclate normalized pmi (pointwise mutual infomation) between vertex u and v in graph input_graph
    :param input_graph: an input graph
    :param u: a vertex in input_graph
    :param v: a vertex in input_graph
    :param size_intersection:   size of intersection of N[u] and N[v], i.e., # of common (closed) neighbors of u and v
    :return:
    """
    n = input_graph.number_of_nodes()
    return npmi(size_intersection / n, (1 + input_graph.degree(u)) / n, (1 + input_graph.degree(v)) / n)


sim_npmi.__annotations__ = {'input_graph': networkx.Graph, 'u': Any, 'v': any, 'size_intersection': float,
                            'return': float}


def data_polish(input_graph, sim_func, threshold, th_abs_error=0):
    """
    apply one iteration of data polishing
    :param input_graph:   an input graph
    :param sim_func: a function calculating similarity value
    :param threshold:   threshold of similarity,
            if similarity value of neighbors between vertices u and v in input_graph
            is not less than threshold, add an edge (u, v) to new graph
    :param th_abs_error        additive error of threshold
    :return:    a polished graph
    """

    similarity_functions = {sim_intersection, sim_jaccard, sim_pmi, sim_npmi}
    assert (sim_func in similarity_functions)

    h = networkx.Graph()  # type: networkx.Graph
    h.add_nodes_from(input_graph.nodes(data=True))

    for u in nodes(input_graph):
        common_neighbors = neighbor_intersection(input_graph, u)  # type: Dict[Any, float]
        for v, size_intersection in common_neighbors.items():
            similarity = sim_func(input_graph, u, v, size_intersection)  # type: float
            # if similarity >= threshold:
            if similarity >= threshold + th_abs_error:
                h.add_edges_from([(u, v, input_graph[u][v] if input_graph.has_edge(u, v) else {})])
            elif similarity >= threshold - th_abs_error and input_graph.has_edge(u, v):
                h.add_edges_from([(u, v, input_graph[u][v])])
    return h


data_polish.__annotations__ = {'input_graph': networkx.Graph, 'sim_func': Callable, 'threshold': float,
                               'th_abs_error': float,
                               'return': networkx.Graph}


def iterate_data_polish(input_graph, sim_func, threshold, max_iteration, max_period=3, th_abs_error=0, verbose=False):
    """
    iterate data polishing until max_iteration times or converged
    :param input_graph:           an input graph
    :param sim_func:    a function calculating similarity value
    :param max_iteration:   maximum iteration number
    :param max_period:      maximum length of cyclic
    :param threshold:
    :param th_abs_error:
    :param verbose:         if True, show graph information for each iteration
    :return:    polished graph after convergence or given number of iteration
    """

    assert (max_period > 0)

    graph_history = deque()  # type: Deque[networkx.Graph]
    graph_history.appendleft(input_graph)
    current_graph = input_graph  # type: networkx.Graph

    is_converged = False

    for i in range(max_iteration):
        current_graph = data_polish(input_graph=current_graph, sim_func=sim_func, threshold=threshold,
                                    th_abs_error=th_abs_error)  # type: networkx.Graph
        if verbose:
            print(i, 'th iteration: current graph width', current_graph.number_of_edges(), 'edges, ',
                  'latest graph with', graph_history[0].number_of_edges(), 'edges, ',
                  'len(graph_history)=', len(graph_history))

        for old_graph in graph_history:
            if is_identical_graph(current_graph, old_graph):
                is_converged = True
                break

        if is_converged:
            break

        graph_history.appendleft(current_graph)
        if len(graph_history) > max_period + 1:
            graph_history.pop()

    return current_graph


iterate_data_polish.__annotations__ = {'input_graph': networkx.Graph, 'sim_func': Callable, 'threshold': float,
                                       'max_iteration': int, 'max_period': int, 'th_abs_error': float, 'verbose': bool,
                                       'return': networkx.Graph}
