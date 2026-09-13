---
id: leetcode-c-endlesscheng-luu0kb-dp-optimizations-monotonic-queue-fenwick-recognition
node: dp-linear-knapsack.dp-optimizations-monotonic-queue-fenwick
type: cloze
anki: 1787272458779
tags: [concept-cloze, leetcode, recall, recognition]
---
dp[i] 只依赖一个滑动区间内 dp 的最值时，用 {{c1::单调队列优化 DP}}。

转移是滑动范围最值时维护单调队列；转移依赖按值域前缀的最优值时，离散化后用树状数组查询和更新。

**Evidence**

二、动态规划：单调队列优化 DP、树状数组优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F88.11%20-%20DP%20%E4%BC%98%E5%8C%96%EF%BC%9A%E5%8D%95%E8%B0%83%E9%98%9F%E5%88%97%E4%B8%8E%E6%A0%91%E7%8A%B6%E6%95%B0%E7%BB%84)
