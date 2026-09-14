---
id: leetcode-c-endlesscheng-9ozfk9-monotonic-stack-nearest-boundary-template
node: stack-queue-monotonic.monotonic-stack-nearest-boundary
type: cloze
anki: 1787272403105
tags: [concept-cloze, leetcode, recall, template]
---
单调栈模板通常存 {{c1::下标}}，这样可直接得到边界位置与距离。

```
def nearest_left_greater(nums: list[int]) -> list[int]:
    left = [-1] * len(nums)
    stack: list[int] = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] <= x:
            stack.pop()
        if stack:
            left[i] = stack[-1]
        stack.append(i)
    return left
```

**Evidence**

一、单调栈 > §1.1 基础

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F03.01%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E6%B1%82%E6%9C%80%E8%BF%91%E6%94%AF%E9%85%8D%E8%BE%B9%E7%95%8C)
