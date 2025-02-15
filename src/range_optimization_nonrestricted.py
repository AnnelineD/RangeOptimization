from collections import deque
from itertools import repeat, cycle, islice
from math import gcd, lcm

from src.base_calc import numberToBase, order, to_number, to_size, to_number_special
from src.leaf_extension import make_leaf_nodes, next_step, last_layer, last_layer2
from src.node import Node
from src.pattern import minimal_seq, pattern_ext, repetition_ext, one_up
from src.range_utility import find_last_number_of_range, strip_equal_start, number_of_nodes_per_layer, find_group, \
  skip_elements


def nth(it, n):
    for i in range(n):
        x = next(it)
    return x


def base_layer(step, base, l_, offset):
  # doesn't work!!!!

  step_order = order(step, base)
  step_split = numberToBase(step, base)
  offset_split = numberToBase(offset, base)
  offset_split = to_size(offset_split, len(step_split))

  pat1 = minimal_seq(pattern_ext(step_split[-1], offset, base))

  lv1 = []
  for p in pat1:
    lv1.append(Node({p: ()}, l_))

  lv_prev = lv1
  for i in range(step_order - 1):
    lv_new = []
    r = minimal_seq(repetition_ext(to_number(step_split[-(i+1):], base), offset, base))

    pat = minimal_seq(one_up(r, base, step_split[-(i + 2)]))

    lv_prev_it = iter(cycle(lv_prev))
    for p in pat:
      lv_new.append(Node({p: next(lv_prev_it)}, l_))
    lv_prev = lv_new


  lv3 = []
  pat3 = minimal_seq(one_up(repetition_ext(to_number(step_split[1:], base), offset, base), base, step_split[0]))

  r3 = minimal_seq(repetition_ext(step, offset, base))
  lv2_it = iter(cycle(lv_prev))
  pat3_it = iter(cycle(pat3))
  for tk in r3:
    lv3.append(Node(dict(zip(list(islice(pat3_it, tk)), list(islice(lv2_it, tk)))), l_))

  return lv3


def base_layer_with_offset(offset_, step_, base_, l_):
  assert offset_ < step_

  step_split = numberToBase(step_, base_)
  n_layers = len(step_split)

  offset_split = to_size(numberToBase(offset_, base_), n_layers)

  lv_prev = make_leaf_nodes(offset_split[-1], step_split[-1], base_, l_)

  assert n_layers > 1  # This case is already handled in the crange method before calling this method, so this should never occur

  for i in range(2, n_layers):
    lv_prev = next_step(offset_split[-i:], step_split[-i:], lv_prev, base_, l_)

  return last_layer(offset_split, step_split, lv_prev, base_, l_)


def base_layer_with_offset2(start_, step_, stop_, base_, l_, start_idx, stop_idx, n_steps):
  # assert offset_ < step_

  n_steps = int(n_steps)
  step_split = numberToBase(step_, base_)
  n_layers = len(step_split)

  stop_split = numberToBase(stop_, base_)
  start_split = to_size(numberToBase(start_, base_), n_layers)

  lv_prev = make_leaf_nodes(start_split[-1], step_split[-1], base_, l_, n_steps)

  assert n_layers > 1  # This case is already handled in the crange method before calling this method, so this should never occur

  for i in range(2, n_layers):
    lv_prev = next_step(start_split[-i:], step_split[-i:], lv_prev, base_, l_, n_steps)

  last = last_layer2(start_split, step_split, stop_split, lv_prev, base_, l_, start_idx, stop_idx, n_steps)

  return last



def crange(start: int, stop: int, step: int, base: int) -> tuple[Node, list[Node]]:
  assert base > 1
  assert step > 0
  assert start >= 0
  assert start <= stop

  if stop == start:
    return # TODO empty graph??

  l = []
  start_split_1 = numberToBase(start, base)

  # Generate a tree with only the start number
  if stop - start <= step:
    curr_node = ()

    for s in reversed(start_split_1):
      curr_node = Node({s: curr_node}, l)

    return curr_node, l


  last_number = find_last_number_of_range(start, stop, step)
  last_number_split = numberToBase(last_number, base)

  start_split = to_size(start_split_1, len(last_number_split))
  offset = start%step

  std_nodes = int(step/gcd(base**(order(step, base) + 1), step))

  start_split_, last_number_split_, to_add = strip_equal_start(start_split, last_number_split)


  # calculate the number of nodes in each layer, which is not the lowest or highest layer
  size_intermediate_layers = number_of_nodes_per_layer(start_split_, last_number_split_, step, base)


  pat = pattern_ext(step, offset, base)

  # the next two are also calculated in the find_group method (not efficient?)
  pat_start_idx = pat.index(to_number(start_split_[-(order(step, base) + 1):], base))
  pat_stop_idx = pat.index(to_number(last_number_split[-(order(step, base) + 1):], base))


  r1 = repetition_ext(step, offset, base)

  assert pat_start_idx <= sum(r1)

  start_group, start_idx = find_group(pat, r1, to_number(start_split_[-(order(step, base) + 1):], base))
  separate_start_group: bool = (start_idx != 0)

  stop_group, stop_idx = find_group(pat, r1, to_number(last_number_split[-(order(step, base) + 1):], base))
  separate_stop_group: bool = (stop_idx != (r1[stop_group] - 1))


  # bottom layer (leaf nodes)

  # in the case there will only be one layer (only leaf nodes)
  if len(last_number_split_) == (order(step, base) + 1):
    n_paths = int((last_number - start) / step) + 1
    if n_paths < len(pat):
      print("special 1")
      step_split = numberToBase(step, base)
      n_layers = len(step_split)

      start_split = to_size(numberToBase(start, base), n_layers)

      if n_layers == 1:
        print("special 1 1")
        curr_node = Node(dict(zip(pat[pat_start_idx:pat_stop_idx + 1], repeat(()))), l)

      else:
        lv_prev = make_leaf_nodes(start_split[-1], step_split[-1], base, l, n_paths)

        for i in range(2, n_layers):
          lv_prev = next_step(start_split[-i:], step_split[-i:], lv_prev, base, l, n_paths)

        lv_prev_it = iter(cycle(lv_prev))
        # skip_elements(lv_prev_it, pat_start_idx)
        partial_pat = islice(lv_prev_it, pat_stop_idx + 1)
        assert (pat_start_idx <= pat_stop_idx)
        pat_ = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat[pat_start_idx:pat_stop_idx + 1]]

        curr_node = Node(dict(zip(pat_, partial_pat)), l)

    else:
      print("special 2")
      step_split = numberToBase(step, base)
      n_layers = len(step_split)

      offset_split = to_size(numberToBase(offset, base), n_layers)

      if n_layers == 1:
        curr_node = Node(dict(zip(pat[pat_start_idx:pat_stop_idx + 1], repeat(()))), l)

      else:
        lv_prev = make_leaf_nodes(offset_split[-1], step_split[-1], base, l)

        for i in range(2, n_layers):
          lv_prev = next_step(offset_split[-i:], step_split[-i:], lv_prev, base, l)

        lv_prev_it = iter(cycle(lv_prev))
        skip_elements(lv_prev_it, pat_start_idx)
        partial_pat = islice(lv_prev_it, pat_stop_idx + 1)
        assert(pat_start_idx <= pat_stop_idx)
        pat_ = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat[pat_start_idx:pat_stop_idx + 1]]

        curr_node = Node(dict(zip(pat_, partial_pat)), l)

    to_add.reverse()
    for e in to_add:
      curr_node = Node({e: curr_node}, l)

    return curr_node, l

  # make leaf layer

  if order(step, base) == 0:
    pat_it = iter(cycle(pat))
    lv1 = [Node(dict(zip(islice(pat_it, tk), repeat(()))), l) for tk in r1]

  else:
    n_paths = (last_number - start)/step + 1
    if n_paths < len(pat):
      print("this case")
      small_range = True
      # print("start idx", pat_start_idx, pat_stop_idx)
      lv1 = base_layer_with_offset2(start, step, last_number, base, l, pat_start_idx, pat_stop_idx, n_paths)
      separate_start_group = separate_stop_group = False


      start_group = 0
      stop_group = len(lv1) - 1

    else:
      small_range = False
      lv1 = base_layer_with_offset(offset, step, base, l)
  lv_prev = lv1

  # extra start node
  curr_start_node = None
  curr_start_idx = - (order(step, base) + 2)

  if separate_start_group:
    last_idx_start_group = pat_start_idx + r1[start_group] - (start_idx + 1)
    # lv1_start_node = Node(dict(zip(pat[pat_start_idx:last_idx_start_group + 1], repeat(()))), l)
    node_to_copy = lv1[start_group]
    part_of_pat = [to_size(numberToBase(p, base), (order(step, base) + 1))[-(order(step, base) + 1)] for p in pat[pat_start_idx:last_idx_start_group + 1]]

    lv1_start_node = Node({p: node_to_copy.cd[p] for p in part_of_pat}, l)
    curr_start_node = lv1_start_node

  # extra stop node
  curr_stop_node = None

  if separate_stop_group:
    first_idx_stop_group = pat_stop_idx - stop_idx
    # lv1_stop_node = Node(dict(zip(pat[first_idx_stop_group:pat_stop_idx + 1], repeat(()))), l)

    node_to_copy = lv1[stop_group]
    part_of_pat = [to_size(numberToBase(p, base), (order(step, base) + 1))[-(order(step, base) + 1)] for p in pat[first_idx_stop_group:pat_stop_idx + 1]]

    lv1_stop_node = Node({p: node_to_copy.cd[p] for p in part_of_pat}, l)

    curr_stop_node = lv1_stop_node


  # intermediate layers

  size_intermediate_layers.reverse()
  next_start_group = (start_group + 1) %len(r1)  # correct both with or without the modulo (without modulo, we might go through one cycle more of the previous level nodes)

  to_skip = next_start_group if separate_start_group else start_group

  std_nodes_ = len(r1)
  eq_stop_node = stop_group

  for i, nns in enumerate(size_intermediate_layers):

    lv_curr = []
    lv_prev_it = iter(cycle(lv_prev))

    skip_elements(lv_prev_it, to_skip)

    stop_groups_to_skip = (eq_stop_node - last_number_split_[curr_start_idx]) % std_nodes_
    if separate_start_group:
      nodes = [curr_start_node] + list(islice(lv_prev_it, base - start_split_[curr_start_idx] - 1))
      curr_start_node = Node(dict(zip(range(start_split_[curr_start_idx], base), nodes)), l)

    if not separate_start_group and start_split_[curr_start_idx] > 0:
      separate_start_group = True
      nodes = islice(lv_prev_it, base - start_split_[curr_start_idx])
      curr_start_node = Node(dict(zip(range(start_split_[curr_start_idx], base), nodes)), l)

    next_eq_stop_node = None
    first_node = next(lv_prev_it)
    peek_node = first_node

    for n in range(nns):
      d = dict(zip(range(base), [peek_node] + list(islice(lv_prev_it, base - 1))))
      if d[last_number_split_[curr_start_idx]] == lv_prev[eq_stop_node]:
        next_eq_stop_node = n
      lv_curr.append(Node(d, l))

      peek_node = next(lv_prev_it)
      if peek_node == first_node:
        break

    if next_eq_stop_node is None and not small_range:
      # This should never occur
      raise NotImplementedError("Unexpected condition: next_eq_stop_node should not be None.")

    lv_prev_it_stop = iter(cycle(lv_prev))
    skip_elements(lv_prev_it_stop, stop_groups_to_skip)

    if separate_stop_group:
      nodes = list(islice(lv_prev_it_stop, last_number_split_[curr_start_idx])) + [curr_stop_node]
      curr_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), nodes)), l)

    if not separate_stop_group and last_number_split[curr_start_idx] < base - 1:
      separate_stop_group = True
      nodes = islice(lv_prev_it_stop, last_number_split_[curr_start_idx] + 1)
      curr_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), nodes)), l)

    lv_prev = lv_curr

    curr_start_idx -= 1
    to_skip = 0
    std_nodes_ = std_nodes
    eq_stop_node = next_eq_stop_node


  # top layer

  lv_prev_it = iter(cycle(lv_prev))
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
  start, stop, step, base = (47, 91, 15, 10)


  rn, l = crange(start, stop, step, base)
  print("BASE", base)
  # print(repr(rn))

  # print(sorted(map(tuple, rn.paths())))
  r = [i for i in range(start, stop, step)]
  print("real  ", [to_number(i, base) for i in (sorted(map(tuple, rn.paths())))])
  print("wanted", r)
  # assert(r == [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
  print(len(r))
  # print(max(map(to_number, rn.paths())))

  print("#wanted: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))
  print("check: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))

  ns = (map(lambda x: to_number(list(x), base), rn.paths()))
  m = start % step
  for n in ns:
    if not n % step == m:
      print("INCORRECT NUMBERS from", n)
      break
  print()
  print_graph(l)

  print()
  print()
  print()

  # l_ = []
  # base_layer(125, 10, l_)
  # print_graph(l_)