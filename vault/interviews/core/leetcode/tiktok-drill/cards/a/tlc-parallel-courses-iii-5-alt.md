---
id: tlc-parallel-courses-iii-5-alt
node: a.parallel-courses-iii
type: qa
step: 5
---
## Q
**LC 2050 并行课程 III**｜另一种解法

不手写入度数组和队列，还有什么写法能解 LC 2050（`n <= 5 * 10^4`，先修关系是 DAG，课程可同时上）？它的复杂度是多少，什么时候该选它而不是 Kahn 算法？

## A
**标准库 `graphlib.TopologicalSorter`。** 它保证前驱先于后继出现。按这个顺序做 DP：`finish[v] = time[v - 1] + max(finish[p] for p in 先修课)`，没有先修课时取 `0`。

```python
from collections import defaultdict
from graphlib import TopologicalSorter


def minimum_time_graphlib(n: int, relations: list[list[int]], time: list[int]) -> int:
    pre: defaultdict[int, list[int]] = defaultdict(list)
    ts: TopologicalSorter[int] = TopologicalSorter()
    for i in range(1, n + 1):
        ts.add(i)
    for a, b in relations:
        pre[b].append(a)
        ts.add(b, a)                               # add(节点, *前驱)
    finish: dict[int, int] = {}
    for v in ts.static_order():                    # 前驱一定先出现
        finish[v] = time[v - 1] + max((finish[p] for p in pre[v]), default=0)
    return max(finish.values())
```

运行：`(3, [[1,3],[2,3]], [3,2,5])` → `8`；`(5, [[1,5],[2,5],[3,5],[3,4],[4,5]], [1,2,3,4,5])` → `12`；`5 * 10^4` 门课的链 → `500000000`。

**复杂度。** 时间 `O(n + m)`；空间 `O(n + m)`。与 Kahn 版本相同。

**另一条路：记忆化 DFS。** `finish(v) = time[v-1] + max(finish(p) for p in pre[v])`，加 `functools.cache`。写法最短，但依赖链最长 `5 * 10^4`，默认递归上限下直接 `RecursionError`；只在数据规模小或链短时使用。

**怎么选。**
- 面试要展示拓扑排序本身：手写 Kahn，能顺手讲清入度、环检测。
- 想要短而不易错的代码，且允许用标准库：`graphlib`，前驱先于后继已经由库保证。
- 链很深的大输入：不要用递归记忆化。
- Python 版本低于 3.9 没有 `graphlib`，只能手写。
