import numpy as np
from array_range import array_range


def test():

  def innertest(shape, step):
    x = np.arange(np.prod(shape)).reshape(shape) + 1
    y = x.copy()
    neg = np.sum(x < 0)
    for tup in array_range([0, 0], x.shape, step):
      x[tup] *= -1
      newneg = np.sum(x < 0)
      assert newneg > neg
      neg = newneg
    assert np.array_equal(x, -y)

  innertest([4, 7], [2, 4])
  innertest([4, 7], [1, 1])
  innertest([4, 7], [5, 4])
  innertest([4, 7], [5, 9])


if __name__ == '__main__':
  test()
  print('success')