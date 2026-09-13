---
id: leetcode-c-endlesscheng-txls3i-reconstruct-dp-solution-template
node: dp-linear-knapsack.reconstruct-dp-solution
type: cloze
anki: 1787272417805
tags: [concept-cloze, leetcode, recall, template]
---
方案恢复通常从 {{c1::目标状态反向追踪 parent}}。

```
def solve(nums):
    dp = [0] * (len(nums) + 1)
    parent = [-1] * (len(nums) + 1)
    for i, x in enumerate(nums, 1):
        if dp[i - 1] + x > dp[i - 1]:
            dp[i] = dp[i - 1] + x
            parent[i] = i - 1
        else:
            dp[i] = dp[i - 1]
            parent[i] = i - 1
    path = []
    cur = len(nums)
    while cur > 0:
        path.append(cur)
        cur = parent[cur]
    return dp[-1], path[::-1]
```

**Evidence**

专题：输出具体方案（打印方案）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.21%20-%20DP%20%E6%96%B9%E6%A1%88%E8%BF%98%E5%8E%9F)
