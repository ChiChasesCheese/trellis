---
id: leetcode-c-endlesscheng-mor1u6-monotonic-stack-template
node: stack-queue-monotonic.monotonic-stack
type: cloze
anki: 1787272420506
tags: [concept-cloze, leetcode, recall, template]
---
求下一个更大元素时，当前 x 会弹出所有 {{c1::栈顶值小于 x}} 的下标。

```
def next_greater(nums):
    ans = [-1] * len(nums)
    stack = []
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            ans[stack.pop()] = i
        stack.append(i)
    return ans
```

**Evidence**

§3.7 单调栈

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F08.09%20-%20%E5%8D%95%E8%B0%83%E6%A0%88)
