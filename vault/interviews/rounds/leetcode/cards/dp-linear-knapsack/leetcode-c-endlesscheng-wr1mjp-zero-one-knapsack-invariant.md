---
id: leetcode-c-endlesscheng-wr1mjp-zero-one-knapsack-invariant
node: dp-linear-knapsack.zero-one-knapsack
type: cloze
anki: 1787272472381
tags: [concept-cloze, invariant, leetcode, recall]
---
一维 0/1 背包必须按容量 {{c1::从大到小}} 更新，避免重复选当前物品。

处理完前 i 个物品后，dp[c] 只使用这 i 个物品；一维压缩倒序更新保证当前物品不会被重复选取

**Evidence**

3. 动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F90.10%20-%200-1%20%E8%83%8C%E5%8C%85)
