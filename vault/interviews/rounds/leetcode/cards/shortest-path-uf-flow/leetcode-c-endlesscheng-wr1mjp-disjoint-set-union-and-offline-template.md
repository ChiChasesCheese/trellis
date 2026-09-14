---
id: leetcode-c-endlesscheng-wr1mjp-disjoint-set-union-and-offline-template
node: shortest-path-uf-flow.disjoint-set-union-and-offline
type: cloze
anki: 1787272473680
tags: [concept-cloze, leetcode, recall, template]
---
支持路径压缩的 find 会执行 {{c1::parent[x] = parent[parent[x]]}} 或递归压缩。

```
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True
```

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.14%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86%E4%B8%8E%E7%A6%BB%E7%BA%BF%E5%A4%84%E7%90%86)
