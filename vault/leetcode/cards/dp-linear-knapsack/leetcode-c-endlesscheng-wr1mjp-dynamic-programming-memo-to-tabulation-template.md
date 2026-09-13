---
id: leetcode-c-endlesscheng-wr1mjp-dynamic-programming-memo-to-tabulation-template
node: dp-linear-knapsack.dynamic-programming-memo-to-tabulation
type: cloze
anki: 1787272471580
tags: [concept-cloze, leetcode, recall, template]
---
从递归开始设计 DP 时，先写 {{c1::dfs(state) 的含义、边界和所有决策分支}}，再加 cache。

```
from functools import cache

def min_cost(nums):
    @cache
    def dfs(i):
        if i >= len(nums):
            return 0
        take_one = nums[i] + dfs(i + 1)
        take_two = nums[i] + dfs(i + 2)
        return min(take_one, take_two)
    return dfs(0)
```

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.07%20-%20%E8%AE%B0%E5%BF%86%E5%8C%96%E6%90%9C%E7%B4%A2%E4%B8%8E%E9%80%92%E6%8E%A8%20Dynamic%20Programming)
