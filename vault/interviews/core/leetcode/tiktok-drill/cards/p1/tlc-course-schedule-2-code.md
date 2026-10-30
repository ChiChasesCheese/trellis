---
id: tlc-course-schedule-2-code
node: p1.course-schedule
type: qa
step: 2
---
## Q
**LC 207 课程表**｜写出 Python 实现

`numCourses` 门课（`1 <= numCourses <= 2000`），先修对 `prerequisites[i] = [a, b]` 表示学 `a` 之前要先学 `b`（`0 <= prerequisites.length <= 5000`，下标都在 `[0, numCourses)`，先修对互不相同）。返回能否学完所有课程。要求线性时间，不用递归。

## A
**思路。** 建邻接表和入度数组，边方向是「先修课 → 后修课」。把入度为 0 的课程放进队列，每取出一门就计数，并把后继课程的入度减一，减到 0 就入队。最后学完的课程数等于 `numCourses` 才说明没有环。

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

运行：`2, [[1,0]]` → `True`；`2, [[1,0],[0,1]]` → `False`；`1, []` → `True`；`3, [[0,1],[1,2],[2,0]]` → `False`；`4, [[1,0],[2,0],[3,1],[3,2]]` → `True`；`2000` 门课连成链 → `True`。

**复杂度。** 时间 `O(V + E)`：建图扫一遍先修对，每个点出队一次、每条边减一次入度；空间 `O(V + E)`。

**写法要点。** `[[] for _ in range(n)]` 每个节点一个独立列表（`[[]] * n` 会共享同一个）；`for course, pre in prerequisites` 直接解包，注意题面里 `[a, b]` 是「学 `a` 先学 `b`」，所以第一个是后修课；`deque(生成器)` 一步建好初始队列；`collections.deque` 的 `popleft` 是 `O(1)`，用列表 `pop(0)` 会退化成 `O(n)`。
