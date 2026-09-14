---
id: leetcode-c-endlesscheng-g0n5iy-fenwick-tree-prefix-counts-template
node: advanced-ds-heap.fenwick-tree-prefix-counts
type: cloze
anki: 1787272479980
tags: [concept-cloze, leetcode, recall, template]
---
树状数组更新索引 i 后，下一个位置是 {{c1::i += i & -i}}。

```
class Fenwick:
    def __init__(self, n):
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        while i < len(self.bit):
            self.bit[i] += delta
            i += i & -i

    def prefix(self, i):
        total = 0
        while i > 0:
            total += self.bit[i]
            i -= i & -i
        return total
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.14%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E5%89%8D%E7%BC%80%E8%AE%A1%E6%95%B0)
