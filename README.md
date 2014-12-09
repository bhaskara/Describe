Utility for printing a summary Haskellish description of a nested Python object.  Finds the most specific type description that applies.  E.g., 

```
In [11]: import describe

In [12]: describe.wh({'foo': 3, 'bar': 4})
Out[12]: '{String: Int}'

In [13]: describe.wh([(3, 'foo', np.zeros((2, 2))), (6, 'bar', np.ones((3, 3)))])
Out[13]: '[(Int, String, 2d array)]'

In [16]: describe.wh([(3, 'foo', np.zeros((2, 2))), (6, 'bar', np.ones((3, 3, 3)))])
Out[16]: '[(Int, String, *d array)]'

In [18]: describe.wh([3, 4, None, 2, None])
Out[18]: '[Maybe(Int)]'

```