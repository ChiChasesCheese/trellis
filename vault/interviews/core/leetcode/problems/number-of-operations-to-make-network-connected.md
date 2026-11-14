---
slug: number-of-operations-to-make-network-connected
---
## Q
**LC 1319 连通网络的操作次数**｜Medium

`n` 台电脑由网线 `connections` 相连，每次可拔一根线接到别处，求让全网连通的最少次数，不可能返回 `-1`。

## A
**一句话。** 线少于 `n - 1` 根不可能；否则冗余线一定够用，答案是连通分量数减一，用并查集数分量。

```python
def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1
    fa = list(range(n))

    def find(x):
        while fa[x] != x:
            fa[x] = fa[fa[x]]    # 路径压缩
            x = fa[x]
        return x

    parts = n
    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            fa[ra] = rb
            parts -= 1
    return parts - 1
```

**复杂度。** 时间 `O((n + m) α(n))`，空间 `O(n)`。

**易错点。**
- 去数冗余边再比较：边数 `≥ n - 1` 时冗余边一定 `≥` 分量数 - 1，不必单独数。
- 返回分量数：连接 `c` 个分量只要 `c - 1` 根线。

**追问。**
- 用 DFS？：建邻接表，对未访问的点各做一次 DFS，次数就是分量数。
- 为什么线够就一定能连通？：`c` 个分量最少用 `n - c` 根线，多出的 `m - (n - c) ≥ c - 1` 根都是冗余的。

**同模式。** LC 547 省份数量、LC 323 无向图中连通分量的数目、LC 684 冗余连接
