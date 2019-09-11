# array_range

**Motivation** Numpy's [`array_split`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.array_split.html) can split a multidimensional array into non-overlapping sub-arrays. However, this is not a memory-efficient way to partition an array since it effectively doubles memory usage.

This module provides an *iterable generator* that produces tuples of slices, each of which can be used to index into a Numpy array and obtain a small view into it. It is very memory-efficient since no copy of the array is ever created.

This all works because Numpy ndarrays can be indexed using a tuple of slices: that is, `arr[a:b, c:d, e:f]` is equivalent to `arr[(slice(a, b), slice(c, d), slice(e, f))]`.

This module doesn't import Numpy at all since it generates Python slices.

**Installation** `$ pip install array_range`

**API and usage** `def array_range(start: List[int], stop: List[int], step: List[int]) -> Iterable[Tuple]` takes same arguments as `range` but all three are required, and all three arguments need to be the same length. Because the iterable contains tuples of slices, and because tuples of slices can be used to index Numpy multidimensional arrays (or any multidimensional data type you may have), you can do something like the following:

```py
from array_range import array_range
import numpy as np
arr = np.random.randint(1, 10,(1000, 1000))

for tup in array_range([0, 0], arr.shape, [5, 7]):
  arr[tup] *= -1 # dumb example
```

The above example is overly-contrived so let me describe a real-world use case: suppose `arr` is a memory-mapped Numpy array far too large to fit in memory, and you want to run a run a non-overlapping-window operation over it. `array_range` would let you do this easily. In the above example, the array would be modified in 5x7 chunks at a time.

Like `numpy.array_split`, this library will handle the case where the final slice in any given dimension isn't the same size as the rest (as in the case above, 1000 is not evenly divisible by 7 so the last block would be 5x2).