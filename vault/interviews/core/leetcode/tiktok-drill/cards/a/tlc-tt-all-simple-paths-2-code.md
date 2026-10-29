---
id: tlc-tt-all-simple-paths-2-code
node: a.tt-all-simple-paths
type: qa
step: 2
---
## Q
**枚举有向图中的所有简单路径（含环的情况）**｜写出 Python 实现

有向图有 `n` 个点（`n <= 15`）、至多 60 条边，可能有环。返回从 `s` 到 `t`（`s != t`）的所有简单路径，顺序任意。

## A
**思路。** 先从 `t` 沿反向边 BFS，标出能到达 `t` 的点。然后从 `s` 回溯 DFS：只进「不在当前路径上、且能到达 `t`」的点，进点标记、出点撤销；到达 `t` 时存下路径副本。

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

运行：例子 `n = 4`，`edges = [[0,1],[0,2],[1,2],[2,3],[1,3]]`，`0 → 3` → `[[0, 1, 2, 3], [0, 1, 3], [0, 2, 3]]`；带环 `[[0,1],[1,0],[1,2],[2,1]]`，`0 → 2` → `[[0, 1, 2]]`；`[[0,1],[1,0]]`，`0 → 2` → `[]`。

**复杂度。** 时间 `O(P·n + n + m)`，`P` 为 DFS 走过的路径前缀数，与输出规模同阶；空间 `O(n + m)` 加输出，递归深度不超过 `n`。

**写法要点。** 邻接表用 `[[] for _ in range(n)]`，不能写 `[[]] * n`（`n` 个引用指向同一个列表）；`deque.popleft()` 是 `O(1)`；`path` 和 `on_path` 在递归里共享、原地改再撤销，避免每层复制；只在到达 `t` 时 `path.copy()`。
