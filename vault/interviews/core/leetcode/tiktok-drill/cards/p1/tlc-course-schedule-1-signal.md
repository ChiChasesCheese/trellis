---
id: tlc-course-schedule-1-signal
node: p1.course-schedule
type: qa
step: 1
---
## Q
**LC 207 课程表**｜Medium · LC TikTok 热度 88/100（近 30 天） · 近一年被问：美国 15 次、国内 4 次 · CodeTop 国内累计 35 次 · 最近 2026-10-15（面试记录）

共有 `numCourses` 门课，编号 `0` 到 `numCourses - 1`。先修关系 `prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。判断能否学完所有课程。`1 <= numCourses <= 2000`，`0 <= prerequisites.length <= 5000`，`prerequisites[i].length == 2`，`0 <= a, b < numCourses`，所有先修对互不相同。例：`numCourses = 2, prerequisites = [[1,0],[0,1]]` → `false`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「先修 / 依赖 / 必须先于」+「能否全部完成」→ 有向图（directed graph）判环；能学完当且仅当图是有向无环图（DAG）。
- 要排顺序或判环的有向图 → 拓扑排序（topological sort），Kahn 算法（按入度）或 DFS 三色标记。
- `V <= 2000`、`E <= 5000`：线性 `O(V + E)` 足够。2000 层的链会触到 Python 的 1000 层递归上限，BFS 版的 Kahn 更稳。

**推导链。**
1. 暴力：对每门课做一次 DFS，看沿先修关系能否绕回自己，`O(V(V + E))`。
2. 浪费：每次从头搜，之前探索过的结论没有复用。
3. 洞察：没有未完成先修课的课程（入度为 0）可以立刻学；学完后把它的出边删掉，后继课程入度减一，可能产生新的入度为 0 的课程。
4. 环上的每个点都有来自环内的入边，入度降不到 0，永远不会出队；所以学完的课程数等于 `numCourses` 才说明无环。时间 `O(V + E)`。

**同模式的题**：LC 210 课程表 II（输出顺序）、LC 1136 并行课程、LC 269 火星词典、LC 802 找到最终的安全状态。
