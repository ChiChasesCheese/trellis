---
id: tlc-patterns-shortest-path-1-signals
node: patterns.shortest-path
type: qa
step: 1
---
## Q
**最短路（Shortest Path）｜信号**

什么样的题面该想到 Dijkstra、Bellman-Ford、0-1 BFS，还是普通 BFS？"带状态的最短路"怎么识别？

## A
先看**边的代价**：

| 边的代价 | 算法 | 复杂度 |
|---|---|---|
| 每步代价相同（或只数步数） | BFS | `O(V + E)` |
| 只有 0 和 1 | 0-1 BFS（双端队列） | `O(V + E)` |
| 非负且不全相同 | Dijkstra（最小堆） | `O((V + E) log V)` |
| 有负权，或**限制经过的边数** | Bellman-Ford | `O(k · E)` |
| 所有点对 | Floyd | `O(V^3)`，`V <= 100` |

**触发信号：**
- 「最便宜 / 最短 / 最少花费」且各条边价格不同：LC 787 机票价格（Dijkstra 或 Bellman-Ford）。
- 「**最多经过 `k` 站**」「最多 `k` 条边」：限制边数 ⇒ Bellman-Ford 按轮松弛，或把"已用边数"放进状态。
- 网格里**可以消除 `k` 个障碍**：LC 1293 ⇒ 状态不只是位置，还有"剩余次数"：`(r, c, left)`，在状态图上做 BFS。
- 状态之间的转移代价相同（单词接龙 LC 127）⇒ 普通 BFS。

**近似信号：**
- 只问连通性 ⇒ 并查集 / DFS。
- 无权图用 Dijkstra 也对，但 BFS 更简单更快。
- 有负权环时最短路无定义；Dijkstra 在有负权边时可能出错。
- 要最小生成树（连通所有点的最小总边权）⇒ Kruskal / Prim，不是最短路。
- 数据范围：`n <= 100`、边 `<= n(n-1)/2`（LC 787）允许 `O(k · E)`。
