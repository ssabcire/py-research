"""
unit test for binarize_graph.py
"""

from __future__ import absolute_import, print_function, division, unicode_literals

import unittest
import networkx

from datapolish.graph import binarize_graph

if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter


class TestBinarize(unittest.TestCase):

    def test_binarize_graph(self):
        g = networkx.complete_graph(10)
        for (u, v) in edges(g):
            g[u][v]['weight'] = min(u, v) / max(u, v)

        for th in (0, 0.1, 0.3, 0.5, 1):
            h = binarize_graph(g, 'weight', th)
            for (u, v) in edges(g):
                if min(u, v) / max(u, v) >= th:
                    self.assertTrue(h.has_edge(u, v))
                else:
                    self.assertFalse(h.has_edge(u, v))


if __name__ == '__main__':
    unittest.main()
