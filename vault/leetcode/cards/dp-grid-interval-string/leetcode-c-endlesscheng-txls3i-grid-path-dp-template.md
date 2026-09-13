---
id: leetcode-c-endlesscheng-txls3i-grid-path-dp-template
node: dp-grid-interval-string.grid-path-dp
type: cloze
anki: 1787272412704
tags: [concept-cloze, leetcode, recall, template]
---
最小路径和不可达状态应初始化为 {{c1::float('inf')}}。

```
def solve(grid):
    m, n = len(grid), len(grid[0])
    dp = [[float('inf')] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for r in range(m):
        for c in range(n):
            if r:
                dp[r][c] = min(dp[r][c], dp[r - 1][c] + grid[r][c])
            if c:
                dp[r][c] = min(dp[r][c], dp[r][c - 1] + grid[r][c])
    return dp[-1][-1]
```

**Evidence**

二、网格图 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.04%20-%20%E7%BD%91%E6%A0%BC%E8%B7%AF%E5%BE%84%20DP)
