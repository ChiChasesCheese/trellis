---
id: leetcode-c-endlesscheng-g6ktkl-median-minimize-l1-template
node: greedy-sorting.median-minimize-l1
type: cloze
anki: 1787272436108
tags: [concept-cloze, leetcode, recall, template]
---
排序后可用 {{c1::nums[len(nums) // 2]}} 作为一个最优中位数。

```
def min_moves_to_equal(nums: list[int]) -> int:
    nums.sort()
    median = nums[len(nums) // 2]
    return sum(abs(x - median) for x in nums)
```

**Evidence**

§4.5

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F10.16%20-%20%E4%B8%AD%E4%BD%8D%E6%95%B0%E8%B4%AA%E5%BF%83)
