---
id: leetcode-q-partition-equal-subset-sum-pattern
node: dp-linear-knapsack.0-1-knapsack
type: qa
anki: 1787354597353
tags: [lc::416, leetcode, pattern, recall]
---
## Q
如何用动态规划判断数组能否划分为两个和相等的子集（0/1背包子集和问题）？

## A
先求总和 total，若为奇数直接返回 false；否则目标为 target = total // 2，转化为「能否从 nums 中选出若干数使其和恰好等于 target」的 0/1 背包可行性问题。用一维布尔数组 dp[0..target]，dp[0] = True，对每个 num 从 target 倒序遍历到 num，做 dp[c] |= dp[c - num]，倒序遍历保证每个数只被用一次（0/1背包特征）。最终返回 dp[target]。时间复杂度 O(n * target)，空间 O(target)。

**Evidence**

canPartition 方法：total = sum(nums); target = total // 2; dp = [False] * (target + 1); dp[0] = True; for num in nums: for c in range(target, num - 1, -1): dp[c] |= dp[c - num]; return dp[target]

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F416%20-%20Partition%20Equal%20Subset%20Sum)
