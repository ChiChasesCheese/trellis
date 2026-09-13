---
id: leetcode-c-endlesscheng-mor1u6-weighted-union-find-template
node: shortest-path-uf-flow.weighted-union-find
type: cloze
anki: 1787272422908
tags: [concept-cloze, leetcode, recall, template]
---
递归 find 后，应执行 weight[x] += {{c1::weight[old_parent]}}。

```
class WeightedUF:
    def __init__(self, n):
        self.p = list(range(n))
        self.w = [0] * n

    def find(self, x):
        if self.p[x] != x:
            parent = self.p[x]
            root = self.find(parent)
            self.w[x] += self.w[parent]
            self.p[x] = root
        return self.p[x]
```

**Evidence**

§7.6 带权并查集（边权并查集）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.17%20-%20%E5%B8%A6%E6%9D%83%E5%B9%B6%E6%9F%A5%E9%9B%86)
