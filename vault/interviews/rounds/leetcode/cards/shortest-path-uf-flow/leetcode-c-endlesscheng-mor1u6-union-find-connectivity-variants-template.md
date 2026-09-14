---
id: leetcode-c-endlesscheng-mor1u6-union-find-connectivity-variants-template
node: shortest-path-uf-flow.union-find-connectivity-variants
type: cloze
anki: 1789002114994
tags: [concept-cloze, leetcode, recall, template]
---
路径压缩应把 parent[x] 改为 {{c1::find(parent[x])}}。

```
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        self.parent[a] = b
        return True
```

**Evidence**

七、并查集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.12%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%EF%BC%9A%E8%BF%9E%E9%80%9A%E6%80%A7%E3%80%81%E4%B8%AD%E4%BB%8B%E3%80%81%E8%B7%B3%E8%BF%87%E4%B8%8E%E5%8C%BA%E9%97%B4)
