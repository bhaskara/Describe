from collections import namedtuple
import numpy as np

List = namedtuple('List', ['type', 'length'])
Tuple = namedtuple('Tuple', ['types'])
Array = namedtuple('Array', ['dim'])
Dict = namedtuple('Dict', ['key', 'value'])
Int = namedtuple('Int', ['min', 'max'])
Float = namedtuple('Float', ['min', 'max'])
Str = namedtuple('String', [])
Atom = namedtuple('Atom', ['type'])
Maybe = namedtuple('Maybe', ['type'])
Any = namedtuple('Any', [])
Empty = namedtuple('Empty', [])

idxs = [Maybe, List, Tuple, Dict, Array, Int, Float, Str, Atom, Any, Empty]

def idx(d):
  return idxs.index(type(d))

def wh(obj):
  return pprint(describe(obj))

def pprint(desc, lvl=0):
  if isinstance(desc, Empty):
    return "?"
  elif isinstance(desc, Any):
    return "*"
  elif isinstance(desc, Atom):
    return desc.type
  elif isinstance(desc, Str):
    return "String"
  elif isinstance(desc, Dict):
    return '{' + "{}: {}".format(pprint(desc.key),
                                 pprint(desc.value)) + '}'
  elif isinstance(desc, Float):
    if lvl < -1:
      return "Float({}, {})".format(*desc)
    else:
      return "Float"
  elif isinstance(desc, Int):
    if lvl < -1:
      return "Int({}, {})".format(*desc)
    else:
      return "Int"
  elif isinstance(desc, Maybe):
    return "Maybe({})".format(pprint(desc.type))
  elif isinstance(desc, Array):
    return "{}d array".format(desc.dim)
  elif isinstance(desc, List):
    return "[{}]".format(pprint(desc.type, lvl=lvl + 1))
  elif isinstance(desc, Tuple):
    types = ", ".join([pprint(t, lvl=lvl + 1) for t in desc.types])
    return "({})".format(types)
  
  

def describe(obj):
  if isinstance(obj, tuple):
    return Tuple(map(describe, obj))
  elif isinstance(obj, list):
    return List(generalize(*map(describe, obj)), len(obj))
  elif isinstance(obj, np.ndarray):
    return Array(len(obj.shape))
  elif obj is None:
    return Maybe(Empty())
  elif isinstance(obj, dict):
    return Dict(generalize(*map(describe, obj.iterkeys())),
                generalize(*map(describe, obj.itervalues())))
  elif isinstance(obj, str):
    return Str()
  elif isinstance(obj, int):
    return Int(obj, obj)
  elif isinstance(obj, float):
    return Float(obj, obj)
  else:
    return Atom(getattr(obj, '__class__', type(obj)))

def generalize(*descs):
  def pairwise(d1, d2):
    if idx(d1) > idx(d2):
      d2, d1 = d1, d2
    if d1 == d2:
      return d1
    elif isinstance(d1, Maybe):
      t1 = d1.type
      t2 = d2.type if isinstance(d2, Maybe) else d2
      return Maybe(generalize(t1, t2))
    elif isinstance(d2, Empty):
      return d1
    elif isinstance(d2, Any):
      return d2
    elif isinstance(d1, List):
      if isinstance(d2, List):
        return List(generalize(d1.type, d2.type), '*')
    elif isinstance(d1, Tuple):
      if isinstance(d2, Tuple) and len(d1.types) == len(d2.types):
        return Tuple([generalize(t1, t2) for t1, t2 in zip(d1.types, d2.types)])
    elif isinstance(d1, Dict):
      if isinstance(d2, Dict):
        return Dict(generalize(d1.key, d2.key), generalize(d1.value, d2.value))
    elif isinstance(d1, Array):
      if isinstance(d2, Array):
        dim = d1.dim if d1.dim == d2.dim else '*'
        return Array(dim)
    elif isinstance(d1, Int):
      if isinstance(d2, Int):
        a, b = d1
        c, d = d2
        return Int(min(a, c), max(b, d))
    elif isinstance(d1, Float):
      if isinstance(d2, Float):
        a, b = d1
        c, d = d2
        return Float(min(a, c), max(b, d))
    else:
      return Any()

  return reduce(pairwise, descs, Empty())
      
      
a = [1, 2, 3]
b = (4, ('a', 'b'), 2.2)
c = [(False, np.zeros(3)), (True, np.zeros(4))]
          
