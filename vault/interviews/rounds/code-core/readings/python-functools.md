---
nodes: [python.stdlib, python.idioms, performance.amortized]
url: https://docs.python.org/3/library/functools.html
tags: [docs]
---
# functools — higher-order functions and operations on callables

`@cache` turns an exponential recursion into a polynomial one with one line,
which makes this page the highest-leverage single import in a timed round. The
documentation is also explicit about the two preconditions people skip:
arguments must be hashable, and the function must be pure. Everything else on
the page — `cmp_to_key`, `partial`, `reduce`, `total_ordering` — is a
minutes-saver you should be able to reach for without a search.

**Extract on read:**
- `@cache` vs `@lru_cache(maxsize=...)`, and `cache_info()` for checking the
  memo is actually hitting.
- `cmp_to_key` as the escape hatch when the order is not a function of one item,
  and why a real `key=` is cheaper ([[cc-python-idioms-sorted-key-mechanics]]).
- `total_ordering` to get all six comparisons from `__eq__` and `__lt__`.

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/functools.html)

## Archived copy
![[python-functools-clip]]
%% trellis:end %%
