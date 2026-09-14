---
id: leetcode-c-endlesscheng-g0n5iy-grouped-knapsack-dp-recognition
node: dp-linear-knapsack.grouped-knapsack-dp
type: cloze
anki: 1787272478580
tags: [concept-cloze, leetcode, recall, recognition]
---
物品分组且每组最多选一个方案时，使用 {{c1::分组背包}}。

每组只能选一种方案或选组内前缀时，逐组更新容量 DP；每个新状态必须来自处理当前组之前的旧状态。

**Evidence**

动态规划

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E7%81%B5%E8%8C%B6%E5%B1%B1%E8%89%BE%E5%BA%9C%2F91.10%20-%20%E5%88%86%E7%BB%84%E8%83%8C%E5%8C%85)
