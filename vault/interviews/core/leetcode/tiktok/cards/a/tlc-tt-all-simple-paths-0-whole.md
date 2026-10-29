---
id: tlc-tt-all-simple-paths-0-whole
node: a.tt-all-simple-paths
type: qa
---
## Q
**枚举有向图中的所有简单路径（含环的情况）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-08-23（面试记录）

给一个有向图：`n` 个点（编号 `0 .. n-1`）和边表 `edges`（`[u, v]` 表示 `u → v`，没有重边），以及起点 `s`、终点 `t`（`s != t`）。按任意顺序返回从 `s` 到 `t` 的**所有简单路径**：路径上不能重复经过同一个点。`1 <= n <= 15`，边数 `<= 60`，图里**可能有环**。例：`n = 4`，`edges = [[0,1],[0,2],[1,2],[2,3],[1,3]]`，`s = 0`，`t = 3` → `[[0,1,2,3],[0,1,3],[0,2,3]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（backtracking）DFS：从 `s` 出发，用 `on_path` 标记**当前路径上**的点，走进去时标记、退回来时撤销；到达 `t` 就把路径的副本存下来。先从 `t` 沿反向边 BFS 求出「能到达 `t` 的点」，DFS 只走这些点，剪掉注定走不到 `t` 的分支。

**识别。** 「返回**所有**路径」→ 输出本身可能是指数级，只能枚举，用回溯；`n <= 15` 是在告诉你指数级可以接受。「可能有环」+「简单路径」→ 必须防止重复进点，但标记的是**当前路径**，不是「访问过」：一个点可以出现在许多条不同的路径里。

**推导。** 最暴力的是枚举点的所有排列再检查每对相邻点之间有没有边，`O(n!·n)`。改成沿边 DFS，只沿存在的边扩展，状态是「当前路径」。图有环时不加限制会无限绕圈，所以加 `on_path`；和普通遍历不同，回溯时要把标记撤销，否则别的分支经过同一个点会被误挡。最后加可达性剪枝：如果 `v` 根本走不到 `t`，从 `v` 往下的整棵子树都不会产出路径，提前一次反向 BFS（`O(n + m)`）就能把这类分支全部剪掉。

```python
from collections import deque


def all_simple_paths(n: int, edges: list[list[int]], s: int, t: int) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    rev: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        rev[v].append(u)

    # 剪枝：先从 t 反向 BFS，只保留能走到 t 的点
    reach = [False] * n
    reach[t] = True
    queue = deque([t])
    while queue:
        v = queue.popleft()
        for u in rev[v]:
            if not reach[u]:
                reach[u] = True
                queue.append(u)

    paths: list[list[int]] = []
    path = [s]
    on_path = [False] * n            # 只记当前路径上的点，回溯时撤销
    on_path[s] = True

    def dfs(u: int) -> None:
        if u == t:
            paths.append(path.copy())  # 存副本：path 之后还会被修改
            return
        for v in graph[u]:
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

运行：例子 → `[[0, 1, 2, 3], [0, 1, 3], [0, 2, 3]]`；带环的 `n = 3`，`edges = [[0,1],[1,0],[1,2],[2,1]]`，`0 → 2` → `[[0, 1, 2]]`；走不到 `t` 的 `edges = [[0,1],[1,0]]`，`0 → 2` → `[]`；`n = 4`，`edges = [[0,1],[1,2],[2,0],[0,3],[2,3]]`，`1 → 3` → `[[1, 2, 0, 3], [1, 2, 3]]`。

**复杂度。** 时间 `O(P·n + n + m)`，`P` 是 DFS 走过的路径前缀数；剪枝后每个前缀都能延伸到 `t`（只是可能被当前路径挡住），输出本身就是 `O(Σ 路径长度)`，这是下界。空间：递归深度和 `path` 都不超过 `n`，另加输出。

**易错点。**
- 用全局 `visited`（访问过就再也不进）：边表 `[[0,2],[0,1],[1,2],[2,3]]`，`0 → 3` 只得到 `[[0, 2, 3]]`，漏掉 `[0, 1, 2, 3]`（点 2 在第一条路径里被标记后再也进不去）。标记必须在回溯时撤销。
- 存 `path` 本身而不是 `path.copy()`：所有结果指向同一个列表，最后全变成 `[s]`。
- 不加 `on_path`：有环时（`0 → 1 → 0 → 1 …`）无限递归。

**追问。**
- 图保证无环（DAG）：不需要 `on_path`；可以按点记忆化「从 `u` 到 `t` 的全部路径」（LC 797）。
- 列出所有简单环：对每个起点 `start`，只允许走编号比它大的点，回到 `start` 就记一个环，每个环只被它的最小点记录一次。
- 只要路径条数：DAG 上是 `O(n + m)` 的 DP；有环图上数简单路径是 #P-hard，只能枚举或状压。

**同模式。** LC 797 所有可能的路径、LC 46 全排列、LC 79 单词搜索、LC 1059 从起点到终点的所有路径。
