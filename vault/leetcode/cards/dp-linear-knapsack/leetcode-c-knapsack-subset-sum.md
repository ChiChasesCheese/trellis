---
id: leetcode-c-knapsack-subset-sum
node: dp-linear-knapsack.knapsack-subset-sum
type: cloze
anki: 1787102186411
tags: [concept-cloze, leetcode, recall]
---
在0/1背包子集和DP中，内层容量循环必须{{c1::逆序遍历（从target到num）}}，这样才能保证每个元素在更新dp数组时{{c2::最多被选一次}}。

若正序遍历，dp[i]在被num更新后可能又被用于更新更大的dp[j]，导致同一个num被重复使用，退化成完全背包（无限选取）而非0/1背包。

**Evidence**

逆序遍历c保证每个元素最多选一次；正序遍历导致一个元素选多次（nums[i]用于更新dp[i]后，又用于更新后续dp）

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F0-1%20%E8%83%8C%E5%8C%85%E4%B8%8E%E5%AD%90%E9%9B%86%E5%92%8C)
