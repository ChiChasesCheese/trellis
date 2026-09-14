---
id: leetcode-c-endlesscheng-mor1u6-lazy-dynamic-persistent-segment-tree-template
node: advanced-ds-heap.lazy-dynamic-persistent-segment-tree
type: cloze
anki: 1789002115920
tags: [concept-cloze, leetcode, recall, template]
---
区间加作用于长度 len 的区间和时，节点值增加 {{c1::delta*len}}。

```
def apply(tree, lazy, node, left, right, delta):
    tree[node] += delta * (right - left + 1)
    lazy[node] += delta

def push(tree, lazy, node, left, right):
    if lazy[node] == 0 or left == right:
        return
    mid = (left + right) // 2
    apply(tree, lazy, node * 2, left, mid, lazy[node])
    apply(tree, lazy, node * 2 + 1, mid + 1, right, lazy[node])
    lazy[node] = 0
```

**Evidence**

§8.4 Lazy 线段树（有区间更新）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.16%20-%20Lazy%E3%80%81%E5%8A%A8%E6%80%81%E5%BC%80%E7%82%B9%E4%B8%8E%E5%8F%AF%E6%8C%81%E4%B9%85%E5%8C%96%E7%BA%BF%E6%AE%B5%E6%A0%91)
