---
id: leetcode-q-height-checker-pattern
node: greedy-sorting.bubble-sort
type: qa
anki: 1787175409485
tags: [lc::1051, leetcode, pattern, recall]
---
## Q
如何判断数组中每个位置的元素是否处于「排序后应处的位置」？(如 LC 1051 Height Checker)

## A
将原数组排序得到 expected，逐位比较 heights[i] != expected[i]，统计不相等的个数即为答案。核心思路：排序后的数组即为每个位置的"正确目标值"，无需还原具体排列，只需比较位置对应关系。时间复杂度 O(n log n)，空间 O(n)。

**Evidence**

```
class Solution:
    def heightChecker(self, heights: List[int]) -> int:
        n = len(heights)
        expected = sorted(heights)
        return sum(heights[i] != expected[i] for i in range(n))
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1051%20-%20Height%20Checker)
