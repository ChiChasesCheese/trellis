---
nodes: [toolbox.union-find]
url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
tags: [canonical]
---
# Disjoint Set Union (cp-algorithms)

Twenty lines of code that solve a surprising share of assessment problems:
anything phrased as "these two records share an identifier, group everything
transitively connected". The page builds it from the naive version to path
compression plus union by size, states the near-constant amortized bound, and
then covers the applications — connected components, cycle detection in an
undirected graph, and offline queries.

**Extract on read:**
- The two optimizations and why both are needed for the amortized bound.
- Storing set size or a per-set aggregate in the root, so a query is O(1).
- Modelling "shared attribute" links as edges, which is what turns a record
  linking problem into a components problem.

%% trellis:begin %%
## Source
[Open the original ↗](https://cp-algorithms.com/data_structures/disjoint_set_union.html)

## Archived copy
![[cp-algorithms-dsu-clip]]
%% trellis:end %%
