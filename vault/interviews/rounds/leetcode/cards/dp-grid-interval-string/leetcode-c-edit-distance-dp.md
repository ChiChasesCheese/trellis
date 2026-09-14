---
id: leetcode-c-edit-distance-dp
node: dp-grid-interval-string.edit-distance-dp
type: cloze
anki: 1787102263959
tags: [concept-cloze, leetcode, recall]
---
在编辑距离DP中，当 s[i-1] == t[j-1] 时，dp[i][j] = {{c1::dp[i-1][j-1]}}（不需要任何操作）；当字符不匹配时，dp[i][j] = {{c2::1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])}}（插入/删除/替换三选一）。

边界条件：dp[i][0] = i，dp[0][j] = j。LCS问题是编辑距离的特例（只允许跳过字符，不允许替换）。

**Evidence**

if s[i-1] == t[j-1]: dp[i][j] = dp[i-1][j-1] else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%BC%96%E8%BE%91%E8%B7%9D%E7%A6%BB%20DP)
