---
id: leetcode-c-endlesscheng-txls3i-interval-dp-template
node: dp-grid-interval-string.interval-dp
type: cloze
anki: 1787272414806
tags: [concept-cloze, leetcode, recall, template]
---
最长回文子序列相等两端的转移是 {{c1::2 + dp[l+1][r-1]}}。

```
def solve(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for left in range(n - 1, -1, -1):
        dp[left][left] = 1
        for right in range(left + 1, n):
            if s[left] == s[right]:
                dp[left][right] = 2 + dp[left + 1][right - 1]
            else:
                dp[left][right] = max(dp[left + 1][right], dp[left][right - 1])
    return dp[0][n - 1] if n else 0
```

**Evidence**

§8.1 最长回文子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.11%20-%20%E5%8C%BA%E9%97%B4%20DP%20%E4%B8%8E%E5%8F%AF%E6%B6%88%E9%99%A4%E5%8C%BA%E9%97%B4)
