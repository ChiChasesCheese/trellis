---
id: leetcode-c-endlesscheng-txls3i-lcs-alignment-dp-template
node: dp-grid-interval-string.lcs-alignment-dp
type: cloze
anki: 1787272413304
tags: [concept-cloze, leetcode, recall, template]
---
LCS 的二维状态通常是两个 {{c1::前缀}} 的答案。

```
def solve(s, t):
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    for i, a in enumerate(s, 1):
        for j, b in enumerate(t, 1):
            if a == b:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]
```

**Evidence**

§4.1 最长公共子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.06%20-%20LCS%20%E5%AF%B9%E9%BD%90%20DP)
