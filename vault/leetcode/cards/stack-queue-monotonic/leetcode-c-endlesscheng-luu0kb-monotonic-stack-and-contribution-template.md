---
id: leetcode-c-endlesscheng-luu0kb-monotonic-stack-and-contribution-template
node: stack-queue-monotonic.monotonic-stack-and-contribution
type: cloze
anki: 1787272460480
tags: [concept-cloze, leetcode, recall, template]
---
元素 mid 作为子数组最小值的数量是 (mid-left) × {{c1::(right-mid)}}。

```
def sum_subarray_mins(nums):
    mod = 10**9 + 7
    stack = []
    total = 0
    for i, value in enumerate(nums + [float('-inf')]):
        while stack and nums[stack[-1]] >= value:
            mid = stack.pop()
            left = stack[-1] if stack else -1
            total += nums[mid] * (mid - left) * (i - mid)
        stack.append(i)
    return total % mod
```

**Evidence**

四、数据结构：贡献法

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.16%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E4%B8%8E%E8%B4%A1%E7%8C%AE%E6%B3%95)
