---
id: leetcode-c-endlesscheng-txls3i-optimized-dp-data-structures-template
node: dp-linear-knapsack.optimized-dp-data-structures
type: cloze
anki: 1787272416005
tags: [concept-cloze, leetcode, recall, template]
---
插入新候选前，弹出所有不会再优于它的 {{c1::队尾候选}}。

```
from collections import deque

def solve(nums, width):
    dp = [0] * len(nums)
    q = deque()
    for i, x in enumerate(nums):
        while q and q[0] < i - width:
            q.popleft()
        dp[i] = x + (dp[q[0]] if q else 0)
        while q and dp[q[-1]] <= dp[i]:
            q.pop()
        q.append(i)
    return max(dp, default=0)
```

**Evidence**

§11.3 单调队列优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.15%20-%20%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%BC%98%E5%8C%96%20DP)
