---
id: tlc-is-graph-bipartite-0-whole
node: c.is-graph-bipartite
type: qa
---
## Q
**LC 785 判断二分图**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 3 次 · 最近 2022-07-17（国内 CodeTop）

无向图有 `n` 个节点（编号 `0..n-1`），`graph[u]` 是 `u` 的邻接点列表；无自环、无平行边，图可能不连通。若能把节点分成两个独立集合 `A`、`B`，使每条边的两个端点一个在 `A` 一个在 `B`，则是二分图。判断 `graph` 是否是二分图。`1 <= n <= 100`，`0 <= graph[u].length < n`，`graph[u]` 不含 `u` 且无重复，若 `graph[u]` 含 `v` 则 `graph[v]` 含 `u`。例：`graph = [[1,2,3],[0,2],[0,1,3],[0,2]]` → `false`；`graph = [[1,3],[0,2],[1,3],[0,2]]` → `true`（分成 `{0,2}` 与 `{1,3}`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用两种颜色做 DFS 染色：把当前点染成 `c`，邻居必须染成 `-c`，遇到已染成同色的邻居就说明有奇环；每个连通分量各染一次。

**识别。** 「分成两组、每条边跨组」就是二染色，等价于图中没有奇数长度的环。

**推导。** 暴力：枚举 `2^n` 种分组逐条验证边，`n = 100` 不可行。洞察：一个点的颜色一旦确定，邻居的颜色就被迫确定，传播下去要么全部一致要么在某条边上冲突，所以一次遍历就够。

```python
def is_bipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = [0] * n                              # 0 = 未染色，1 / -1 = 两个集合

    def dfs(u: int, c: int) -> bool:             # 把 u 染成 c，并要求邻居染成 -c
        color[u] = c
        for v in graph[u]:
            if color[v] == c:                    # 邻居与自己同色：出现奇环
                return False
            if color[v] == 0 and not dfs(v, -c):
                return False
        return True

    for start in range(n):                       # 图可能不连通：每个连通分量各染一次
        if color[start] == 0 and not dfs(start, 1):
            return False
    return True
```

运行：示例一 → `False`；示例二 → `True`；`[[]]`（单点）→ `True`；`[[1],[0],[3],[2]]`（两个不连通的边）→ `True`；`[[1,2],[0,2],[0,1]]`（三角形）→ `False`。

**复杂度。** 时间 `O(n + E)`，空间 `O(n)`（染色数组与递归栈）。

**拓展优化。**
- 并查集：每个点 `u` 与它所有邻居合并到一个「对立集合」，若 `u` 与某个邻居同集合则失败。
- 把递归换成队列（BFS），没有递归深度问题：

```python
from collections import deque


def is_bipartite_bfs(graph: list[list[int]]) -> bool:
    color = [0] * len(graph)
    for start in range(len(graph)):
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:                             # 显式队列，没有递归深度限制
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:
                    return False
                if color[v] == 0:
                    color[v] = -color[u]
                    queue.append(v)
    return True
```

**易错点。**
- 只从节点 0 出发：图不连通时，其余分量没有检查；`[[1],[0],[3,4],[2,4],[2,3]]` 前半是边、后半是三角形，应返回 `false`。
- 只检查「未染色邻居」而不检查已染色邻居的冲突，奇环永远发现不了。
- 最坏深度：链状图深度等于 `n`，这里 `n <= 100` 远低于 CPython 默认递归上限约 1000；若 `n` 达 `10^5`，需要 `sys.setrecursionlimit` 或改用 BFS。

**追问。**
- 构造一个划分方案：保留 `color` 数组，`color == 1` 的是 A，`-1` 的是 B。
- 边数很大的稠密图：BFS 与 DFS 都是 `O(n + E)`，瓶颈在读边。

**同模式。** LC 886 可能的二分法、LC 207 课程表（环检测）、LC 684 冗余连接、LC 1042 不邻接植花、LC 399 除法求值。
