---
id: tlc-course-schedule-iv-0-whole
node: b.course-schedule-iv
type: qa
---
## Q
**LC 1462 课程表 IV**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 1 次 · 最近 2022-07-16（国内 CodeTop）

共有 `numCourses` 门课，编号 `0` 到 `numCourses - 1`。`prerequisites[i] = [ai, bi]` 表示想选 `bi` 必须先选 `ai`。先决条件可以是间接的：`a` 是 `b` 的先决条件，`b` 是 `c` 的先决条件，则 `a` 也是 `c` 的先决条件。给 `queries`，`queries[j] = [uj, vj]`，对每个查询回答 `uj` 是否是 `vj` 的先决条件，返回布尔数组。`2 <= numCourses <= 100`，`0 <= prerequisites.length <= numCourses * (numCourses - 1) / 2`，`ai != bi`，每对 `[ai, bi]` 互不相同，先修关系图中没有环，`1 <= queries.length <= 10^4`，`ui != vi`。例：`numCourses = 2`，`prerequisites = [[1,0]]`，`queries = [[0,1],[1,0]]` → `[false, true]`；`numCourses = 3`，`prerequisites = [[1,2],[1,0],[2,0]]`，`queries = [[1,0],[1,2]]` → `[true, true]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 预处理整张图的传递闭包（transitive closure），每个查询 `O(1)`。按拓扑序（Kahn 算法）处理节点，用一个 Python 整数当位集（bitset）保存每个节点的全部先修课：`pre[v] |= pre[u] | (1 << u)`。

**识别。** 「间接先决条件」就是图上的可达性（reachability）。查询多（`10^4`）而节点少（`<= 100`），适合先把所有点对的可达性算出来再 `O(1)` 回答。图保证无环（DAG），所以拓扑序可用；节点只有 `100` 个，Floyd–Warshall 的 `O(n^3)` 也行。

**推导。** 暴力：每个查询做一次 DFS / BFS，`O(n + E)`，边数最多 `4950`，乘以 `10^4` 个查询约 `5 × 10^7`，Python 偏慢。浪费：大量查询重复探索同样的子图。洞察：节点只有 `100` 个，所有 `n^2` 个点对的答案是有限的，一次算完。方法一：Floyd–Warshall，`O(n^3) = 10^6`。方法二：按拓扑序，处理到 `v` 时它的所有先修课已经确定，`v` 的先修集合就是各直接前驱的先修集合加上前驱本身，用整数的位或 `|` 一次合并 `100` 位。

```python
from collections import deque


def check_if_prerequisite(num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for a, b in prerequisites:             # a 是 b 的先修课：边 a -> b
        graph[a].append(b)
        indegree[b] += 1
    pre = [0] * num_courses                # pre[v]：位集，第 u 位为 1 表示 u 是 v 的（直接或间接）先修课
    queue = deque(i for i in range(num_courses) if indegree[i] == 0)
    while queue:                           # 拓扑序：处理 u 时，它的所有先修课都已并入 pre[u]
        u = queue.popleft()
        for v in graph[u]:
            pre[v] |= pre[u] | (1 << u)
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return [bool(pre[v] >> u & 1) for u, v in queries]
```

运行：三个示例依次得到 `[False, True]`、`[False, False]`、`[True, True]`；链 `0→1→2` 查 `[0,2]` 得 `True`；`100` 门课、`4950` 条边的完全有向无环图加 `10^4` 个查询约 `0.5 ms`。

**复杂度。** 时间 `O(n + E)` 次位运算（每次约 `n` 位）加 `O(1)` 每个查询；空间 `O(n)` 个整数，约 `n^2 / 8` 字节。

**易错点。**
- 只检查直接的先修边：链 `0→1→2` 查 `[0,2]` 得到 `False`，正确是 `True`。
- 位集传播漏掉 `u` 自己，写成 `pre[v] |= pre[u]`：示例 1 得到 `[False, False]`，正确是 `[False, True]`；`pre[u]` 只含 `u` 的先修课，不含 `u`。
- 查询方向读反：问“`u` 是不是 `v` 的先决条件”要读 `pre[v]` 的第 `u` 位，而不是 `pre[u]` 的第 `v` 位。

**追问。**
- 图里可能有环：拓扑序处理不到环上的点；先用强连通分量（Tarjan）缩点再在 DAG 上做，或者直接用 Floyd–Warshall。
- 在线加边：新增 `a → b` 时，所有能到达 `a` 的点（含 `a`）都要并入 `b` 及其后继的集合，`O(n^2)` 每条边。
- Floyd–Warshall 写法：三重循环更新 `reach[i][j] |= reach[i][k] and reach[k][j]`，`O(n^3)`，`n = 100` 时只有 `10^6` 步。

**同模式。** LC 207 / 210 课程表、LC 1334 阈值距离内邻居数最少的城市、LC 802 找到最终的安全状态、LC 1971 寻找图中是否存在路径。
