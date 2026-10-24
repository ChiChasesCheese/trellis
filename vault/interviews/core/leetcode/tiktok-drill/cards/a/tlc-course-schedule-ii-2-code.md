---
id: tlc-course-schedule-ii-2-code
node: a.course-schedule-ii
type: qa
step: 2
---
## Q
**LC 210 课程表 II**｜写出 Python 实现

`numCourses` 门课（`1 <= numCourses <= 2000`），先修对 `[a, b]` 表示学 `a` 之前先学 `b`（`a != b`，先修对互不相同，数量至多 `numCourses * (numCourses - 1)`）。返回一个合法学习顺序，学不完返回 `[]`。

## A
**思路。** 建邻接表（边 `b → a`）和入度数组，入度为 0 的课程入队。每次出队就把它追加进结果，并把后继的入度减一，减到 0 入队。结果长度等于 `numCourses` 才有效，否则有环。

```python
from collections import deque


def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)
        indegree[course] += 1
    queue = deque(i for i, d in enumerate(indegree) if d == 0)
    order: list[int] = []
    while queue:
        cur = queue.popleft()
        order.append(cur)                          # 出队顺序就是一个合法的拓扑序
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == num_courses else []
```

运行：`2, [[1,0]]` → `[0, 1]`；`4, [[1,0],[2,0],[3,1],[3,2]]` → `[0, 1, 2, 3]`；`1, []` → `[0]`；`2, [[1,0],[0,1]]` → `[]`；`3, []` → `[0, 1, 2]`。

**复杂度。** 时间 `O(V + E)`；空间 `O(V + E)`。

**写法要点。** `for course, pre in prerequisites` 的顺序对应题面 `[a, b]`：`a` 是后修课；`order` 既当结果又当计数，省掉单独的计数器；最后一行用条件表达式同时处理成功和失败；`deque` 保证 `popleft` 是 `O(1)`。
