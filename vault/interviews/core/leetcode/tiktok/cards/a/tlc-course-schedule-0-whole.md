---
id: tlc-course-schedule-0-whole
node: a.course-schedule
type: qa
---
## Q
**LC 207 课程表**｜Medium · TikTok·字节 高频

共有 `numCourses` 门课，编号 `0` 到 `numCourses - 1`。先修关系 `prerequisites[i] = [a, b]` 表示学 `a` 之前必须先学 `b`。判断能否学完所有课程。`1 <= numCourses <= 2000`，`0 <= prerequisites.length <= 5000`，`prerequisites[i].length == 2`，`0 <= a, b < numCourses`，所有先修对互不相同。例：`numCourses = 2, prerequisites = [[1,0]]` → `true`；`numCourses = 2, prerequisites = [[1,0],[0,1]]` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把课程当节点、先修关系当有向边（先修课指向后修课），问题就是「这张有向图有没有环」；用拓扑排序（Kahn 算法）：反复取出入度为 0 的课程，取出的课程数等于 `numCourses` 才说明无环。`O(V + E)`。

**识别。** 「依赖 / 先修 / 必须先于」+「能否全部完成」是有向图判环的信号。`V <= 2000`、`E <= 5000`，线性算法即可；递归 DFS 在 2000 层的链上会触到 Python 默认的 1000 层递归上限，BFS 版本的 Kahn 算法没有这个问题。

**推导。** 暴力：对每门课做一次 DFS 看能否回到自己，`O(V(V + E))`。浪费是每次从头搜。洞察：没有任何未完成先修课的课程（入度为 0）可以立刻学；学完后把它从图里删掉，它的后继课程入度减一，可能又出现新的入度为 0 的课程。如果存在环，环上每个点都有一条来自环内的入边，入度永远降不到 0，永远进不了队列，最终取出的课程数小于 `numCourses`。

```python
from collections import deque


def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)                  # 边 pre -> course：先修课指向后修课
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    taken = 0
    while queue:
        cur = queue.popleft()
        taken += 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == num_courses                    # 有环 => 环上的点入度永远降不到 0
```

运行：`2, [[1,0]]` → `True`；`2, [[1,0],[0,1]]` → `False`；`1, []` → `True`；`3, [[0,1],[1,2],[2,0]]` → `False`；`4, [[1,0],[2,0],[3,1],[3,2]]` → `True`；`2000` 门课连成一条链 → `True`（无递归）。

**复杂度。** 时间 `O(V + E)`：每条边处理一次，每个点出队一次；空间 `O(V + E)`（邻接表和入度数组）。

**易错点。**
- 不能用单个 `visited` 集合做 DFS 判环：菱形图（`0` 指向 `1` 和 `2`，二者都指向 `3`）里 `3` 会被访问两次，被误判成环，`4, [[1,0],[2,0],[3,1],[3,2]]` 得到 `False`，正确是 `True`。DFS 判环必须区分"在当前路径上"和"已完成"两种状态（三色标记）。
- 判断条件是取出的课程数等于 `numCourses`，不是队列为空；孤立课程（不在任何先修对里）也要计入，所以初始队列要扫描全部 `numCourses` 个点的入度。
- 邻接表别写 `[[]] * n`，所有节点会共享同一个列表。

**追问。**
- 要输出一个学习顺序：就是 LC 210，出队顺序即是拓扑序。
- 最少几个学期学完（每学期可并行任意门）：Kahn 按层处理，层数就是学期数；有环返回 `-1`。
- 用 DFS 做：三色标记，状态 `1` 表示在当前路径上，遇到状态 `1` 的点就有环；链很长时要改成迭代或调大递归上限。

**同模式。** LC 210 课程表 II、LC 1136 并行课程、LC 269 火星词典、LC 802 找到最终的安全状态、LC 310 最小高度树。
