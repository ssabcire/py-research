from __future__ import absolute_import, print_function, division, unicode_literals

import unittest
import networkx

from datapolish.graph import closed_neighbors


class TestClosedNeighborsIter(unittest.TestCase):

    def test_closed_neighbors_iter(self):
        g = networkx.Graph()
        g.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 5)])
        neighbors = [{v for v in closed_neighbors(g, n)} for n in g.nodes()]
        self.assertEqual(neighbors[0], {2, 4, 5, 1})
        self.assertEqual(neighbors[1], {1, 3, 2})
        self.assertEqual(neighbors[2], {2, 4, 3})
        self.assertEqual(neighbors[3], {3, 1, 4})
        self.assertEqual(neighbors[4], {1, 5})

        g = networkx.Graph()
        g.add_edges_from([(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 5), (1, 6), (2, 3), (2, 5)])
        '''
        g = networkx.graph_atlas(480)
        0 [1, 2, 4]
        1 [0, 2, 3, 5, 6]
        2 [0, 1, 3, 5]
        3 [1, 2]
        4 [0]
        5 [1, 2]
        6 [1]
        '''
        self.assertEqual(set(closed_neighbors(g, 0)), {0, 1, 2, 4})
        self.assertEqual(set(closed_neighbors(g, 1)), {1, 0, 2, 3, 5, 6})
        self.assertEqual(set(closed_neighbors(g, 2)), {2, 0, 1, 3, 5})
        self.assertEqual(set(closed_neighbors(g, 3)), {3, 1, 2})
        self.assertEqual(set(closed_neighbors(g, 4)), {4, 0})
        self.assertEqual(set(closed_neighbors(g, 5)), {5, 1, 2})
        self.assertEqual(set(closed_neighbors(g, 6)), {6, 1})


if __name__ == '__main__':
    unittest.main()