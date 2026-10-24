---
id: tlc-patterns-union-find-6-variants
node: patterns.union-find
type: qa
step: 6
---
## Q
**并查集（Union-Find）｜变形：按块统计（LC 924）与带权并查集（LC 399）**

"移除哪个感染点最划算"为什么只看块内恰好一个感染点的块？除法求值怎样让并查集带上比值？

## A
**LC 924**：先合并连通块，统计每块大小和块内初始感染点个数。若一块里有两个或更多感染点，移除其中一个，块仍会被另一个感染，没有收益；若**恰好一个**，移除它就救下整块。

```python
from collections import Counter
class UnionFind:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        self.p[ra] = rb
        return ra != rb

def min_malware_spread(graph: list[list[int]], initial: list[int]) -> int:
    n = len(graph)
    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if graph[i][j]:
                uf.union(i, j)
    size = Counter(uf.find(i) for i in range(n))
    infected = Counter(uf.find(x) for x in initial)
    best_save, ans = -1, min(initial)
    for x in sorted(initial):              # 从小到大：并列时保留编号最小的
        root = uf.find(x)
        save = size[root] if infected[root] == 1 else 0
        if save > best_save:
            best_save, ans = save, x
    return ans
```

运行：`([[1,1,0],[1,1,0],[0,0,1]], [0,1])` → `0`；`([[1,0,0],[0,1,0],[0,0,1]], [0,2])` → `0`；`([[1,1,1],[1,1,1],[1,1,1]], [1,2])` → `1`。一个都救不了时返回 `min(initial)`。

**LC 399 带权并查集**：每个点记 `ratio[x] = x / parent[x]`。`find` 压缩路径时累乘比值：`x/root = (x/parent) * (parent/root)`；`union(a, b, v)`（`a / b = v`）把 `a` 的根挂到 `b` 的根下，根与根的比值设为 `v * ratio[b] / ratio[a]`。查询 `c / d`：两者在同一个块里时等于 `ratio[c] / ratio[d]`，否则 `-1.0`。例：`a/b=2, b/c=3` 时 `a/c = 6.0`，`b/a = 0.5`。变量数 `<= 40`，DFS 建图也可行。
