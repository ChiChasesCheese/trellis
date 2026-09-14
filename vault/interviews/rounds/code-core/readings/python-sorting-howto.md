---
nodes: [python.idioms, output.ordering, toolbox.sorted]
url: https://docs.python.org/3/howto/sorting.html
tags: [docs, canonical]
---
# Sorting Techniques (Python HOWTO)

The single best short text on getting a total order right in Python. It covers
key functions, `operator.itemgetter`/`attrgetter`, `reverse=`, and — the part
worth the whole read — how to sort by several keys in different directions using
the guaranteed stability of `list.sort`. It ends with the decorate-sort-undecorate
pattern and the note that `cmp_to_key` exists but costs a Python call per
comparison.

**Extract on read:**
- Composite tuple keys, and negation as the only way to reverse a single numeric
  component ([[cc-python-idioms-sorted-key-mechanics]]).
- Stability as a guarantee you can build on: sort by the minor key first, then
  the major one.
- `itemgetter(1, 0)` as a faster `lambda`, and why `key=` allocates one object
  per element ([[cc-performance-memory-sort-key-cost]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/sorting.html)

## Archived copy
![[python-sorting-howto-clip]]
%% trellis:end %%
