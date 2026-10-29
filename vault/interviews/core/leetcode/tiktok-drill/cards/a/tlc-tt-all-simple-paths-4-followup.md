---
id: tlc-tt-all-simple-paths-4-followup
node: a.tt-all-simple-paths
type: qa
step: 4
---
## Q
**枚举有向图中的所有简单路径（含环的情况）**｜追问

写完有环图的 `s → t` 简单路径枚举后，面试官接着问：（1）如果图保证无环（DAG），可以怎样简化？（2）把图里所有的简单环也列出来，每个环只出现一次。

## A
1. **DAG。** 无环时任何沿边走的路径天然不重复，`on_path` 可以去掉。还可以记忆化「从 `u` 到 `t` 的全部路径」，汇合点的后半段只算一次（LC 797）。用元组存，可以安全地被多个前缀共享：

```python
from functools import cache


def dag_paths(n: int, edges: list[list[int]], s: int, t: int) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    @cache
    def from_(u: int) -> tuple[tuple[int, ...], ...]:   # u 到 t 的全部路径
        if u == t:
            return ((t,),)
        return tuple((u, *p) for v in graph[u] for p in from_(v))

    return [list(p) for p in from_(s)]
```

2. **所有简单环。** 同一个环从它的每个点出发都能走一遍，会重复。规定只从环上**编号最小**的点 `start` 记录：DFS 只进编号大于 `start` 的点，某条边回到 `start` 就记下当前路径。自环在 `start` 本身就会被记成 `[start]`。

```python
def simple_cycles(n: int, edges: list[list[int]]) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    cycles: list[list[int]] = []
    for start in range(n):
        path, on_path = [start], {start}

        def dfs(u: int) -> None:
            for v in graph[u]:
                if v == start:
                    cycles.append(path.copy())
                elif v > start and v not in on_path:
                    on_path.add(v); path.append(v)
                    dfs(v)
                    path.pop(); on_path.discard(v)

        dfs(start)
    return cycles
```

   运行：`n = 3`，`edges = [[0,1],[1,2],[2,0],[1,0],[2,2]]` → `[[0, 1, 2], [0, 1], [2]]`。环很多时可提 Johnson 算法，它保证每输出一个环只花 `O(n + m)`。

**Python 提醒**：`@cache` 的返回值被所有调用方共享，记忆化返回 `list` 时调用方一改，缓存就被污染；返回元组（不可变）才安全。
