---
id: tlc-parallel-courses-iii-4-followup
node: a.parallel-courses-iii
type: qa
step: 4
---
## Q
**LC 2050 并行课程 III**｜追问

面试官接着问：（1）输出关键路径上的是哪几门课？（2）输入可能有环，如何检测？（3）同一时间最多只能上 `k` 门课？分别怎么改。

## A
1. **关键路径**：更新 `start[v]` 变大时同时记下 `prev[v] = u`（取得最大完成时间的那个先修课）。算完后找到完成时间最大的课程 `end`，沿 `prev` 一直回溯到入度为 `0` 的课，反转即是关键路径。
2. **检测环**：统计出队课程数。拓扑排序结束时出队数小于 `n`，说明剩下的课程互相等待，存在环；这题保证无环，但真实系统里应当检查。标准库的 `prepare()` 一步完成这个检查：

```python
from graphlib import CycleError, TopologicalSorter


def has_cycle(n: int, relations: list[list[int]]) -> bool:
    ts: TopologicalSorter[int] = TopologicalSorter()
    for i in range(1, n + 1):
        ts.add(i)
    for a, b in relations:
        ts.add(b, a)
    try:
        ts.prepare()                       # 有环时这里抛 graphlib.CycleError
    except CycleError:
        return True
    return False
```

   `has_cycle(2, [[1,2],[2,1]])` → `True`，`has_cycle(3, [[1,3],[2,3]])` → `False`。

3. **最多同时上 `k` 门**：问题变成"带资源约束的调度"，一般情形是 NP 难，没有简单的最优算法。面试里的做法是贪心：用优先队列，每次从可开始的课里选「后续依赖链最长」的先上，用一个"进行中的课"小根堆记录完成时间，不保证最优，但常作为启发式；要说清它是启发式。

**Python 提醒**：`graphlib.TopologicalSorter`（Python 3.9+）的 `add(node, *predecessors)` 把前驱写在节点后面；`prepare()` 会检测环并抛 `CycleError`，`static_order()` 内部同样会调用它；捕获时写具体的 `CycleError`，不要用裸的 `except Exception`，否则会把其他错误也当成「有环」。
