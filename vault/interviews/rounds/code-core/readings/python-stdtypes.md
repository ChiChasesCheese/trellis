---
nodes: [python, input.normalization]
url: https://docs.python.org/3/library/stdtypes.html
tags: [docs]
---
# Built-in Types

The reference for `str`, `list`, `dict`, `set` and `int` — the five types a
timed solution is almost entirely made of. Most people never read the string
method table in full and then hand-roll `partition`, `removeprefix`,
`casefold` or `str.translate`. It is also the page that documents dict view
objects, the guaranteed insertion order of `dict`, and the exact semantics of
slicing, all of which decide whether an idiom is O(1) or O(n).

**Extract on read:**
- The `str` method table: `strip`/`casefold`/`partition`/`removeprefix`/`translate`
  — normalization done in one call instead of five.
- `dict` views (`keys`, `items`) are lazy and support O(1) membership; `list(d)`
  is a copy ([[cc-performance-hot-loop-membership-in-list]]).
- Set operations (`|`, `&`, `-`, `<=`) as one-line replacements for a loop.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/stdtypes.html)

## Archived copy
![[python-stdtypes-clip]]
%% trellis:end %%
