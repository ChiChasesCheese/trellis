---
id: leetcode-c-endlesscheng-wr1mjp-fenwick-and-segment-tree-template
node: advanced-ds-heap.fenwick-and-segment-tree
type: cloze
anki: 1787272473980
tags: [concept-cloze, leetcode, recall, template]
---
Fenwick 更新索引时的跳转是 {{c1::i += i & -i}}。

```
class Fenwick:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, delta):
        i += 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, i):
        total = 0
        i += 1
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total
```

**Evidence**

4. 数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.15%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E4%B8%8E%E7%BA%BF%E6%AE%B5%E6%A0%91)
