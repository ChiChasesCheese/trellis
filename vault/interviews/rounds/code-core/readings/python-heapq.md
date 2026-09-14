---
nodes: [python.stdlib, toolbox.heap]
url: https://docs.python.org/3/library/heapq.html
tags: [docs]
---
# heapq — heap queue algorithm

Python's priority queue is a plain list plus six functions, and the module page
is the whole API. Worth reading end to end because the two techniques an
assessment actually needs — tuple keys for deterministic tie-breaks, and the
absence of decrease-key — are consequences of that design rather than features
you can look up by name. The "Priority Queue Implementation Notes" section at
the bottom is the part most people never reach and the part that matters.

**Extract on read:**
- `heappush` / `heappop` / `heapify` / `heapreplace` / `heappushpop` and which
  of the last two pops first.
- `nlargest` / `nsmallest` with `key=` as a top-k that avoids a full sort.
- The notes on removed and changed entries — the lazy-invalidation pattern in
  [[cc-performance-amortized-lazy-heap]] is straight out of them.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/heapq.html)

## Archived copy
![[python-heapq-clip]]
%% trellis:end %%
