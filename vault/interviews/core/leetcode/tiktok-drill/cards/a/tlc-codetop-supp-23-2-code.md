---
id: tlc-codetop-supp-23-2-code
node: a.codetop-supp-23
type: qa
step: 2
---
## Q
**补充题23 检测循环依赖**｜写出 Python 实现

`n` 个模块（`1 <= n <= 10^5`），依赖列表 `deps`（至多 `2 * 10^5` 项，`[a, b]` 表示 `a` 依赖 `b`，可能重复，可能自依赖）。返回依赖中是否存在循环。要求 `O(n + m)`，且 `10^5` 层的依赖链不能触发递归错误。

## A
**思路。** 按「`b` 先于 `a`」建边 `b -> a` 并统计入度，Kahn 算法：入度为 `0` 的模块入队，出队时把它指向的模块入度减一，减到 `0` 的入队。出队总数小于 `n` 就是有环。

```python
from collections import deque

def has_cycle(n: int, deps: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:                       # a 依赖 b：先有 b 才能有 a，边 b -> a
        graph[b].append(a)
        indeg[a] += 1
    queue = deque(i for i in range(n) if indeg[i] == 0)   # 没有任何前置依赖的模块先上
    done = 0
    while queue:
        u = queue.popleft()
        done += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return done < n                         # 有模块始终入度不为 0：它们在环上或依赖环上的模块
```

运行：`(3, [[1,0],[2,1]])` → `False`，`(3, [[0,1],[1,2],[2,0]])` → `True`，`(1, [[0,0]])` → `True`，`(4, [[1,0],[2,1],[3,2],[1,3]])` → `True`，`(2, [])` → `False`；`10^5` 个模块的一条链 → `False`，加上首尾相连的一条依赖 → `True`。

**复杂度。** 时间 `O(n + m)`：每个模块入队出队各一次，每条边被扣减一次；空间 `O(n + m)`：邻接表、入度数组和队列。

**写法要点。**
- `[[] for _ in range(n)]` 建邻接表；不能写 `[[]] * n`，那样所有位置是同一个列表。
- `for a, b in deps` 直接解包依赖对，名字和题意对应（`a` 依赖 `b`）。
- `deque(i for i in range(n) if indeg[i] == 0)` 用生成器一步建出初始队列；`popleft()` 是 `O(1)`，列表的 `pop(0)` 是 `O(n)`。
- 只用一个计数器 `done`，不需要保存拓扑序；需要顺序时（LC 210）改成追加到列表。
- 标准库有现成的 `graphlib.TopologicalSorter`，遇到环抛 `CycleError`，面试里可以提一句，但要先手写。
