---
slug: graph-valid-tree
---
## Q
**LC 261 Graph Valid Tree**｜Medium

`n` 个节点（`0..n-1`）和无向边列表 `edges`，判断这些边能否构成一棵树。

## A
**一句话。** 树等价于恰好 `n-1` 条边且无环：先查边数，再用并查集加边，两端已连通就是环。

```python
def valid_tree(n, edges):
    if len(edges) != n - 1:   # 多了有环，少了不连通
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # 路径折半
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:        # 两端已连通：成环
            return False
        parent[ra] = rb
    return True
```

**复杂度。** 时间 `O(n·α(n))`，空间 `O(n)`。

**易错点。**
- 只查无环：`n=4`，`[[0,1],[2,3]]` 无环但不连通。
- 只查连通：`n=3`，`[[0,1],[1,2],[0,2]]` 连通但有环，靠边数 `3 != 2` 拦下。

**追问。**
- 为什么边数对了再无环就一定连通？：`n` 个点 `n-1` 条边的无环图是森林，分量数 `n - (n-1) = 1`。
- 要返回多余的那条边（LC 684）？：并查集遇到成环的边直接返回它。

**同模式。** LC 323 无向图中连通分量的数目、LC 684 冗余连接、LC 547 省份数量、LC 1319 连通网络的操作次数
