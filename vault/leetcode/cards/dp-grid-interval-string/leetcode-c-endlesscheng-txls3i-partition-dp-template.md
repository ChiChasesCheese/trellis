---
id: leetcode-c-endlesscheng-txls3i-partition-dp-template
node: dp-grid-interval-string.partition-dp
type: cloze
anki: 1787272413904
tags: [concept-cloze, leetcode, recall, template]
---
恰好 k 段的常见状态是 {{c1::dp[segments][prefix_length]}}。

```
def solve(nums):
    n = len(nums)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for left in range(i):
            if dp[left] and sum(nums[left:i]) >= 0:
                dp[i] = True
                break
    return dp[n]
```

**Evidence**

§5.3 约束划分个数

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.08%20-%20%E5%88%92%E5%88%86%E5%9E%8B%20DP)
