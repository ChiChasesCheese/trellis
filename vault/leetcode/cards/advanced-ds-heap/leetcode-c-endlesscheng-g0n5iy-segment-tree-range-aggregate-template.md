---
id: leetcode-c-endlesscheng-g0n5iy-segment-tree-range-aggregate-template
node: advanced-ds-heap.segment-tree-range-aggregate
type: cloze
anki: 1787272480580
tags: [concept-cloze, leetcode, recall, template]
---
迭代线段树查询半开区间 [left, right) 时，循环条件是 {{c1::left < right}}。

```
class SegmentTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.tree = [0] * (2 * self.n)
        self.tree[self.n:] = nums
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]

    def query(self, left, right):
        left += self.n
        right += self.n
        total = 0
        while left < right:
            if left & 1:
                total += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                total += self.tree[right]
            left //= 2
            right //= 2
        return total
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.16%20-%20%E7%BA%BF%E6%AE%B5%E6%A0%91%E5%8C%BA%E9%97%B4%E8%81%9A%E5%90%88%E4%B8%8E%E5%AE%9A%E4%BD%8D)
