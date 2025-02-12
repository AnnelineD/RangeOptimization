from itertools import cycle, islice

from src.base_calc import to_number, to_size, numberToBase
from src.node import Node
from src.pattern import pattern, minimal_seq, repetition_offset


def make_leaf_nodes(start, step, base, l):
  assert start < base
  assert step < base

  pat = pattern(step, start, base)
  return [Node({p: ()}, l) for p in pat]


def next_step(start_split, step_split, prev_nodes, base, l):
  # assert step < base
  # assert start < base

  step_o = to_number(step_split[1:], base)

  if step_o == 0:
    pat = pattern(step_split[0], start_split[0], base)
  else:
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base**len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]

  lv_prev_it = iter(cycle(prev_nodes))

  return [Node({p: next(lv_prev_it)}, l) for p in pat]


def last_layer(start_split, step_split, prev_nodes, base, l):
    lv_new = []
    lv_prev_it = iter(cycle(prev_nodes))

    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))

    r = repetition_offset(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))
    if len(pat_full) == sum(minimal_seq(r)):
        r = minimal_seq(r)

    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]
    pat_it = iter(cycle(pat))

    for tk in r:
        lv_new.append(Node(dict(zip(islice(pat_it, tk), islice(lv_prev_it, tk))), l))

    return lv_new