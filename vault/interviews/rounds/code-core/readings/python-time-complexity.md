---
nodes: [performance, toolbox]
url: https://wiki.python.org/moin/TimeComplexity
tags: [canonical]
---
# TimeComplexity (Python Wiki)

One table per built-in container giving the average and worst-case cost of every
operation: `list`, `collections.deque`, `set` and `dict`. This is the page that
settles arguments before they start — `x in list` is O(n) and `x in set` is
O(1), `list.pop(0)` is O(n) and `deque.popleft()` is O(1), `list.insert` is O(n),
`sort` is O(n log n). Memorising the four tables removes most of the guesswork
from choosing a structure at minute five.

**Extract on read:**
- `list` versus `deque` at the two ends, and why `pop(0)` in a loop is quadratic
  ([[cc-performance-amortized-append-doubling]]).
- `dict`/`set` amortized O(1) lookup, insert and delete — and the worst case.
- The costs that justify picking the structure before coding rather than after
  ([[cc-performance-budget-decide-before-coding]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://wiki.python.org/moin/TimeComplexity)

## Archived copy
![[python-time-complexity-clip]]
%% trellis:end %%
