from __future__ import absolute_import, print_function, division, unicode_literals
import unittest
from datapolish import jaccard, pmi, npmi


class TestSimilarity(unittest.TestCase):

    def test_jaccard(self):
        self.assertEqual(jaccard(100, 100, 100), 1)
        self.assertEqual(jaccard(0, 100, 100), 0)
        self.assertEqual(jaccard(100, 200, 100), 0.5)
        self.assertEqual(jaccard(5, 10, 10), 1/3)
        self.assertEqual(jaccard(4, 10, 10), 1/4)
        self.assertEqual(jaccard(3, 6, 4), 3/7)

    def test_pmi(self):
        self.assertEqual(pmi(0, 0, 0), -float('inf'))
        self.assertEqual(pmi(0, 0.5, 0.5), -float('inf'))
        self.assertEqual(pmi(0.25, 0.5, 0.5), 0)
        self.assertEqual(pmi(0.1, 0.8, 0.25), -1)
        self.assertEqual(pmi(0.5, 0.5, 0.5), 1)
        self.assertEqual(pmi(0.25, 0.25, 0.25), 2)

    def test_npmi(self):
        self.assertEqual(npmi(0, 0.5, 0.5), -1)
        self.assertEqual(npmi(0.5, 0.5, 0.5), 1)
        self.assertEqual(npmi(0.25, 0.5, 0.5), 0)


if __name__ == '__main__':
    unittest.main()
