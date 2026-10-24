---
id: tlc-patterns-shortest-path-7-problems
node: patterns.shortest-path
type: qa
step: 7
---
## Q
**最短路（Shortest Path）｜本组用到最短路的题**

按变形分类，这个题组里哪些题属于最短路？

## A
**加权图 / 限制边数**
- LC 787 K 站中转内最便宜的航班（Bellman-Ford，或 Dijkstra 加站数状态）
- LC 399 除法求值（图上的路径乘积，可用 DFS / 带权并查集）

**带状态的 BFS**
- LC 1293 网格中的最短路径（状态含剩余消除次数）

**无权最短路（BFS）**
- LC 127 单词接龙
- LC 815 公交路线
- LC 994 腐烂的橘子（多源）
- LC 286 墙与门（多源）
- LC 934 最短的桥（多源）
- LC 317 离建筑物最近的距离（对每栋楼各做一次 BFS）

**相邻：最小生成树**
- LC 1584 连接所有点的最小费用（Kruskal）

提示：先看边的代价，再看有没有"最多 `k` 步 / 最多消除 `k` 次"这类限制，限制就是状态的一个分量。
