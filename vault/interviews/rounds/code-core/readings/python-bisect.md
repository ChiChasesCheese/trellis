---
nodes: [python.stdlib, toolbox.sorted, chrono.intervals]
url: https://docs.python.org/3/library/bisect.html
tags: [docs]
---
# bisect — array bisection algorithm

Five functions, one page, and the difference between two of them decides
whether an inclusive boundary is right. `bisect_left` returns the first index
whose value is not less than the target; `bisect_right` the first index whose
value is greater. They differ only on an exact hit — which is exactly where a
"within the last hour" or "up to and including" rule lives. The searching-sorted-lists
recipes at the end of the page are worth copying into your own notes.

**Extract on read:**
- `bisect_left` vs `bisect_right`, and range counting as the difference of two.
- `insort` — O(log n) to find the position, O(n) to shift; when re-sorting wins.
- The `key=` parameter (3.10+), and why neither function works on a descending list.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/bisect.html)

## Archived copy
![[python-bisect-clip]]
%% trellis:end %%
