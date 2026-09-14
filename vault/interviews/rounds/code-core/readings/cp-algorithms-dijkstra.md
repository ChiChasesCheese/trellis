---
nodes: [algorithms.shortest-path]
url: https://cp-algorithms.com/graph/dijkstra.html
tags: [canonical]
---
# Dijkstra's algorithm (cp-algorithms)

Read it for the invariant, not the code: once a vertex is popped with the
smallest tentative distance, that distance is final — which is exactly the
property that breaks when a problem adds a hop limit or a negative edge, and
knowing why tells you when to reach for Bellman-Ford instead. The page also
covers the sparse-graph version with a priority queue and path reconstruction
via parent pointers.

**Extract on read:**
- The greedy invariant and the two conditions that void it (negative weights, a
  bound on the number of edges used).
- The heap version with lazy stale entries — the same pattern as
  [[cc-performance-amortized-lazy-heap]].
- Reconstructing the path from parent pointers, and where a deterministic
  tie-break has to be inserted.

%% trellis:begin %%
## Source
[Open the original ↗](https://cp-algorithms.com/graph/dijkstra.html)

## Archived copy
![[cp-algorithms-dijkstra-clip]]
%% trellis:end %%
