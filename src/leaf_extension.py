from itertools import cycle, islice

from src.base_calc import to_number, to_size, numberToBase
from src.node import Node
from src.pattern import pattern, repetition_offset


def make_leaf_nodes(start, step, base, l):
  assert start < base
  assert step < base

  pat = pattern(step, start, base)
  return [Node({p: ()}, l) for p in pat]


def next_step(start_split, step_split, prev_nodes, base, l):
  prev_step = to_number(step_split[1:], base)

  if prev_step == 0:
    pat = pattern(step_split[0], start_split[0], base)
  else:
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base**len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]

  lv_prev_it = iter(cycle(prev_nodes))
  return [Node({p: next(lv_prev_it)}, l) for p in pat]


def last_layer(start_split, step_split, prev_nodes, base, l):
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]
    r = repetition_offset(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))

    pat_it = iter(cycle(pat))
    lv_prev_it = iter(cycle(prev_nodes))
    return [Node(dict(zip(islice(pat_it, tk), islice(lv_prev_it, tk))), l) for tk in r]