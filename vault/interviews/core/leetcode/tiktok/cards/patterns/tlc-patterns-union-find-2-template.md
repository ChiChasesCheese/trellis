---
id: tlc-patterns-union-find-2-template
node: patterns.union-find
type: qa
step: 2
---
## Q
**并查集（Union-Find）｜模板：路径压缩 + 按大小合并**

写出并查集的标准类，说明两个优化各自解决什么问题。

## A
```python
class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n                     # 连通块个数

    def find(self, x: int) -> int:
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:      # 路径压缩：沿途的点直接挂到根上
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                   # 已经连通：加这条边会成环
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra               # 小树挂到大树下
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True
```

运行：`uf = UnionFind(5)`，`union(0,1)`、`union(1,2)` 返回 `True`，`union(0,2)` 返回 `False`，`uf.count` 为 `3`。

- **路径压缩**：`find` 之后让沿途节点直接指向根，下次查询接近 `O(1)`。没有它，一条退化成链的树（`10000` 个点串成一串）每次 `find(0)` 要走 `9999` 步。
- **按大小（或按秩）合并**：总是小树挂到大树下，树高 `O(log n)`。
- 两者合起来是摊还 `O(α(n))`，`α` 是反阿克曼函数，实际不超过 4。
- 迭代写 `find`，避免链很长时递归爆栈；递归写法 `if parent[x] != x: parent[x] = find(parent[x])` 更短，但链上千时会 `RecursionError`。
- `union` 返回布尔值：`False` 表示两端已连通，Kruskal 判环、统计冗余边都靠它。
- 非整数节点（邮箱、字符串）用 `dict` 先映射成编号。
