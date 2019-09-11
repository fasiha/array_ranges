"""
Numpy's `split` can split a multidimensional array into non-overlapping
sub-arrays. However, this is not a memory-efficient way of dealing with
non-overlapping partitions of an array because it effectively doubles
memory usage.

This module provides an iterable generator that produces tuples of slices,
each of which can be used to index into a Numpy array and obtain a small
view into it. It is very memory-efficient since no copy of the array is
ever created.

This all works because Numpy ndarrays can be indexed using a tuple of
slices: that is, `arr[a:b, c:d, e:f]` is equivalent to
`arr[(slice(a, b), slice(c, d), slice(e, f))]`.

This module doesn't import Numpy at all since it generates Python slices.
"""

from itertools import product
from typing import List, Iterable, Tuple


def array_range(start: List[int], stop: List[int], step: List[int]) -> Iterable[Tuple]:
  """
  Makes an iterable of non-overlapping slices, e.g., to partition an array

  Returns an iterable of tuples of slices, each of which can be used to
  index into a multidimensional array such as Numpy's ndarray.

  >> [arr[tup] for tup in array_range([0, 0], arr.shape, [5, 7])]
  
  where `arr` can be indexed with a tuple of slices (e.g., Numpy), will
  evaluate to a list of sub-arrays.

  Same arguments as `range` except all three arguments are required and
  expected to be list-like of same length. `start` indicates the indexes
  to start each dimension. `stop` indicates the stop index for each
  dimension. `step` is the size of the chunk in each dimension.
  """
  assert len(start) == len(stop)
  assert len(stop) == len(step)
  assert all(map(lambda x: x > 0, step))
  startRangesGen = map(lambda v: range(*v), zip(start, stop, step))
  startToSliceMapper = lambda multiStart: tuple(
      slice(i, min(i + step, stop)) for i, stop, step in zip(multiStart, stop, step))
  return map(startToSliceMapper, product(*startRangesGen))
