---
id: tlc-patterns-topo-sort-2-template
node: patterns.topo-sort
type: qa
step: 2
---
## Q
**拓扑排序（Topological Sort）｜模板：Kahn 算法（课程表 II）**

写出用入度表的拓扑排序，并同时回答「能否完成」和「给出一个顺序」。

## A
```python
from collections import deque
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for course, pre in prerequisites:
        graph[pre].append(course)          # 边方向：先修课 -> 后修课
        indeg[course] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    order: list[int] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:              # 所有先修课都已取出
                q.append(v)
    return order if len(order) == num_courses else []   # 有环：环上的点入度永远降不到 0
```

运行：`(2, [[1,0]])` → `[0, 1]`；`(4, [[1,0],[2,0],[3,1],[3,2]])` → `[0, 1, 2, 3]`；`(1, [])` → `[0]`；`(2, [[0,1],[1,0]])` → `[]`。时间 `O(V + E)`，空间 `O(V + E)`。

- 题面 `[a, b]` 的含义："学 `a` 之前先学 `b`"，所以边是 `b -> a`。方向写反，课程 `[[1,0]]` 会得到 `[1, 0]`。
- LC 207 只问能否完成：返回 `len(order) == num_courses` 即可。
- 同时取出的点可以按层处理：把 `while q` 里的循环按 `len(q)` 分层，层数就是最少学期数。
- 想得到字典序最小的拓扑序：把 `deque` 换成最小堆 `heapq`，每次弹出编号最小的入度为 0 的点，`O(V log V + E)`。
