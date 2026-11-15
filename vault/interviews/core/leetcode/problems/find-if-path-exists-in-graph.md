---
slug: find-if-path-exists-in-graph
---
## Q
**LC 1971 寻找图中是否存在路径**｜Easy

有 `n` 个顶点（编号 `0` 到 `n-1`）的双向图，`edges` 给出所有边。问是否存在从 `source` 到 `destination` 的路径。

## A
**一句话。** 建邻接表后做 DFS，从 `source` 出发能走到 `destination` 就返回 `True`；`seen` 数组防止走回头路。

```python
def valid_path(n, edges, source, destination):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)
    seen = [False] * n

    def dfs(u):
        if u == destination:
            return True
        seen[u] = True
        return any(dfs(v) for v in g[u] if not seen[v])

    return dfs(source)
```

**复杂度。** 时间 `O(n + e)`，空间 `O(n + e)`。

**易错点。**
- 图是双向的：每条边要在两个端点的邻接表里各存一次。
- 不标记访问：有环时无限递归。
- `source == destination`：不用走边，直接返回 `True`，上面的 DFS 已经覆盖。

**追问。**
- 递归深度太大怎么办？：改用并查集，合并所有边后比较 `find(source)` 和 `find(destination)`。

**同模式。** LC 547 省份数量、LC 323 无向图中连通分量的数目、LC 797 所有可能的路径
