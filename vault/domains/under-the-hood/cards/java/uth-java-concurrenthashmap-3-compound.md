---
id: uth-java-concurrenthashmap-3-compound
node: java.concurrenthashmap
type: qa
step: 3
---
## Q
**ConcurrentHashMap 用起来的两个坑**｜Java · OpenJDK 25

为什么 `ConcurrentHashMap` 不允许 `null`？在 `computeIfAbsent` 里递归算斐波那契会怎样？

## A
**背景。** `computeIfAbsent(k, f)` 的意思是「没有 k 就调用 `f` 算一个放进去」。它在持有桶锁期间执行你传入的函数。这对记忆化（把算过的结果存起来）很诱人，但函数里又去改同一张表，就会出事。

**结构。** 每个桶头节点一把 `synchronized` 锁；函数在持锁期间执行。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="55" y="22" width="230" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">computeIfAbsent(5) 持桶锁</text>
<rect x="55" y="80" width="230" height="32" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fib(4) 又来改同一张表</text>
<rect x="55" y="138" width="230" height="32" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">IllegalStateException</text>
<line x1="170" y1="54" x2="170" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,80.0 167.0,74.0 173.0,74.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="170" y1="112" x2="170" y2="138" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="170.0,138.0 167.0,132.0 173.0,132.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="182" y="72" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">函数在持锁时运行</text>
<text x="182" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">占位节点检测到重入</text>
</svg>
```

**细节。**

- key 和 value 都不能是 `null`，`put` 开头直接抛 `NullPointerException`（实测）。并发下 `get` 返回 `null` 就无法区分「没有」和「值为 null」。
- 递归 `computeIfAbsent(n, k -> fib(k-1) + fib(k-2))` 实测抛 `IllegalStateException: Recursive update`。
- 单个原子方法（`putIfAbsent`、`merge`）是安全的，先 `get` 再 `put` 的组合不是原子的。

**为什么。** 函数在持锁时执行，再改同一个桶会破坏结构，所以源码用占位节点（`ReservationNode`）检测重入并直接报错。

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
