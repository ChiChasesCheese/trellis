---
nodes: [python.stdlib, python.idioms, algorithms.backtracking]
url: https://docs.python.org/3/library/itertools.html
tags: [docs]
---
# itertools — functions creating iterators for efficient looping

The enumeration toolkit: `combinations`, `permutations`, `product`, plus the
streaming helpers `accumulate`, `groupby`, `pairwise` and `chain`. Read the
table at the top and then the entry for `groupby`, whose one precondition —
input must already be sorted by the grouping key — silently produces wrong
answers rather than errors. The "Itertools Recipes" section at the bottom is a
small library of things you would otherwise write badly under time pressure.

**Extract on read:**
- `groupby` groups only *adjacent* equal keys, and its group iterator is
  invalidated when you advance ([[cc-python-stdlib-itertools-calls]]).
- `accumulate(values, initial=0)` as a prefix-sum array in one call.
- `product(range(2), repeat=n)` and `combinations` for exhaustive enumeration
  when the constraint says n is small.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/itertools.html)

## Archived copy
![[python-itertools-clip]]
%% trellis:end %%
