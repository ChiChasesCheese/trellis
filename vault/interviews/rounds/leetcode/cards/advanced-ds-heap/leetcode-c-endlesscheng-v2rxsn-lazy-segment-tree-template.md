---
id: leetcode-c-endlesscheng-v2rxsn-lazy-segment-tree-template
node: advanced-ds-heap.lazy-segment-tree
type: cloze
anki: 1787272468279
tags: [concept-cloze, leetcode, recall, template]
---
对完整覆盖节点做区间加法时，同时更新节点聚合值和 {{c1::lazy 标记}}。

```
class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.sum = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
    def apply(self, node, left, right, value):
        self.sum[node] += (right - left + 1) * value
        self.lazy[node] += value
    def push(self, node, left, right):
        if self.lazy[node] and left != right:
            mid = (left + right) // 2
            self.apply(node * 2, left, mid, self.lazy[node])
            self.apply(node * 2 + 1, mid + 1, right, self.lazy[node])
            self.lazy[node] = 0
```

**Evidence**

四、数据结构：lazy 线段树

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.19%20-%20Lazy%20%E7%BA%BF%E6%AE%B5%E6%A0%91)
