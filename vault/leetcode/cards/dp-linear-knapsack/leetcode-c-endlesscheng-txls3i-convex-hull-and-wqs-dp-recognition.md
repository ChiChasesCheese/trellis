---
id: leetcode-c-endlesscheng-txls3i-convex-hull-and-wqs-dp-recognition
node: dp-linear-knapsack.convex-hull-and-wqs-dp
type: cloze
anki: 1787272416405
tags: [concept-cloze, leetcode, recall, recognition]
---
DP 转移能写成 min(m*x+b) 时，考虑 {{c1::Convex Hull Trick}}。

CHT 将形如 min(m_j*x+b_j) 的转移维护为直线下包络；WQS 用每选一次的罚分把“恰好/至多 k 次”约束转为无约束 DP，再二分罚分。

**Evidence**

§11.7 斜率优化 DP

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F07.17%20-%20CHT%20%E4%B8%8E%20WQS%20%E4%BA%8C%E5%88%86%E4%BC%98%E5%8C%96)
