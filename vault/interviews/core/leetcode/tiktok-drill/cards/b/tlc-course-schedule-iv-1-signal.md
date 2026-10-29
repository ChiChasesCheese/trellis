---
id: tlc-course-schedule-iv-1-signal
node: b.course-schedule-iv
type: qa
step: 1
---
## Q
**LC 1462 课程表 IV**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 1 次 · 最近 2022-07-16（CodeTop）

`numCourses` 门课，`prerequisites[i] = [ai, bi]` 表示想选 `bi` 必须先选 `ai`，先决条件可以是间接的。给 `queries`，`queries[j] = [uj, vj]`，回答 `uj` 是不是 `vj` 的先决条件。`2 <= numCourses <= 100`，`0 <= prerequisites.length <= numCourses * (numCourses - 1) / 2`，先修图无环，`1 <= queries.length <= 10^4`，`ui != vi`。例：`numCourses = 2`，`prerequisites = [[1,0]]`，`queries = [[0,1],[1,0]]` → `[false, true]`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「间接先决条件」→ 图上的可达性（reachability），整张图的传递闭包（transitive closure）。
- 「查询 `10^4` 次，课程只有 `100` 门」→ 预处理所有点对，每个查询 `O(1)`；`n^2 = 10^4` 个点对，完全存得下。
- 「保证无环」→ 可以用拓扑序（Kahn 算法）；`n <= 100` 也可以用 Floyd–Warshall `O(n^3) = 10^6`。
- 边数最多 `n(n-1)/2` → 图可以非常稠密，每个查询单独 DFS 的代价不小。

**推导链。**
1. 暴力：每个查询做一次 DFS / BFS，`O(n + E)`，约 `5000`，乘以 `10^4` 个查询约 `5 × 10^7`。
2. 浪费：不同查询重复探索同一片子图。
3. 方法一：Floyd–Warshall，`reach[i][j] |= reach[i][k] and reach[k][j]`，`O(n^3)`。
4. 方法二：按拓扑序，节点 `v` 的先修集合 = 各直接前驱的先修集合 ∪ 前驱本身；用整数当位集（bitset），一次位或合并 `100` 位。
5. 查询读 `pre[v]` 的第 `u` 位，`O(1)`。

**同模式的题**：LC 207 / 210 课程表、LC 1334 阈值距离内邻居数最少的城市、LC 802 找到最终的安全状态、LC 1971 寻找图中是否存在路径。
