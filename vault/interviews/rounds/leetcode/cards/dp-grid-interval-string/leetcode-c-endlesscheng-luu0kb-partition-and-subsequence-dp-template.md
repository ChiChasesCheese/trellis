---
id: leetcode-c-endlesscheng-luu0kb-partition-and-subsequence-dp-template
node: dp-grid-interval-string.partition-and-subsequence-dp
type: cloze
anki: 1787272458079
tags: [concept-cloze, leetcode, recall, template]
---
划分型 DP 的基本转移是枚举 start，并用 dp[start] 更新 {{c1::dp[end]}}。

```
def min_partitions(text, valid):
    n = len(text)
    inf = n + 1
    dp = [inf] * (n + 1)
    dp[0] = 0
    for end in range(1, n + 1):
        for start in range(end):
            if valid(text[start:end]):
                dp[end] = min(dp[end], dp[start] + 1)
    return -1 if dp[n] == inf else dp[n]
```

**Evidence**

二、动态规划：划分型 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.08%20-%20%E5%88%92%E5%88%86%E5%9E%8B%E4%B8%8E%E5%AD%90%E5%BA%8F%E5%88%97%20DP)
