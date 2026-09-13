---
id: leetcode-c-endlesscheng-v2rxsn-monotonic-stack-template
node: stack-queue-monotonic.monotonic-stack
type: cloze
anki: 1787272467379
tags: [concept-cloze, leetcode, recall, template]
---
处理“下一个更大元素”时，新值到来后弹出所有 {{c1::更小的栈顶}}。

```
def next_greater(nums):
    ans = [-1] * len(nums)
    stack = []
    for i, value in enumerate(nums):
        while stack and nums[stack[-1]] < value:
            ans[stack.pop()] = i
        stack.append(i)
    return ans
```

**Evidence**

四、数据结构：单调栈

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.16%20-%20%E5%8D%95%E8%B0%83%E6%A0%88)
