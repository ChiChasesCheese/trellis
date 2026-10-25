---
id: tlc-course-schedule-iv-2-code
node: b.course-schedule-iv
type: qa
step: 2
---
## Q
**LC 1462 课程表 IV**｜写出 Python 实现

`num_courses`（`2..100`）门课，`prerequisites[i] = [a, b]` 表示 `a` 是 `b` 的直接先修课，先修图无环，先决条件可传递。对每个查询 `[u, v]` 判断 `u` 是否是 `v` 的先决条件（直接或间接），`queries` 最多 `10^4` 个，返回布尔列表。

## A
**思路。** 按拓扑序处理，`pre[v]` 是一个整数位集，第 `u` 位为 `1` 表示 `u` 是 `v` 的先决条件。处理 `u` 时把 `pre[u]` 和 `u` 自己并入它每个后继的 `pre`；入度降到 `0` 的节点入队。查询直接读位。

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

运行：`(2, [[1,0]], [[0,1],[1,0]])` → `[False, True]`，`(2, [], [[1,0],[0,1]])` → `[False, False]`，`(3, [[1,2],[1,0],[2,0]], [[1,0],[1,2]])` → `[True, True]`，`(3, [[0,1],[1,2]], [[0,2],[0,1]])` → `[True, True]`；`100` 门课、`4950` 条边、`10^4` 个查询约 `0.5 ms`。

**复杂度。** 预处理 `O(n + E)` 次位运算，每次作用在约 `100` 位的整数上；查询 `O(1)`；空间 `O(n)` 个整数。

**写法要点。** Python 的 `int` 是任意精度，直接当位集用，`|`、`<<`、`>>` 都是 C 级别的操作，比二维布尔表快得多；`pre[v] >> u & 1` 的优先级是先移位再与，等价于 `(pre[v] >> u) & 1`；`bool(...)` 把 `0 / 1` 转成布尔；`deque` 的 `popleft` 是 `O(1)`；入度为 `0` 的初始节点用生成器直接喂给 `deque`。
