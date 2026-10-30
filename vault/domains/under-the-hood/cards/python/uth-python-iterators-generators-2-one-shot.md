---
id: uth-python-iterators-generators-2-one-shot
node: python.iterators-generators
type: qa
step: 2
---
## Q
**迭代器为什么只能走一遍**｜Python · CPython 3.14

`m = map(str, [1, 2])`，连着 `list(m)` 两次，第二次为什么是空的？为什么列表却能 `for` 很多遍？

## A
**背景。** 游标是有状态的：走到哪了，记在它自己身上。想遍历两遍，就需要两个游标。

**结构。** 列表这类可迭代对象，每次 `iter()` 都新建一个游标，互不影响。而 `map`、`zip`、文件、生成器本身**就是**游标，`iter()` 它们返回的是它们自己，走完就空了，不会倒带。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="90" y="30" width="60" height="28" rx="3"/>
<rect x="150" y="30" width="60" height="28" rx="3"/>
<rect x="210" y="30" width="60" height="28" rx="3"/>
<rect x="90" y="130" width="60" height="28" rx="3"/>
<rect x="150" y="130" width="60" height="28" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="120" y1="12" x2="120" y2="30"/>
<line x1="240" y1="82" x2="240" y2="58"/>
<line x1="250" y1="116" x2="214" y2="142"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="120.0,30.0 117.0,24.0 123.0,24.0"/>
<polygon points="240.0,58.0 243.0,64.0 237.0,64.0"/>
<polygon points="214.0,142.0 217.1,136.1 220.6,140.9"/>
</g>
<g fill="currentColor">
<text x="120" y="48">a</text>
<text x="180" y="48">b</text>
<text x="240" y="48">c</text>
<text x="170" y="100">iter(L) 每次新建一个游标</text>
<text x="120" y="148">1</text>
<text x="180" y="148">2</text>
<text x="170" y="190">它自己就是游标: 走完不倒带</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="40" y="49">列表 L</text>
<text x="40" y="149">map 对象</text>
<text x="170" y="207">list(m) 第二次得到 []</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="128" y="20" text-anchor="start" font-size="11">游标 1</text>
<text x="248" y="78" text-anchor="start" font-size="11">游标 2</text>
<text x="256" y="116" text-anchor="start" font-size="11">游标已在末尾</text>
</g>
</g>
</svg>
```

```python
m = map(str, [1, 2])
list(m)   # ['1', '2']
list(m)   # []
```

**细节。**

- 实测 `iter(it) is it` 为 `True`；已经走完的迭代器再 `next()`，每次都抛 `StopIteration`。
- 惯用法 `next(iter(s))`：新建一个游标，只取一个元素就丢掉，不必先把集合转成列表。

**为什么。** 迭代器不存元素，只存位置，所以省内存；代价是不能回头。

**坑。** 把 `zip(...)`、`map(...)` 的结果存进变量，用了两遍，第二遍什么都没有。需要两遍时，先用 `list()` 固定下来。

**例题：** LC 2603 收集树中金币

无向无根树有 `n` 个节点，`coins[i]` 为 1 表示该点有金币。可以走边，也可以原地收集距离不超过 2 的金币，收完要回到出发点，求最少走过的边数（重复走同一条边每次都算）。`1 <= n <= 3 * 10^4`。

```python
def minimum_edges_to_collect_coins(coins: list[int], edges: list[list[int]]) -> int:
    n = len(coins)
    if n <= 1:
        return 0
    adj: list[set[int]] = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)

    leaves = [v for v in range(n) if len(adj[v]) == 1 and coins[v] == 0]
    while leaves:
        v = leaves.pop()
        if not adj[v]:
            continue
        u = next(iter(adj[v]))
        adj[u].discard(v)
        adj[v].discard(u)
        if len(adj[u]) == 1 and coins[u] == 0:
            leaves.append(u)

    for _ in range(2):
        layer = [v for v in range(n) if len(adj[v]) == 1]
        for v in layer:
            if not adj[v]:
                continue
            u = next(iter(adj[v]))
            adj[u].discard(v)
            adj[v].discard(u)

    remaining_edges = sum(len(nbrs) for nbrs in adj) // 2
    return remaining_edges * 2
```
