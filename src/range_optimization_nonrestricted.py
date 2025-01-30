from collections import deque
from itertools import repeat, cycle, islice
from math import gcd

from src.base_calc import numberToBase, order, to_number, to_size, to_number_special
from src.node import Node
from src.pattern import minimal_seq, pattern_ext, repetition_ext
from src.range_utility import find_last_number_of_range, strip_equal_start, number_of_nodes_per_layer, find_group



def nth(it, n):
    for i in range(n):
        x = next(it)
    return x


def skip_elements(iterator, count):
  deque(islice(iterator, count), maxlen=0)


def crange(start: int, stop: int, step: int, base: int) -> tuple[Node, list[Node]]:
  BASE = base
  assert base > 1
  assert step > 0
  assert start >= 0
  assert start <= stop

  if stop == start:
    return # TODO empty graph??

  l = []
  start_split_1 = numberToBase(start, base)
  step_order = order(step, base)

  # Generate a tree with only the start number
  if stop - start <= step:
    curr_node = ()
    if step_order >= order(start, base):  # create only one node with digit of order(step)
      curr_node = Node({start: ()}, l)
    else:
      trailing_digits = start_split_1[:-(step_order + 1)]   # all digits that need to come before the leaf node
      leaf = to_number(start_split_1[-(step_order + 1):], base)  # leaf node of order == order(step)
      trailing_digits.reverse()

      for s in [leaf] + trailing_digits:
        curr_node = Node({s: curr_node}, l)

      # you can use this instead of the if/else for simplicity. BUT an inconsistency arises with the other trees since other trees have number of order(step), in their leaf nodes, and with following code this special case returns leafs of order 0. So use the if/else above for consistency.
      # for s in reversed(start_split_1):
      #   curr_node = Node({s: prev_node}, l)
      #   prev_node = curr_node

    return curr_node, l


  last_number = find_last_number_of_range(start, stop, step)
  last_number_split = numberToBase(last_number, base)

  start_split = to_size(start_split_1, len(last_number_split))

  offset = start%step

  std_nodes = int(step/gcd(BASE**(order(step, base) + 1), step))

  start_split_, last_number_split_, to_add = strip_equal_start(start_split, last_number_split)


  # calculate the number of nodes in each layer, which is not the lowest or highest layer
  size_intermediate_layers = number_of_nodes_per_layer(start_split_, last_number_split_, step, base)


  pat = minimal_seq(pattern_ext(step, offset, base))

  # the next two are also calculated in the find_group method (not efficient?)
  pat_start_idx = pat.index(to_number(start_split_[-(order(step, base) + 1):], base))
  pat_stop_idx = pat.index(to_number(last_number_split[-(order(step, base) + 1):], base))


  r1 = repetition_ext(step, offset, base)
  # compress r1 only if pattern is also compressed
  if len(pat) == sum(minimal_seq(r1)):
    r1_ = minimal_seq(r1)
  else:
    r1_ = r1

  assert pat_start_idx <= sum(r1_)

  start_group, start_idx = find_group(pat, r1_, to_number(start_split_[-(order(step, base) + 1):], base))
  separate_start_group: bool = (start_idx != 0)

  stop_group, stop_idx = find_group(pat, r1_, to_number(last_number_split[-(order(step, base) + 1):], base))
  separate_stop_group: bool = (stop_idx != (r1_[stop_group] - 1))


  # bottom layer (leaf nodes)
  lv1 = []

  pat_it = iter(cycle(pat))

  # in the case there will only be one layer (only leaf nodes)
  if len(last_number_split_) == (order(step, base) + 1):
    curr_node = Node(dict(zip(pat[pat_start_idx:pat_stop_idx + 1], repeat(()))), l)
    to_add.reverse()
    for e in to_add:
      curr_node = Node({e: curr_node}, l)

    return curr_node, l

  # make leaf layer
  for tk in r1_:
    lv1.append(Node(dict(zip(islice(pat_it, tk), repeat(()))), l))

  lvs = [lv1]

  # extra start node
  curr_start_node = None
  curr_start_idx = - (order(step, base) + 2)

  if separate_start_group:
    last_idx_start_group = pat_start_idx + r1_[start_group] - (start_idx + 1)
    lv1_start_node = Node(dict(zip(pat[pat_start_idx:last_idx_start_group + 1], repeat(()))), l)

    curr_start_node = lv1_start_node

  # extra stop node
  curr_stop_node = None

  if separate_stop_group:
    first_idx_stop_group = pat_stop_idx - stop_idx
    lv1_stop_node = Node(dict(zip(pat[first_idx_stop_group:pat_stop_idx + 1], repeat(()))), l)

    curr_stop_node = lv1_stop_node


  # intermediate layers

  size_intermediate_layers.reverse()
  next_start_group = (start_group + 1) %len(r1_)  # correct both with or without the modulo (without modulo, we might go through one cycle more of the previous level nodes)

  to_skip = next_start_group if separate_start_group else start_group

  std_nodes_ = len(r1_)
  eq_stop_node = stop_group

  for i, nns in enumerate(size_intermediate_layers):

    lv_curr = []
    lv_prev = lvs[-1]
    lv_prev_it = iter(cycle(lv_prev))

    skip_elements(lv_prev_it, to_skip)

    stop_groups_to_skip = (eq_stop_node - last_number_split_[curr_start_idx]) % std_nodes_
    if separate_start_group:
      nodes = [curr_start_node] + list(islice(lv_prev_it, BASE - start_split_[curr_start_idx] - 1))
      curr_start_node = Node(dict(zip(range(start_split_[curr_start_idx], BASE), nodes)), l)

    if not separate_start_group and start_split_[curr_start_idx] > 0:
      separate_start_group = True
      nodes = islice(lv_prev_it, BASE - start_split_[curr_start_idx])
      curr_start_node = Node(dict(zip(range(start_split_[curr_start_idx], BASE), nodes)), l)

    next_eq_stop_node = None
    first_node = next(lv_prev_it)
    peek_node = first_node

    for n in range(nns):
      d = dict(zip(range(BASE), [peek_node] + list(islice(lv_prev_it, BASE - 1))))
      if d[last_number_split_[curr_start_idx]] == lv_prev[eq_stop_node]:
        next_eq_stop_node = n
      lv_curr.append(Node(d, l))

      peek_node = next(lv_prev_it)
      if peek_node == first_node:
        break

    if next_eq_stop_node is None:
      # This should never occur
      raise NotImplementedError("Unexpected condition: next_eq_stop_node should not be None.")

    lv_prev_it_stop = iter(cycle(lv_prev))
    skip_elements(lv_prev_it_stop, stop_groups_to_skip)

    if separate_stop_group:
      nodes = list(islice(lv_prev_it_stop, last_number_split_[curr_start_idx])) + [curr_stop_node]
      curr_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), nodes)), l)

    if not separate_stop_group and last_number_split[curr_start_idx] < BASE - 1:
      separate_stop_group = True
      nodes = islice(lv_prev_it_stop, last_number_split_[curr_start_idx] + 1)
      curr_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), nodes)), l)

    lvs.append(lv_curr)

    curr_start_idx -= 1
    to_skip = 0
    std_nodes_ = std_nodes
    eq_stop_node = next_eq_stop_node


  # top layer

  lv_prev_it = iter(cycle(lvs[-1]))

  skip_elements(lv_prev_it, to_skip)

  # Initialize first and last nodes
  first_node = [curr_start_node] if separate_start_group else []
  last_node = [curr_stop_node] if separate_stop_group else []

  # Compute slice size of middle nodes
  slice_size = (last_number_split_[0] - start_split_[0] + 1) - separate_start_group - separate_stop_group

  nodes = first_node + list(islice(lv_prev_it, slice_size)) + last_node
  edge_labels = range(start_split_[0], last_number_split_[0] + 1)

  top_node = Node(dict(zip(edge_labels, nodes)), l)

  # lvs.append([top_node])
  to_add.reverse()
  for e in to_add:
    top_node = Node({e: top_node}, l)

  return top_node, l


def print_graph(l):
  print("digraph G { \n ranksep=3")
  for n in l: n.graphviz()
  print("}")



if __name__ == '__main__':
  start, stop, step, base = (20908, 65539, 35, 16)


  rn, l = crange(start, stop, step, base)
  print("BASE", base)
  # print(repr(rn))

  # print(sorted(map(tuple, rn.paths())))
  r = [i for i in range(start, stop, step)]
  print("real  ", [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
  print("wanted", r)
  # assert(r == [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
  print(len(r))
  # print(max(map(to_number, rn.paths())))

  print("#wanted: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))
  print("check: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))

  ns = (map(lambda x: to_number_special(list(x), order(step, base), base), rn.paths()))
  m = start % step
  for n in ns:
    if not n % step == m:
      print("INCORRECT NUMBERS from", n)
      break
  print()
  print_graph(l)