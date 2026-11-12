---
slug: is-graph-bipartite
---
## Q
**LC 785 判断二分图**｜Medium

无向图（可能不连通）用邻接表 `graph` 给出，判断能否把节点分成两组，使每条边的两端分属不同组。

## A
**一句话。** 两色 DFS 染色：邻居必须染相反色，遇到同色邻居就是奇环，每个连通分量各染一次。

```python
def is_bipartite(graph):
    n = len(graph)
    color = [0] * n               # 0 未染色，1 / -1 两组

    def dfs(u, c):
        color[u] = c
        for v in graph[u]:
            if color[v] == c:     # 同色：奇环
                return False
            if color[v] == 0 and not dfs(v, -c):
                return False
        return True

    for s in range(n):            # 每个连通分量
        if color[s] == 0 and not dfs(s, 1):
            return False
    return True
```

**复杂度。** 时间 `O(n+E)`，空间 `O(n)`。

**易错点。**
- 只从节点 `0` 出发：不连通时其余分量没检查，`[[1],[0],[3,4],[2,4],[2,3]]` 后半是三角形，应为 `false`。
- 只处理未染色邻居、不检查已染色邻居的冲突：奇环发现不了。

**追问。**
- 要给出一种划分？：保留 `color`，`1` 是一组，`-1` 是另一组。
- `n` 很大会递归过深吗？：会，改用 BFS 染色。

**同模式。** LC 886 可能的二分法、LC 207 课程表、LC 684 冗余连接、LC 1042 不邻接植花
