---
id: leetcode-c-endlesscheng-luu0kb-dp-optimizations-monotonic-queue-fenwick-template
node: dp-linear-knapsack.dp-optimizations-monotonic-queue-fenwick
type: cloze
anki: 1787272458980
tags: [concept-cloze, leetcode, recall, template]
---
求窗口最大 dp 时，插入新下标前弹出队尾所有 dp 值 {{c1::不大于新值}} 的元素。

```
from collections import deque

def window_max_dp(values, width):
    dp = [0] * len(values)
    queue = deque()
    for i, value in enumerate(values):
        while queue and queue[0] < i - width:
            queue.popleft()
        best = dp[queue[0]] if queue else 0
        dp[i] = best + value
        while queue and dp[queue[-1]] <= dp[i]:
            queue.pop()
        queue.append(i)
    return dp
```

**Evidence**

二、动态规划：单调队列优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.11%20-%20DP%20%E4%BC%98%E5%8C%96%EF%BC%9A%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97%E4%B8%8E%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84)
