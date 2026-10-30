---
id: tlc-possible-bipartition-2-code
node: p3.possible-bipartition
type: qa
step: 2
---
## Q
**LC 886 可能的二分法**｜写出 Python 实现

`n`（`1` 到 `2000`）个人，编号 `1..n`；`dislikes` 里最多 `10^4` 对 `[a, b]`（`a < b`，互不相同）表示这两人不能同组。返回能否把所有人分进两组（组的大小任意）。

## A
**思路。** 建邻接表。`color[i]` 为 `0` 表示未分组，`1` 或 `-1` 表示两个组。对每个未染色的点作为起点，染成 `1` 后做 BFS：遍历邻居，同色则返回 `False`，未染色则染成相反色并入队。所有起点都通过则返回 `True`。

```python
from collections import deque

def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)
    color = [0] * (n + 1)                          # 0 = 未分组，1 / -1 = 两个组
    for start in range(1, n + 1):                  # 图可能不连通：每个连通块都要查
        if color[start]:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == color[u]:           # 互相讨厌的人落在同一组
                    return False
                if color[v] == 0:
                    color[v] = -color[u]           # 敌人的敌人放另一组
                    queue.append(v)
    return True
```

运行：`(4, [[1,2],[1,3],[2,4]])` → `True`，`(3, [[1,2],[1,3],[2,3]])` → `False`，`(5, [[1,2],[2,3],[3,4],[4,5],[1,5]])` → `False`，`(1, [])` → `True`；`n = 2000` 的一条链（`[i, i+1]`）→ `True`。

**复杂度。** 时间 `O(n + m)`：每个点入队至多一次，每条边从两端各看一次；空间 `O(n + m)`。

**写法要点。** `[[] for _ in range(n + 1)]` 建邻接表，下标直接对应编号 `1..n`，多开一格省去减一；`color` 数组同时承担「是否访问过」和「颜色」，不需要额外的 `visited`；用 `1 / -1` 两个颜色，取反就是 `-color[u]`，冲突判断就是 `==`；`deque.popleft()` 是 `O(1)`；外层 `for start` 加 `continue` 保证每个连通块只起一次 BFS。
