---
id: leetcode-c-endlesscheng-txls3i-lcs-alignment-dp-invariant
node: dp-grid-interval-string.lcs-alignment-dp
type: cloze
anki: 1787272413204
tags: [concept-cloze, invariant, leetcode, recall]
---
LCS 中末字符相等时转移到 {{c1::dp[i-1][j-1]}}。

dp[i][j] 只表示 s[:i] 与 t[:j] 的答案；相等字符使用 dp[i-1][j-1]，不等时不能强行匹配

**Evidence**

§4.1 最长公共子序列

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.06%20-%20LCS%20%E5%AF%B9%E9%BD%90%20DP)
