"""
unit test for identical_graph.py
"""

from __future__ import absolute_import, print_function, division, unicode_literals

import unittest
import networkx

from datapolish.graph import is_identical_graph


if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter


class TestIdenticalGraph(unittest.TestCase):

    def test_is_identical_graph(self):
        g = networkx.complete_graph(10)
        h = networkx.complete_graph(10)
        self.assertTrue(is_identical_graph(g, h))

        g.remove_edge(8, 9)
        h.remove_edge(8, 9)
        self.assertTrue(is_identical_graph(g, h))

        h.add_edge(8, 9)
        self.assertFalse(is_identical_graph(g, h))

        h.remove_edge(7, 9)
        self.assertFalse(is_identical_graph(g, h))


        h.remove_node(9)
        self.assertFalse(is_identical_graph(g, h))


if __name__ == '__main__':
    unittest.main()
