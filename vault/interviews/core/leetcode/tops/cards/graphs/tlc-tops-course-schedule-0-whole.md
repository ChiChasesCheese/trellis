---
id: tlc-tops-course-schedule-0-whole
node: graphs.course-schedule
type: qa
---
## Q
**LC 207 课程表**｜Medium · 全公司热度第 27 名 · Blind 75、NeetCode 150、Hot 100、Top Interview 150

你这个学期必须选修 `numCourses` 门课程，记为 `0` 到 `numCourses - 1`。在选修某些课程之前需要一些先修课程。先修课程按数组 `prerequisites` 给出，其中 `prerequisites[i] = [ai, bi]`，表示如果要学习课程 `ai` 则必须先学习课程 `bi`。例如，先修课程对 `[0, 1]` 表示：想要学习课程 `0`，你需要先完成课程 `1`。请你判断是否可能完成所有课程的学习？如果可以，返回 `true`；否则，返回 `false`。`1 <= numCourses <= 2000`，`0 <= prerequisites.length <= 5000`，`prerequisites[i].length == 2`，`0 <= ai, bi < numCourses`，`prerequisites[i]` 中的所有课程对互不相同。

例：`numCourses = 2`，`prerequisites = [[1,0]]` → `true`；`numCourses = 2`，`prerequisites = [[1,0],[0,1]]` → `false`（互为先修）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点：** 有向图判环（cycle detection）：DFS 三色标记；等价于能否拓扑排序（topological sort）。

**一句话。** 把「先修 → 后修」建成有向图，能修完所有课当且仅当图中没有环；用 DFS 三色标记，遇到当前路径上的结点就说明有环。

**识别。** 「依赖关系」「先修」「能否完成」就是有向图是否无环（DAG）。`n <= 2000`、边 `<= 5000`，线性即可。

**推导。** 想直接模拟选课顺序要不断找「先修都已完成」的课，复杂度高且难写对。换成图：课程是结点，`b → a` 表示 `b` 先于 `a`。有环意味着环上每门课都在等环上另一门，永远修不完；无环则存在拓扑序。DFS 判环的关键是区分三种状态：未访问、正在当前递归路径上（灰）、已完成且确认其后继无环（黑）。DFS 过程中碰到灰色结点，就是沿着路径绕回来了，有环；碰到黑色结点可以直接跳过，保证每个结点只展开一次。

```python
def can_finish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        graph[b].append(a)              # 边 b -> a：先学 b 才能学 a

    state = [0] * numCourses            # 0 未访问；1 在当前 DFS 路径上；2 已确认从它出发无环

    def has_cycle(u: int) -> bool:
        if state[u] == 1:               # 回到了当前路径上的结点：有环
            return True
        if state[u] == 2:               # 已验证过，无需重复展开
            return False
        state[u] = 1
        for v in graph[u]:
            if has_cycle(v):
                return True
        state[u] = 2                    # 所有后继都无环：标记完成
        return False

    return not any(has_cycle(u) for u in range(numCourses))     # 图可能不连通，每个起点都要试
```

**运行。** `2`、`[[1,0]]` → `True`；`2`、`[[1,0],[0,1]]` → `False`；`1`、`[]` → `True`；`1`、`[[0,0]]`（自环）→ `False`；`4`、`[[1,0],[2,0],[3,1],[3,2]]`（菱形）→ `True`。

**复杂度。** 时间 `O(V + E)`；空间 `O(V + E)`（邻接表）加递归栈 `O(V)`。

**拓展优化。**
- Kahn 算法（BFS 拓扑排序，迭代）：反复取出入度为 0 的结点，能取出全部 `n` 个就无环。不用递归，也顺手得到一个合法的学习顺序（LC 210）。
```python
from collections import deque


def can_finish_kahn(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for a, b in prerequisites:
        graph[b].append(a)
        indeg[a] += 1
    q = deque(u for u in range(numCourses) if indeg[u] == 0)    # 没有先修要求的课先上
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:           # v 的先修全部完成
                q.append(v)
    return done == numCourses           # 有环的结点入度永远降不到 0
```
- 要输出具体顺序（LC 210）：Kahn 的出队顺序，或 DFS 后序反转。

**易错点。**
- 只用一个布尔 `visited`：遇到访问过的结点就判环，菱形图 `[[1,0],[2,0],[3,1],[3,2]]` 里 `3` 被两条路径到达，误判有环，返回 `False`。必须区分「在当前路径上」和「已完成」。
- 忘了对每个起点都启动 DFS：图可能不连通，只从课程 `0` 出发会漏掉其他分量里的环。
- 递归深度等于最长依赖链：`numCourses = 2000` 的一条链（每门课依赖上一门）深度 2000，超过 CPython 默认约 1000 的递归上限而 `RecursionError`；此时用 Kahn 迭代版或调高上限。

**同模式。** LC 210 课程表 II、LC 269 火星词典、LC 802 找到最终的安全状态、LC 1462 课程表 IV。
