"""
unittest for data_polish
"""
from __future__ import absolute_import, print_function, division, unicode_literals

import unittest

from typing import Dict, Any
import networkx

from datapolish import neighbor_intersection, sim_intersection, sim_jaccard, sim_pmi, sim_npmi, \
    data_polish, iterate_data_polish, pmi, npmi
from datapolish.graph import is_identical_graph

if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
    neighbors = networkx.Graph.neighbors
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter
    neighbors = networkx.Graph.neighbors_iter


class TestDataPolish(unittest.TestCase):
    def setUp(self):
        self._g = networkx.Graph()  # type: networkx.Graph
        self._g.add_edges_from([(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 5)])
        # self._degrees = [4, 6, 5, 3, 2, 3, 2]

    def test_neighbor_intersection(self):
        self.assertEqual(neighbor_intersection(self._g, 0), {})
        self.assertEqual(neighbor_intersection(self._g, 1), {0: 3})
        self.assertEqual(neighbor_intersection(self._g, 2), {0: 3, 1: 5})
        self.assertEqual(neighbor_intersection(self._g, 3), {0: 2, 1: 3, 2: 3})
        self.assertEqual(neighbor_intersection(self._g, 4), {0: 2, 1: 1, 2: 1})
        self.assertEqual(neighbor_intersection(self._g, 5), {0: 2, 1: 3, 2: 3, 3: 2})
        self.assertEqual(neighbor_intersection(self._g, 6), {0: 1, 1: 2, 2: 1, 3: 1, 5: 1})

    def test_sim_intersection(self):
        intersections = {
            0: {},
            1: {0: 3},
            2: {0: 3, 1: 5},
            3: {0: 2, 1: 3, 2: 3},
            4: {0: 2, 1: 1, 2: 1, 3: 0},
            5: {0: 2, 1: 3, 2: 3, 3: 2, 4: 0},
            6: {0: 1, 1: 2, 2: 1, 3: 1, 4: 0, 5: 1}
        }   # type: Dict[Any][Dict[Any][float]]
        for u in nodes(self._g):
            num_common_neighbor = neighbor_intersection(self._g, u)     # type: Dict[Any][float]
            for v, intersection_u_v in num_common_neighbor.items():
                self.assertEqual(sim_intersection(self._g, u, v, intersection_u_v), intersections[u][v])

    def test_sim_jaccard(self):
        jaccards = {
            0: {},
            1: {0: 3 / (6 + 4 - 3)},
            2: {0: 3 / (5 + 4 - 3), 1: 5 / (5 + 6 - 5)},
            3: {0: 2 / (3 + 4 - 2), 1: 3 / (3 + 6 - 3), 2: 3 / (3 + 5 - 3)},
            4: {0: 2 / (2 + 4 - 2), 1: 1 / (2 + 6 - 1), 2: 1 / (2 + 5 - 1), 3: 0 / (2 + 3 - 0)},
            5: {0: 2 / (3 + 4 - 2), 1: 3 / (3 + 6 - 3), 2: 3 / (3 + 5 - 3), 3: 2 / (3 + 3 - 2), 4: 0 / (3 + 2 - 0)},
            6: {0: 1 / (2 + 4 - 1), 1: 2 / (2 + 6 - 2), 2: 1 / (2 + 5 - 1), 3: 1 / (2 + 3 - 1), 4: 0 / (2 + 2 - 0),
                5: 1 / (2 + 3 - 1)}
        }   # type: Dict[Any][Dict[Any][float]]
        for u in nodes(self._g):
            num_common_neighbor = neighbor_intersection(self._g, u)     # type: Dict[Any][float]
            for v, intersection_u_v in num_common_neighbor.items():
                self.assertEqual(sim_jaccard(self._g, u, v, intersection_u_v), jaccards[u][v])

    def test_sim_pmi(self):
        pmis = {
            0: {},
            1: {0: pmi(3/7, 6/7, 4/7)},
            2: {0: pmi(3/7, 5/7, 4/7), 1: pmi(5/7, 5/7, 6/7)},
            3: {0: pmi(2/7, 3/7, 4/7), 1: pmi(3/7, 3/7, 6/7), 2: pmi(3/7, 3/7, 5/7)},
            4: {0: pmi(2/7, 2/7, 4/7), 1: pmi(1/7, 2/7, 6/7), 2: pmi(1/7, 2/7, 5/7), 3: -float('inf')},
            5: {0: pmi(2/7, 3/7, 4/7), 1: pmi(3/7, 3/7, 6/7), 2: pmi(3/7, 3/7, 5/7), 3: pmi(2/7, 3/7, 3/7),
                4: -float('inf')},
            6: {0: pmi(1/7, 2/7, 4/7), 1: pmi(2/7, 2/7, 6/7), 2: pmi(1/7, 2/7, 5/7), 3: pmi(1/7, 2/7, 3/7),
                4: -float('inf'), 5: pmi(1/7, 2/7, 3/7)}
        }   # type: Dict[Any][Dict[Any][float]]
        for u in nodes(self._g):
            num_common_neighbor = neighbor_intersection(self._g, u)     # type: Dict[Any][float]
            for v, intersection_u_v in num_common_neighbor.items():
                self.assertEqual(sim_pmi(self._g, u, v, intersection_u_v), pmis[u][v])

    def test_sim_npmi(self):
        npmis = {
            0: {},
            1: {0: npmi(3/7, 6/7, 4/7)},
            2: {0: npmi(3/7, 5/7, 4/7), 1: npmi(5/7, 5/7, 6/7)},
            3: {0: npmi(2/7, 3/7, 4/7), 1: npmi(3/7, 3/7, 6/7), 2: npmi(3/7, 3/7, 5/7)},
            4: {0: npmi(2/7, 2/7, 4/7), 1: npmi(1/7, 2/7, 6/7), 2: npmi(1/7, 2/7, 5/7), 3: -float('inf')},
            5: {0: npmi(2/7, 3/7, 4/7), 1: npmi(3/7, 3/7, 6/7), 2: npmi(3/7, 3/7, 5/7), 3: npmi(2/7, 3/7, 3/7),
                4: -float('inf')},
            6: {0: npmi(1/7, 2/7, 4/7), 1: npmi(2/7, 2/7, 6/7), 2: npmi(1/7, 2/7, 5/7), 3: npmi(1/7, 2/7, 3/7),
                4: -float('inf'), 5: npmi(1/7, 2/7, 3/7)}
        }   # type: Dict[Any][Dict[Any][float]]
        for u in nodes(self._g):
            num_common_neighbor = neighbor_intersection(self._g, u)     # type: Dict[Any][float]
            for v, intersection_u_v in num_common_neighbor.items():
                self.assertEqual(sim_npmi(self._g, u, v, intersection_u_v), npmis[u][v])

    def test_data_polish(self):
        # sim_intersection, 2
        h = networkx.Graph()
        h.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                          (1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 5), (3, 5)])
        self.assertTrue(is_identical_graph(data_polish(self._g, sim_intersection, 2), h))

        # sim_intersection, 3
        h = networkx.Graph()
        h.add_nodes_from(self._g.nodes())
        h.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 5), (2, 3), (2, 5)])
        self.assertTrue(is_identical_graph(data_polish(self._g, sim_intersection, 3), h))

        # sim_intersection, 4
        h = networkx.Graph()
        h.add_nodes_from(self._g.nodes())
        h.add_edges_from([(1, 2)])
        self.assertTrue(is_identical_graph(data_polish(self._g, sim_intersection, 4), h))

    def test_iterate_data_polish(self):
        h = networkx.Graph()
        h.add_nodes_from(self._g.nodes())
        h.add_edges_from([(0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
                          (1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 5), (3, 5)])
        self.assertTrue(is_identical_graph(iterate_data_polish(self._g, sim_intersection, 2, 100, verbose=True), h))

        h = networkx.Graph()
        h.add_nodes_from(self._g.nodes())
        h.add_edges_from([(0, 1), (0, 2), (1, 2), (1, 3), (1, 5), (2, 3), (2, 5)])
        self.assertTrue(is_identical_graph(iterate_data_polish(self._g, sim_intersection, 3, 100, verbose=True), h))
