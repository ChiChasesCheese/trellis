---
id: leetcode-q-find-the-largest-almost-missing-integer-pattern
node: arrays-hash-prefix.hash-table
type: qa
anki: 1787102262507
tags: [lc::3471, leetcode, pattern, recall]
---
## Q
给定长度为 n 的数组和窗口大小 k，找“恰好出现在一个长度为 k 的子数组中”的最大整数，如何避免暴力枚举所有子数组？

## A
利用组合计数：一个值 x 出现在多少个长度为 k 的窗口中，只取决于它在数组中的下标位置，而与具体数值无关。除了首尾边界，数组中间的下标必然会被多个窗口覆盖（当 k>=2 时），所以候选“恰好出现一次”的整数只可能是 nums[0] 或 nums[-1]（如果它们在整个数组中只出现一次）。因此只需特判：k==n 时直接返回最大值；k==1 时用计数数组找出现次数为1的最大值；k>=2 时只检查 nums[0] 和 nums[-1] 的全局出现次数是否为1，取较大者。因为 n<=50，用长度51的计数数组代替哈希表更快。

**Evidence**

largestInteger 解法：k==n 时 return max(nums)；k==1 时遍历计数数组找最大的count==1的值；k>=2 时只检查 count[nums[0]]==1 和 count[nums[-1]]==1，只有首尾元素才可能是唯一候选。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3471%20-%20Find%20the%20Largest%20Almost%20Missing%20Integer)
