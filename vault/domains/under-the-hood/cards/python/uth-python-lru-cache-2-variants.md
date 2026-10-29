---
id: uth-python-lru-cache-2-variants
node: python.lru-cache
type: qa
step: 2
---
## Q
**lru_cache 的三种模式**｜Python · CPython 3.14

`lru_cache(maxsize=None)`、`maxsize=0`、`functools.cache` 内部分别走什么路径？缓存的 key 是什么？

## A
**背景。** 淘汰要靠链表维护使用顺序，每次命中都要动一下链表。如果根本不打算淘汰，这笔开销就白花了。

**结构。** 创建时按 `maxsize` 选三个包装函数之一：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<rect x="90" y="14" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lru_cache(maxsize=?)</text>
<line x1="170" y1="42" x2="60" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="60.0,100.0 63.3,95.5 65.6,99.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="100" width="100" height="50" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="60" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dict</text>
<text x="60" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不淘汰</text>
<line x1="170" y1="42" x2="170" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,100.0 167.5,95.0 172.5,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="100" width="100" height="50" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">不缓存</text>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">直接调用</text>
<line x1="170" y1="42" x2="280" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,100.0 274.4,99.9 276.7,95.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="230" y="100" width="100" height="50" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="280" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dict + 链表</text>
<text x="280" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">淘汰最旧</text>
<text x="70" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">None</text>
<text x="184" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="272" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">n</text>
</svg>
```

**细节。**

- `maxsize=None`：只用 `dict`，没有链表，也不淘汰，更快。`functools.cache` 就是 `lru_cache(maxsize=None)`。
- `maxsize=0`：不缓存，直接调用原函数。
- key 是位置参数元组（带关键字参数时再拼上分隔标记）；只有一个 `int` 或 `str` 参数时，直接拿它当 key，省掉一个元组。

**为什么。** 无限缓存不用维护顺序，省掉每次命中的链表操作。

**坑。** 参数必须可哈希（能算出哈希值），传 `list` 会抛 `TypeError: unhashable type: 'list'`。

**例题：** LC 509 斐波那契数

`F(0) = 0`，`F(1) = 1`，`F(n) = F(n-1) + F(n-2)`，给 `n`，求 `F(n)`。`0 <= n <= 30`。

```python
from functools import cache

def fib(n: int) -> int:
    @cache
    def helper(k: int) -> int:
        return k if k < 2 else helper(k - 1) + helper(k - 2)

    return helper(n)
```
