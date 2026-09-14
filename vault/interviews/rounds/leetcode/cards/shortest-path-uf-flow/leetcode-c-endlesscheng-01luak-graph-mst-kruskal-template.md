---
id: leetcode-c-endlesscheng-01luak-graph-mst-kruskal-template
node: shortest-path-uf-flow.graph-mst-kruskal
type: cloze
anki: 1787272410305
tags: [concept-cloze, leetcode, recall, template]
---
Kruskal 算法的第一步是将所有边按 {{c1::权值从小到大}} 排序，再依次尝试用并查集合并。

```
class UnionFind:
    def __init__(self, n: int):
        self._fa = list(range(n))
        self.cc = n

    def find(self, x: int) -> int:
        if self._fa[x] != x:
            self._fa[x] = self.find(self._fa[x])
        return self._fa[x]

    def merge(self, from_: int, to: int) -> bool:
        x, y = self.find(from_), self.find(to)
        if x == y:
            return False
        self._fa[x] = y
        self.cc -= 1
        return True

import math

# returns total edge weight of the MST, or math.inf if the graph is disconnected
def solve(n: int, edges: list[list[int]]) -> float:
    edges = sorted(edges, key=lambda e: e[2])

    uf = UnionFind(n)
    sum_wt = 0
    for x, y, wt in edges:
        if uf.merge(x, y):
            sum_wt += wt

    if uf.cc > 1:
        return math.inf
    return sum_wt
```

**Evidence**

四、最小生成树模板代码

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F06.09%20-%20%E6%9C%80%E5%B0%8F%E7%94%9F%E6%88%90%E6%A0%91%EF%BC%9AKruskal%20%E7%AE%97%E6%B3%95)
