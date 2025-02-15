from collections import deque
from itertools import islice
from math import gcd

from src.base_calc import order

def skip_elements(iterator, count):
  deque(islice(iterator, count), maxlen=0)


def find_last_number_of_range(start, stop, step):
  rem = stop%step
  offset = start%step
  return stop + offset - rem - (step if offset >= rem else 0)

def find_group(l, group_division, n):
  idx = l.index(n)

  p = 0
  for g_number, g_size in enumerate(group_division):
    g_place = idx - p
    p += g_size
    if p > idx:
      return g_number, g_place


def strip_equal_start(l1: list, l2: list) -> tuple[list, list, list]:
  start = []

  for i in range(len(l1)):
    if l1[i] == l2[i]:
      start.append(l1[i])
    else:
      break

  return l1[i:], l2[i:], start



def number_of_nodes_per_layer(start: list, last_n: list, step: int, base):
  assert(len(start) == len(last_n))

  upper_layer_edges = last_n[0] - start[0] + 1  # number of edges starting from top node

  num_nodes = int(step/gcd(base**(order(step, base) + 1), step))  # ??
  upper_layer_nodes = min(upper_layer_edges, num_nodes)

  num_intermediate_layers = (len(last_n) - 1) - order(step, base) - 1
  if num_intermediate_layers <= 0:
    return []
  size_intermediate_layers = [upper_layer_nodes]  # number of nodes in each layer

  prev_layer_nodes = upper_layer_nodes
  for l in range(num_intermediate_layers - 1):
    curr_layer_edges = prev_layer_nodes * base
    curr_layer_nodes = min(curr_layer_edges, num_nodes)
    size_intermediate_layers.append(curr_layer_nodes)
    prev_layer_nodes = curr_layer_nodes

  return size_intermediate_layers

# def how_many_cicles(boxes, arrows, box_nr, arrow_nr):
#   for i in range(100):
#     if (i*arrows + arrow_nr)%boxes == box_nr:
#       return i
#
# assert(how_many_cicles(3, 4, 1, 1) == 0)
# assert(how_many_cicles(3, 4, 0, 1) == 2)
# assert(how_many_cicles(3, 10, 2, 9) == 2)
# assert(how_many_cicles(3, 10, 2, 4) == 1)