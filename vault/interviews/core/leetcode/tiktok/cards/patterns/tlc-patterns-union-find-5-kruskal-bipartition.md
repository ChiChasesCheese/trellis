---
id: tlc-patterns-union-find-5-kruskal-bipartition
node: patterns.union-find
type: qa
step: 5
---
## Q
**并查集（Union-Find）｜Kruskal 最小生成树（LC 1584）与"敌人的敌人"（LC 886）**

连接所有点的最小费用为什么是"边按权排序 + 判环"？二分图问题怎么用并查集表达？

## A
```python
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
        return ra != rb                    # False 表示已连通，再加这条边会成环

def min_cost_connect_points(points: list[list[int]]) -> int:
    n = len(points)
    edges = sorted((abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
                   for i in range(n) for j in range(i + 1, n))
    uf = UnionFind(n)
    total = used = 0
    for w, i, j in edges:                  # Kruskal：从最便宜的边开始
        if uf.union(i, j):
            total += w
            used += 1
            if used == n - 1:
                break
    return total

def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    uf = UnionFind(2 * n + 2)              # 点 i 表示"i 在 A 组"，点 i + n 表示"i 在 B 组"
    for a, b in dislikes:
        uf.union(a, b + n)                 # a 在 A <=> b 在 B
        uf.union(a + n, b)
        if uf.find(a) == uf.find(a + n):   # 同一个人既在 A 又在 B：矛盾
            return False
    return True
```

运行：`[[0,0],[2,2],[3,10],[5,2],[7,0]]` → `20`；`[[3,12],[-2,5],[-4,1]]` → `18`；`[[0,0]]` → `0`。`possible_bipartition(4, [[1,2],[1,3],[2,4]])` → `True`；`(3, [[1,2],[1,3],[2,3]])` → `False`（三个人两两互不喜欢，奇数环）。

- **Kruskal 的正确性**：最便宜且不成环的边总可以放进某棵最小生成树（割性质）。`union` 返回 `False` 时那条边会成环，跳过。
- `n = 1000` 时约 `5 * 10^5` 条边，排序 `O(E log E)`；稠密图也可用 Prim（堆）。
- 拆点技巧：每个人变成两个点，"对立"变成"A 与 B 交叉合并"，矛盾就是同一个人的两个点被合并。同样的拆点可以做所有"奇偶 / 二选一"约束。
