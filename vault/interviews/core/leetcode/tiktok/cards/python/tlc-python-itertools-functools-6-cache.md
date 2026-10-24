---
id: tlc-python-itertools-functools-6-cache
node: python.itertools-functools
type: qa
step: 6
---
## Q
**Python 工具箱｜`functools.cache`**

`@cache` 把递归变成记忆化搜索，要满足什么条件？它的内存和失效是怎样的？和 `lru_cache` 有什么区别？

## A
`@functools.cache`（3.9+）等价于 `@lru_cache(maxsize=None)`：用「参数元组」做键缓存返回值，同样参数第二次调用直接取。

```python
from functools import cache
@cache
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
print(fib(80))             # 23416728348467685
print(fib.cache_info())    # CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)
fib.cache_clear()          # 清空，把状态还原
```

- 条件：函数是**纯函数**（返回值只由参数决定），且参数**可哈希**。传 `list` 会 `TypeError: unhashable type: 'list'`，需要先转成 `tuple` 或用下标代替。
- 状态数 = 不同参数的个数；时间 = 状态数 × 单个状态的转移成本。把「状态」选成 `(i, j)` 这样的小整数元组，是 DP 题用 `@cache` 的关键（LC 72、139、322）。
- `maxsize=None` 无上限，状态上百万时内存会爆；`lru_cache(maxsize=N)` 保留最近 `N` 个，`maxsize` 要是 2 的幂时最快。
- 缓存会在多个测试用例之间保留；在 LeetCode 的类方法里，用 `@cache` 修饰带 `self` 的方法会把 `self` 也算进键，并让对象无法被回收，改写成方法内部的嵌套函数更安全。
- 递归深度仍受 `sys.getrecursionlimit()` 约束，深度到 `10^4` 以上要改自底向上的递推（见递归与记忆化一组）。
