---
slug: tt-all-simple-paths
---
## Q
**枚举有向图中的所有简单路径（含环的情况）**｜Medium

有向图（`n ≤ 15` 个点，可能有环）、起点 `s`、终点 `t`，返回 `s` 到 `t` 的所有简单路径（点不重复）。

## A
**一句话。** 回溯 DFS：用 `on_path` 标记当前路径上的点，进入时标记、退出时撤销；先从 `t` 反向 BFS 剪掉到不了 `t` 的点。

```python
def all_simple_paths(n, edges, s, t):
    g = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        rev[v].append(u)

    reach = [False] * n          # 剪枝：反向 BFS 求能到 t 的点
    reach[t] = True
    q = deque([t])
    while q:
        v = q.popleft()
        for u in rev[v]:
            if not reach[u]:
                reach[u] = True
                q.append(u)

    paths, path = [], [s]
    on_path = [False] * n        # 只记当前路径，回溯时撤销
    on_path[s] = True

    def dfs(u):
        if u == t:
            paths.append(path[:])    # 存副本
            return
        for v in g[u]:
            if not on_path[v] and reach[v]:
                on_path[v] = True
                path.append(v)
                dfs(v)
                path.pop()
                on_path[v] = False

    if reach[s]:
        dfs(s)
    return paths
```

**复杂度。** 时间 `O(P·n + n + m)`（`P` 为走过的路径前缀数，输出本身是下界），空间 `O(n)` 加输出。

**易错点。**
- 用全局 `visited` 不撤销：边 `[[0,2],[0,1],[1,2],[2,3]]` 求 `0 → 3` 只得 `[[0,2,3]]`，漏掉 `[0,1,2,3]`。
- 存 `path` 而不是 `path[:]`：所有结果指向同一个列表，最后全变成 `[s]`。
- 不加 `on_path`：有环时无限递归。

**追问。**
- 图保证无环（DAG）？：不需要 `on_path`，可对「从 `u` 到 `t` 的全部路径」记忆化（LC 797）。
- 只要路径条数？：DAG 上是 `O(n + m)` 的 DP；有环图上数简单路径是 #P-hard，只能枚举或状压。

**同模式。** LC 797 所有可能的路径、LC 46 全排列、LC 79 单词搜索、LC 1059 从起点到终点的所有路径
