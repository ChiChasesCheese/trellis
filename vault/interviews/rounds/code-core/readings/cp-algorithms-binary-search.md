---
nodes: [algorithms.binary-search]
url: https://cp-algorithms.com/num_methods/binary_search.html
tags: [canonical]
---
# Binary search (cp-algorithms)

The page that makes binary search boring, which is the goal. It frames the
search as maintaining an invariant over a half-open interval rather than as a
loop template to memorize, then generalizes from "find a value in an array" to
"find the smallest answer for which a monotone predicate holds" — the form that
actually shows up when a problem asks for a minimum capacity, a maximum rate or
the earliest feasible time.

**Extract on read:**
- The loop invariant that makes the off-by-one impossible, rather than a
  template you hope you remembered right.
- Searching on the answer space: define `feasible(x)`, prove it is monotone,
  binary search it.
- The real-valued variant and why a fixed iteration count beats an epsilon
  comparison ([[cc-python-pitfalls-float-equality]]).

%% trellis:begin %%
## Source
[Open the original ↗](https://cp-algorithms.com/num_methods/binary_search.html)

## Archived copy
![[cp-algorithms-binary-search-clip]]
%% trellis:end %%
