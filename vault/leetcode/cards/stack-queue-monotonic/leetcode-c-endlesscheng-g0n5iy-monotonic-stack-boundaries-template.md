---
id: leetcode-c-endlesscheng-g0n5iy-monotonic-stack-boundaries-template
node: stack-queue-monotonic.monotonic-stack-boundaries
type: cloze
anki: 1787272480880
tags: [concept-cloze, leetcode, recall, template]
---
求右侧第一个严格更小值时，弹栈条件可写为 {{c1::nums[stack[-1]] > x}}。

```
def next_smaller_right(nums):
    n = len(nums)
    ans = [n] * n
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] > x:
            ans[stack.pop()] = i
        stack.append(i)
    return ans
```

**Evidence**

数据结构

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.17%20-%20%E5%8D%95%E8%B0%83%E6%A0%88%E8%BE%B9%E7%95%8C%E5%AE%9A%E4%BD%8D)
