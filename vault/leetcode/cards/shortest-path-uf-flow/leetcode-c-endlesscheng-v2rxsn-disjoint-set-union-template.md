---
id: leetcode-c-endlesscheng-v2rxsn-disjoint-set-union-template
node: shortest-path-uf-flow.disjoint-set-union
type: cloze
anki: 1787272467679
tags: [concept-cloze, leetcode, recall, template]
---
合并前先比较 {{c1::find(a) 和 find(b)}}，相同则无需合并。

```
def make_dsu(n):
    parent = list(range(n))
    size = [1] * n
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True
    return find, union
```

**Evidence**

四、数据结构：并查集

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.17%20-%20%E5%B9%B6%E6%9F%A5%E9%9B%86)
