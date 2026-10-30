---
id: uth-python-functions-decorators-4-decorator-args
node: python.functions-decorators
type: qa
step: 4
---
## Q
**@lru_cache(maxsize=None) 为什么多了一层括号**｜Python · CPython 3.14

`@cache` 不带括号，`@lru_cache(maxsize=None)` 带参数。带参数的装饰器里面套了几层函数？

## A
**背景。** `@` 后面必须是一个「收一个函数、返回一个函数」的东西。可你还想在装饰时传参数（缓存多大），这些参数得先找个地方放。

**结构。** `@lru_cache(maxsize=None)` 先执行 `lru_cache(maxsize=None)`，它返回一个装饰器 `decorating_function`，再用这个装饰器去装饰函数。一共三层：参数层、装饰器层、wrapper 层。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 195">
<rect x="20" y="14" width="300" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">lru_cache(maxsize=None)</text>
<line x1="170" y1="42" x2="170" y2="70" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,70.0 167.0,64.0 173.0,64.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="180" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">返回</text>
<rect x="20" y="72" width="300" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">decorating_function 真正的装饰器</text>
<line x1="170" y1="100" x2="170" y2="128" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,128.0 167.0,122.0 173.0,122.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="180" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">用它装饰 f</text>
<rect x="20" y="130" width="300" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">wrapper 替换 f 的新函数</text>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">参数层  装饰器层  wrapper 层</text>
</svg>
```

**细节。**

- 源码里 `lru_cache(maxsize=128, typed=False)` 的最后一行是 `return decorating_function`。
- `wraps` 自己就是带参数的装饰器：`wraps(f)` 返回 `partial(update_wrapper, wrapped=f, ...)`。
- 3.8 起 `@lru_cache` 也可以不带括号：发现第一个参数是可调用对象，就直接把它当作被装饰的函数。

**为什么。** 装饰器语法只认「一个函数进、一个函数出」，多出来的参数只能靠闭包再包一层。

**例题：** LC 1140 石子游戏 II

一排石子堆 `piles`，Alice 先手，当前可以取走前 `X` 堆（`1 <= X <= 2M`），然后 `M = max(M, X)`，双方都取最优，求 Alice 最多能得到的石子数。`1 <= piles.length <= 100`。

```python
from functools import lru_cache
from itertools import accumulate

def stone_game_ii(piles: list[int]) -> int:
    n = len(piles)
    suffix_sum = list(accumulate(piles[::-1]))[::-1] + [0]

    @lru_cache(maxsize=None)
    def best(i: int, limit: int) -> int:
        if i + 2 * limit >= n:
            return suffix_sum[i]
        return max(
            suffix_sum[i] - best(i + take, max(limit, take))
            for take in range(1, 2 * limit + 1)
        )

    result = best(0, 1)
    best.cache_clear()
    return result
```
