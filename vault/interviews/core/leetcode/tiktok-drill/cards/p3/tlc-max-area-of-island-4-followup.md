---
id: tlc-max-area-of-island-4-followup
node: p3.max-area-of-island
type: qa
step: 4
---
## Q
**LC 695 岛屿的最大面积**｜追问

面试官接着问：（1）不允许修改输入怎么办？（2）如果格子是一个个变成陆地的，每次要报告当前最大岛屿面积？（3）矩阵很大，放不进内存？

## A
1. **不改输入**：先深拷贝再沉岛，`grid = [row[:] for row in grid]`（`grid[:]` 只复制外层，内层行仍是同一份）；或者另开 `seen = set()`，入栈时加入集合，多花 `O(mn)` 空间。
2. **动态加陆地（LC 305 的思路）**：用并查集（union-find）维护每块的大小，新格子与四邻中已是陆地的合并，同时更新全局最大面积；每次操作近似 `O(α(mn))`：

```python
class IslandArea:
    def __init__(self, m: int, n: int) -> None:
        self.m, self.n = m, n
        self.parent: dict[int, int] = {}       # 只存已变成陆地的格子
        self.size: dict[int, int] = {}
        self.best = 0

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 路径折半
            x = self.parent[x]
        return x

    def add_land(self, i: int, j: int) -> int:     # 把 (i, j) 变成陆地，返回当前最大岛屿面积
        cell = i * self.n + j
        if cell in self.parent:
            return self.best
        self.parent[cell], self.size[cell] = cell, 1
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            nb = ni * self.n + nj
            if 0 <= ni < self.m and 0 <= nj < self.n and nb in self.parent:
                a, b = self.find(cell), self.find(nb)
                if a != b:
                    self.parent[b] = a
                    self.size[a] += self.size[b]
        self.best = max(self.best, self.size[self.find(cell)])
        return self.best
```

3. **矩阵放不下内存**：按行分块处理，每块内部求连通分量，块边界上用并查集把上下两行的分量合并；只保留当前行和上一行的分量编号，内存降到 `O(n)`，思路和分布式连通域标记一致。

**Python 提醒**：`[[0] * n] * m` 得到的是 `m` 个指向同一行的引用，改一格全列都变；造矩阵要用 `[[0] * n for _ in range(m)]`。
