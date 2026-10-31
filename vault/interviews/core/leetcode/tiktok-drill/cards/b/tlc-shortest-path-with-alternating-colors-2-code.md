---
id: tlc-shortest-path-with-alternating-colors-2-code
node: b.shortest-path-with-alternating-colors
type: qa
step: 2
---
## Q
**LC 1129 颜色交替的最短路径**｜写出 Python 实现

有向图有 `n` 个结点（`1 <= n <= 100`），红边数组 `red_edges` 和蓝边数组 `blue_edges`（各至多 `400` 条，可能有自环和平行边）。返回 `answer`：`answer[x]` 是从结点 `0` 到 `x` 的红蓝边交替的最短路径长度，不存在为 `-1`。

## A
**思路。** 邻接表按颜色分开存：`graph[0]` 是红边，`graph[1]` 是蓝边。BFS 的队列元素是 `(结点, 下一条边颜色, 步数)`。起点两种颜色都入队。弹出 `(u, c, d)` 后，若 `u` 尚未有答案就记 `d`；沿颜色 `c` 的出边走到 `v`，进入状态 `(v, 1 - c)`，没见过就入队。

```python
from collections import deque


def shortest_alternating_paths(n: int, red_edges: list[list[int]], blue_edges: list[list[int]]) -> list[int]:
    graph: list[list[list[int]]] = [[[] for _ in range(n)] for _ in range(2)]   # graph[颜色][u]：u 的出边
    for u, v in red_edges:
        graph[0][u].append(v)
    for u, v in blue_edges:
        graph[1][u].append(v)
    ans = [-1] * n
    # 状态 (u, c)：当前在 u，下一条边必须是颜色 c；起点可以先走红也可以先走蓝
    seen = {(0, 0), (0, 1)}
    queue = deque([(0, 0, 0), (0, 1, 0)])  # (结点, 下一条边颜色, 已走步数)
    while queue:
        u, c, d = queue.popleft()
        if ans[u] == -1:                   # BFS 按步数递增，第一次到 u 就是最短
            ans[u] = d
        for v in graph[c][u]:
            if (v, 1 - c) not in seen:     # 走完颜色 c 的边，下一条必须换色
                seen.add((v, 1 - c))
                queue.append((v, 1 - c, d + 1))
    return ans
```

运行：`n = 3, red_edges = [[0,1],[1,2]], blue_edges = []` → `[0, 1, -1]`；`n = 3, red_edges = [[0,1]], blue_edges = [[2,1]]` → `[0, 1, -1]`；`n = 1` 无边 → `[0]`；`n = 3, red_edges = [[0,1],[1,2]], blue_edges = [[0,1]]` → `[0, 1, 2]`；`n = 3, red_edges = [[0,0]], blue_edges = [[0,1],[1,2]]` → `[0, 1, -1]`。

**复杂度。** 时间 `O(n + e)`：至多 `2n` 个状态，各出队一次，每个状态只扫同色出边；空间 `O(n + e)`：邻接表、`seen`、队列。

**写法要点。** `[[[] for _ in range(n)] for _ in range(2)]` 用列表推导建多层独立列表，千万不要写 `[[[]] * n] * 2`（会让所有位置共享同一个列表对象）；颜色用 `0 / 1`，翻转写 `1 - c`；`deque` 的 `popleft()` 是 `O(1)`；`seen` 用元组集合，元组可哈希；解包 `for u, v in red_edges` 直接拆边。
