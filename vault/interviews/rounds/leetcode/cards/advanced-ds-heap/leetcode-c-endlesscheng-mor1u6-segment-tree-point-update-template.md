---
id: leetcode-c-endlesscheng-mor1u6-segment-tree-point-update-template
node: advanced-ds-heap.segment-tree-point-update
type: cloze
anki: 1789002115620
tags: [concept-cloze, leetcode, recall, template]
---
迭代线段树查询 [l,r) 的循环条件是 {{c1::l < r}}。

```
class SegTree:
    def __init__(self, nums):
        self.n = len(nums)
        self.t = [0] * (2 * self.n)
        self.t[self.n:] = nums
        for i in range(self.n - 1, 0, -1):
            self.t[i] = max(self.t[i * 2], self.t[i * 2 + 1])

    def query(self, l, r):
        ans = float('-inf')
        l += self.n
        r += self.n
        while l < r:
            if l & 1:
                ans = max(ans, self.t[l]); l += 1
            if r & 1:
                r -= 1; ans = max(ans, self.t[r])
            l //= 2; r //= 2
        return ans
```

**Evidence**

§8.3 线段树（无区间更新）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.15%20-%20%E7%BA%BF%E6%AE%B5%E6%A0%91%EF%BC%9A%E5%8D%95%E7%82%B9%E6%9B%B4%E6%96%B0%E4%B8%8E%E5%8C%BA%E9%97%B4%E8%81%9A%E5%90%88)
