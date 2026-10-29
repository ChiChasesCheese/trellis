---
id: tlc-parallel-courses-iii-2-code
node: a.parallel-courses-iii
type: qa
step: 2
---
## Q
**LC 2050 并行课程 III**｜写出 Python 实现

`n` 门课（`1 <= n <= 5 * 10^4`），`relations` 里的 `[prev, next]` 表示先修关系（DAG），`time[i]` 是第 `i + 1` 门课的月数（`1 <= time[i] <= 10^4`），先修课全部完成即可开始一门课，可以同时上任意多门课，返回完成全部课程的最少月数。

## A
**思路。** 建邻接表和入度数组。入度为 `0` 的课入队。课程 `u` 出队时，完成时间 `finish = start[u] + time[u - 1]`；对每个后继 `v`，`start[v] = max(start[v], finish)`，入度减一，减到 `0` 就入队。用 `ans` 记录所有完成时间的最大值。

```python
from collections import deque


def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        graph[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)                          # start[v]：v 最早能开始的月份 = 所有先修课完成时间的最大值
    queue = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    ans = 0
    while queue:
        u = queue.popleft()
        finish = start[u] + time[u - 1]
        ans = max(ans, finish)
        for v in graph[u]:
            start[v] = max(start[v], finish)
            indeg[v] -= 1
            if indeg[v] == 0:                      # 先修课全部完成，start[v] 已定
                queue.append(v)
    return ans
```

运行：`(3, [[1,3],[2,3]], [3,2,5])` → `8`；`(5, [[1,5],[2,5],[3,5],[3,4],[4,5]], [1,2,3,4,5])` → `12`；`(1, [], [7])` → `7`；`(3, [], [1,9,4])` → `9`；`5 * 10^4` 门课的链 → `500000000`。

**复杂度。** 时间 `O(n + m)`：每条边、每个点处理一次；空间 `O(n + m)`：邻接表、入度、`start`。

**写法要点。** 用 `deque` 做队列，`popleft` 是 `O(1)`（`list.pop(0)` 是 `O(n)`）；下标从 `1` 开始所以数组长度开 `n + 1`，`time[u - 1]` 做偏移；生成器表达式 `deque(i for i in ... if indeg[i] == 0)` 一次建好初始队列；`start[v] = max(start[v], finish)` 保证取所有先修课中最晚完成的那个。
