---
id: tlc-patterns-topo-sort-6-variants
node: patterns.topo-sort
type: qa
step: 6
---
## Q
**拓扑排序（Topological Sort）｜变形：并行课程的最短完成时间（LC 2050）与间接先修关系的传递闭包**

按拓扑序做 DP 是什么意思？先修课的间接关系怎么查？

## A
- **拓扑序上的 DP**：处理一个点时，它的所有前驱都已处理完，所以可以直接用前驱的结果。并行课程里，一门课的开始时间 = 所有先修课完成时间的最大值，完成时间 = 开始时间 + 课程用时，答案是所有完成时间的最大值（例：LC 2050 并行课程 III）。
- **传递闭包**：按拓扑序，把每个点的"所有祖先"存成位掩码，后继继承前驱的祖先再加上前驱自己：`pre[v] |= pre[u] | (1 << u)`。节点数很小（约 100 以内）时，Floyd 传递闭包 `O(n^3)` 也可行。

**例题：** LC 2050 并行课程 III

`n` 门课、先修关系 `relations`（DAG）、每门课的用时 `time`（月），课程可以同时上，求完成所有课程的最少月数，`1 <= n <= 5 * 10^4`。

```python
from collections import deque
def minimum_time(n: int, relations: list[list[int]], time: list[int]) -> int:
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for a, b in relations:
        graph[a].append(b)
        indeg[b] += 1
    start = [0] * (n + 1)
    queue = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    ans = 0
    while queue:
        u = queue.popleft()
        finish = start[u] + time[u - 1]
        ans = max(ans, finish)
        for v in graph[u]:
            start[v] = max(start[v], finish)
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return ans
```
