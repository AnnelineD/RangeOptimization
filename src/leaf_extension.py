from itertools import cycle, islice, takewhile, accumulate

from src.base_calc import to_number, to_size, numberToBase
from src.node import Node
from src.pattern import pattern, repetition_offset


def make_leaf_nodes(start, step, base, l, n_steps = None):
  assert start < base
  assert step < base

  pat = pattern(step, start, base)
  if n_steps and len(pat) > n_steps:
      pat = pat[:n_steps]

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


def next_step2(start_split, step_split, prev_nodes, base, l, start_idx, stop_idx, n_steps):
  prev_step = to_number(step_split[1:], base)

  if prev_step == 0:
    pat = pattern(step_split[0], start_split[0], base)
  else:
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base**len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]

  if len(pat) > n_steps:
      pat = pat[:n_steps]

  empty_start = []
  # if len(pat) > n_steps:
  #     if start_idx < stop_idx:
  #         pat = pat[start_idx:(stop_idx + 1)]
  #     if stop_idx < start_idx:
  #         pat = pat[start_idx:] + pat[:(stop_idx + 1)]
  #     empty_start = [None]*start_idx

  # print("pat 2", pat)

  lv_prev_it = iter(cycle(prev_nodes))
  # skip_elements(lv_prev_it, start_idx)
  return [Node({p: next(lv_prev_it)}, l) for p in pat]



def last_layer(start_split, step_split, prev_nodes, base, l):
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]
    r = repetition_offset(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))

    pat_it = iter(cycle(pat))
    lv_prev_it = iter(cycle(prev_nodes))
    return [Node(dict(zip(islice(pat_it, tk), islice(lv_prev_it, tk))), l) for tk in r]


def last_layer2(start_split, step_split, stop_split, prev_nodes, base, l, start_idx, stop_idx, n_steps):
    pat_full = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))
    pat = [to_size(numberToBase(i, base), len(step_split))[0] for i in pat_full]
    assert len(pat) > n_steps



    # if len(pat) > n_steps:
    #    print("this case")
    #     if start_idx < stop_idx:
    #        pat = pat[start_idx:(stop_idx + 1)]
    #     if stop_idx < start_idx:
    #         pat = pat[start_idx:] + pat[:(stop_idx + 1)]


    # print("new last pat", pat)
    r = repetition_offset(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))

    if len(pat) > n_steps:
        pat = pat[:int(n_steps)]
        num_groups = list(takewhile(lambda x: x[1] <= len(pat), enumerate(accumulate(r))))[-1][0] + 1
        r = r[:num_groups]
        assert len(pat) >= len(r)
        if len(pat) != sum(r):
            r.append(len(pat) - sum(r))
        assert(len(pat) == sum(r))

    # print("start", pat_full[start_idx])
    # print("stop", to_number(stop_split[-(len(step_split)):], base))
    # start_g, start_gi = find_group(pat_full, r, pat_full[start_idx])
    # stop_g, stop_gi = find_group(pat_full, r, to_number(stop_split[-(len(step_split)):], base))
    #
    # print("groups", start_g, stop_g)
    # if start_g <= stop_g:
    #     r_ = r[start_g:(stop_g + 1)]
    # else:
    #     r_ = r[start_g:] + r[:stop_g + 1]
    # r_[0] = r_[0] - start_gi
    # r_[-1] = stop_gi + 1
    #
    # print("pats", pat)
    # print("new reps", r_)
    # # r_ = [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2]
    #
    pat_it = iter(cycle(pat))
    lv_prev_it = iter(cycle(prev_nodes))
    # skip_elements(lv_prev_it, start_idx)

    return [Node(dict(zip(islice(pat_it, tk), islice(lv_prev_it, tk))), l) for tk in r]