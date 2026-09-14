---
nodes: [python.stdlib, toolbox.hash, model.index, rules.grouping]
url: https://docs.python.org/3/library/collections.html
tags: [docs]
---
# collections — container datatypes

The four types that carry most timed-round state: `defaultdict`, `Counter`,
`deque` and `namedtuple`. Read it once properly rather than looking up
`most_common` for the fifth time mid-round. The page is short, and the parts
that matter are the method tables — in particular the exact behaviour of a
missing key, which is where the two most common bugs live: `defaultdict`
inserting on read, and `Counter` returning zero without inserting.

**Extract on read:**
- `defaultdict(list)` versus `dict.setdefault` versus `dict.get` — which of the
  three mutates on a lookup ([[cc-python-idioms-setdefault-vs-defaultdict]]).
- `Counter.most_common(k)`, `Counter` arithmetic (`+`, `-`, `&`, `|`) as
  multiset operations, and `total()`.
- `deque(maxlen=n)` as a free fixed-size window, and O(1) `appendleft`/`popleft`.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/collections.html)

## Archived copy
![[python-collections-clip]]
%% trellis:end %%
