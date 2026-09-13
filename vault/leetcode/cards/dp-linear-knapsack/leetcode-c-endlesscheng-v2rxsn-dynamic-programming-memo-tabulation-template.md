---
id: leetcode-c-endlesscheng-v2rxsn-dynamic-programming-memo-tabulation-template
node: dp-linear-knapsack.dynamic-programming-memo-tabulation
type: cloze
anki: 1787272464679
tags: [concept-cloze, leetcode, recall, template]
---
不确定递推顺序时，先写 {{c1::记忆化搜索}} 来验证状态和转移。

```
def min_cost(nums):
    n = len(nums)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i - 1] + nums[i - 1]
    return dp[n]
```

**Evidence**

二、动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F89.07%20-%20%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%EF%BC%9A%E8%AE%B0%E5%BF%86%E5%8C%96%E6%90%9C%E7%B4%A2%E4%B8%8E%E9%80%92%E6%8E%A8)
