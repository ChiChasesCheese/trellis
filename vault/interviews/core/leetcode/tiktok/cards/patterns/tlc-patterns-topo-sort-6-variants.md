---
id: tlc-patterns-topo-sort-6-variants
node: patterns.topo-sort
type: qa
step: 6
---
## Q
**拓扑排序（Topological Sort）｜变形：间接先修课查询（LC 1462）**

按拓扑序做 DP 是什么意思？先修课的间接关系怎么查？

## A
**核心**：处理一个点时，它的所有前驱都已处理完，所以可以直接用前驱的结果。

**LC 1462 先修课程（间接）**：查询 `u` 是不是 `v` 的先修课（含间接）。按拓扑序，把每个点的"所有祖先"存成位掩码，后继继承前驱的祖先再加上前驱自己。注意 LC 1462 的 `[a, b]` 表示 **`a` 是 `b` 的先修课**，与 LC 207 的方向相反。

```python
from collections import deque
def check_if_prerequisite(num_courses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> list[bool]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        graph[a].append(b)
        indeg[b] += 1
    reach = [0] * num_courses              # reach[v]：v 的所有先修课（位掩码）
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    while q:
        u = q.popleft()
        for v in graph[u]:
            reach[v] |= reach[u] | (1 << u)   # v 继承 u 的先修课，再加 u 本身
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return [bool(reach[v] >> u & 1) for u, v in queries]
print(check_if_prerequisite(2, [[1,0]], [[0,1],[1,0]]), check_if_prerequisite(3, [[1,2],[1,0],[2,0]], [[1,0],[1,2]]))   # [False, True] [True, True]
```

数据范围 `numCourses <= 100`，Floyd 传递闭包 `O(n^3)` 也可行。
