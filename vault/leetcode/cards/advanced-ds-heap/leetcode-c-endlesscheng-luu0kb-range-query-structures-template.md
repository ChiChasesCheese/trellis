---
id: leetcode-c-endlesscheng-luu0kb-range-query-structures-template
node: advanced-ds-heap.range-query-structures
type: cloze
anki: 1787272460779
tags: [concept-cloze, leetcode, recall, template]
---
Fenwick 更新向上执行 i += i & -i，前缀查询向上汇总执行 {{c1::i -= i & -i}}。

```
class Fenwick:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, index, delta):
        index += 1
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def prefix_sum(self, index):
        total = 0
        index += 1
        while index > 0:
            total += self.tree[index]
            index -= index & -index
        return total
```

**Evidence**

四、数据结构：树状数组

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.17%20-%20%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84%E3%80%81%E7%BA%BF%E6%AE%B5%E6%A0%91%E4%B8%8E%E6%9C%80%E5%B0%8F%E5%A0%86)
