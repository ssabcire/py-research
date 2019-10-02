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
Module for view or iterator of closed neighbors for networkx 1 and 2
"""
from __future__ import absolute_import, print_function, division, unicode_literals
import networkx
from typing import Iterable, Any
from itertools import chain

if networkx.__version__ >= '2':
    nodes = networkx.nodes
    edges = networkx.edges
    neighbors = networkx.Graph.neighbors
else:
    nodes = networkx.nodes_iter
    edges = networkx.edges_iter
    neighbors = networkx.Graph.neighbors_iter


def closed_neighbors(g, v):
    """
    Return an view or iterator of closed neighbors of the input node v
    :param g:   Input graph
    :param v:   A node of graph g
    :return:    A view of closed neighbors of the input node v
    """
    return chain(neighbors(g, v), g.nbunch_iter([v]))


closed_neighbors.__annotations__ = {'g': networkx.Graph, 'v': Any,
                                    'return': Iterable}
