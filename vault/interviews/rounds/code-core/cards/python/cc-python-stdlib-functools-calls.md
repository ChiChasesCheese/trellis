---
id: cc-python-stdlib-functools-calls
node: python.stdlib
type: qa
---
## Q
Memoize a recursive function, sort by a rule that is not expressible as a key, and freeze one argument of a function. Which `functools` calls, and what does each require of you?

## A
```python
from functools import cache, lru_cache, cmp_to_key, reduce, partial
@cache                                   # unbounded memo (3.9+); lru_cache(maxsize=None) before
def solve(state): ...
rows.sort(key=cmp_to_key(compare))       # last resort
total = reduce(operator.add, xs, 0)
to_hex = partial(int, base=16)
```

- `@cache` needs **hashable** arguments and a **pure** function — memoizing something that reads mutable state is a stale-read bug ([[cc-performance-amortized-cache-derived]]).
- It turns an exponential recursion into a polynomial one in one line; raise `sys.setrecursionlimit` if depth may pass 1000.
- Prefer a real `key=` over `cmp_to_key`: a key sorts in C, a comparator adds a wrapper object *and* a Python call per comparison.

## Q zh
给递归函数加记忆化、按一个无法写成 key 的规则排序、以及固定函数的一个参数。用哪些 `functools` 调用？各自对你有什么要求？

## A zh
```python
from functools import cache, lru_cache, cmp_to_key, reduce, partial
@cache                                   # 无界记忆化（3.9+）；更早版本用 lru_cache(maxsize=None)
def solve(state): ...
rows.sort(key=cmp_to_key(compare))       # 最后手段
total = reduce(operator.add, xs, 0)
to_hex = partial(int, base=16)
```

- `@cache` 要求参数**可哈希**、函数**纯粹** —— 给读取可变状态的东西加记忆化就是一个读到陈旧值的 bug（[[cc-performance-amortized-cache-derived]]）。
- 它一行就能把指数级递归变成多项式级；深度可能超过 1000 时要调高 `sys.setrecursionlimit`。
- 优先用真正的 `key=` 而不是 `cmp_to_key`：key 在 C 里排序，比较器则每次比较都多一个包装对象**和**一次 Python 调用。
