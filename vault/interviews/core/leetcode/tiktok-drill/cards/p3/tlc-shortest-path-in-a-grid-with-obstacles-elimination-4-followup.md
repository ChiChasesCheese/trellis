---
id: tlc-shortest-path-in-a-grid-with-obstacles-elimination-4-followup
node: p3.shortest-path-in-a-grid-with-obstacles-elimination
type: qa
step: 4
---
## Q
**LC 1293 网格中的最短路径**｜追问

面试官接着问：（1）要输出具体的路径？（2）每个障碍消除的代价不同（有的要花 `2` 次），或者每格走一步的代价不同？（3）网格非常大，状态放不下？

## A
1. **输出路径**：给每个状态记前驱。可以把队列元素换成 `(i, j, left)`，另用字典 `parent[(i, j, left)] = (pi, pj, pleft)`；到达终点后沿 `parent` 倒推再反转。每格只保留最大剩余的写法里，前驱字典要按“状态”而不是按“格子”存，因为同一格可能有多个状态入过队。
2. **代价不同**：消除代价不同不改变框架，只是 `nleft = left - cost[ni][nj]`；每步代价不同则不再是无权图，BFS 换成 Dijkstra：`heapq` 里放 `(步数或代价, i, j, left)`，同样用“每格最大剩余”做支配剪枝。
3. **网格很大**：把 `k` 限制为 `min(k, m + n - 3)` 后，状态数量级是 `m * n * (m + n)`；仍放不下可以用 A*（曼哈顿距离作启发）减少扩展，或者双向 BFS 在中间相遇。

**Python 提醒**：`deque` 里放元组 `(i, j, left)` 的开销比自定义类小；`not (0 <= ni < m and 0 <= nj < n)` 与 `continue` 配合，比把四个比较写进主条件更容易读；`best_left` 用二维列表比 `dict[(i, j)]` 快，下标访问不需要构造元组键。
