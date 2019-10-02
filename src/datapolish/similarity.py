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
Module for functions calculating similarity value,
such as Jaccard coefficient, pointwise mutual information (PMI), normalized PMI.
"""

from __future__ import absolute_import, print_function, division, unicode_literals
import math

'''
Functions calculating similarity.
'''


def jaccard(size_intersection, size1, size2):
    """
    Calculate Jaccard coefficient of two sets A and B, i.e., |A \cap B| / |A \cup B|
    :param size_intersection: the size of the intersection of set A and B, i.e., |A \cap B|
    :param size1:   the size of set A, i.e., |A|
    :param size2:   the size of set B, i.e., |B|
    :return:    the Jaccard coefficient of two sets A and B
    """
    assert (size1 >= 0 and size2 >= 0)
    assert (size1 > 0 or size2 > 0)
    assert (size_intersection <= size1 and size_intersection <= size2)

    return size_intersection / (size1 + size2 - size_intersection)


jaccard.__annotations__ = {'size_intersection': float, 'size1': float, 'size2': float,
                           'return': float}


def pmi(p_xy, p_x, p_y, base=2):
    """
    calculate pointwise mutual information between x and  y.
    log( p_xy / (p_x * p_y) )
    :param p_xy:    coincidence probability of x and y
    :param p_x:     occurrence probability of x
    :param p_y:     occurrence probability of y
    :param base:    base of log
    :return:    pointwise mutual information between x and  y
    """
    assert (p_xy >= 0 and p_x >= 0 and p_y >= 0 and base > 0)
    assert (p_x <= 1 and p_y <= 1)
    assert (p_xy <= p_x and p_xy <= p_y)

    if p_xy == 0:
        return -float('inf')
    return math.log(p_xy, base) - math.log(p_x, base) - math.log(p_y, base)


pmi.__annotations__ = {'p_xy': float, 'p_x': float, 'p_y': float, 'base': float,
                       'return': float}


def npmi(p_xy, p_x, p_y, base=2):
    """
    calculate normalized pointwise mutual information between x and  y.
    - log( p_xy / (p_x * p_y) ) / log(p_xy)
    :param p_xy:    coincidence probability of x and y
    :param p_x:     occurrence probability of x
    :param p_y:     occurrence probability of y
    :param base:    base of log
    :return:    normalized pointwise mutual information between x and  y
    """
    assert (p_xy >= 0 and p_x >= 0 and p_y >= 0 and base > 0)
    assert (p_x <= 1 and p_y <= 1)
    assert (p_xy <= p_x and p_xy <= p_y)

    if p_xy == 0:
        return -1
    return pmi(p_xy, p_x, p_y, base) / -math.log(p_xy, base)


pmi.__annotations__ = {'p_xy': float, 'p_x': float, 'p_y': float, 'base': float,
                       'return': float}
