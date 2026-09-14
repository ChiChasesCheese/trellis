---
id: leetcode-c-endlesscheng-g0n5iy-hash-union-find-template
node: shortest-path-uf-flow.hash-union-find
type: cloze
anki: 1787272479380
tags: [concept-cloze, leetcode, recall, template]
---
哈希并查集可用 {{c1::parent.setdefault(x, x)}} 按需创建节点。

```
def components(edges):
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    for a, b in edges:
        ra = find(a)
        rb = find(b)
        if ra != rb:
            parent[ra] = rb
    return len({find(x) for x in parent})
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.12%20-%20%E5%93%88%E5%B8%8C%E5%B9%B6%E6%9F%A5%E9%9B%86)
