---
id: tlc-shortest-path-with-alternating-colors-4-followup
node: b.shortest-path-with-alternating-colors
type: qa
step: 4
---
## Q
**LC 1129 颜色交替的最短路径**｜追问

面试官接着问：（1）要输出具体的路径，不只是长度？（2）颜色有 `k` 种，要求按固定顺序循环（红→蓝→绿→红…）？（3）边带权值呢？

## A
1. **输出路径**：给每个状态记一个父状态 `parent[(v, 1 - c)] = (u, c)`，到达目标结点的最短状态后沿父指针一路回溯，再反转。结点 `x` 的最短路径对应它两个状态中先出队的那一个。
2. **`k` 种颜色循环**：邻接表改成 `graph[颜色][u]`（`k` 层），状态 `(u, c)` 表示下一条边必须是颜色 `c`，走完后进入 `(v, (c + 1) % k)`；起点把 `k` 种颜色状态都入队（若允许任选首色），状态总数 `k · n`，复杂度 `O(k · n + e)`。
3. **带权**：BFS 失效（步数不再等于路径长度），换成 Dijkstra，状态仍是 `(u, c)`：

```python
import heapq


def shortest_alternating_weighted(n: int, red: list[tuple[int, int, int]],
                                  blue: list[tuple[int, int, int]]) -> list[float]:
    graph: list[list[list[tuple[int, int]]]] = [[[] for _ in range(n)] for _ in range(2)]
    for u, v, w in red:
        graph[0][u].append((v, w))
    for u, v, w in blue:
        graph[1][u].append((v, w))
    best = {(0, 0): 0, (0, 1): 0}
    heap = [(0, 0, 0), (0, 0, 1)]          # (距离, 结点, 下一条边颜色)
    while heap:
        d, u, c = heapq.heappop(heap)
        if d > best.get((u, c), float("inf")):
            continue                       # 过期条目：已有更短的记录
        for v, w in graph[c][u]:
            if d + w < best.get((v, 1 - c), float("inf")):
                best[(v, 1 - c)] = d + w
                heapq.heappush(heap, (d + w, v, 1 - c))
    return [min(best.get((x, 0), float("inf")), best.get((x, 1), float("inf"))) for x in range(n)]
```
   运行：`n = 3`，红边 `[(0,1,5),(1,2,1)]`，蓝边 `[(0,1,2)]` → `[0, 2, 3]`（路径 `0 →(蓝,2) 1 →(红,1) 2`）。

**Python 提醒**：`[[[] for _ in range(n)] for _ in range(2)]` 必须用推导式；`[[[]] * n] * 2` 会让所有结点共享同一个邻接列表，添加一条边会同时出现在每个结点上。
