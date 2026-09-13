---
id: leetcode-c-endlesscheng-luu0kb-lca-binary-lifting-template
node: tree-advanced.lca-binary-lifting
type: cloze
anki: 1787272460180
tags: [concept-cloze, leetcode, recall, template]
---
同步上跳 LCA 时，从最高倍数向下，只有祖先不同才 {{c1::同时上跳}}。

```
def lca(up, depth, a, b):
    if depth[a] < depth[b]:
        a, b = b, a
    difference = depth[a] - depth[b]
    bit = 0
    while difference:
        if difference & 1:
            a = up[bit][a]
        difference >>= 1
        bit += 1
    if a == b:
        return a
    for level in range(len(up) - 1, -1, -1):
        if up[level][a] != up[level][b]:
            a = up[level][a]
            b = up[level][b]
    return up[0][a]
```

**Evidence**

三、图论：最近公共祖先、树上倍增

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.15%20-%20%E6%9C%80%E8%BF%91%E5%85%AC%E5%85%B1%E7%A5%96%E5%85%88%20LCA)
