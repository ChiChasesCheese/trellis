---
id: leetcode-q-build-array-from-permutation-pattern
node: design-simulation.simulation
type: qa
anki: 1787102261681
tags: [lc::1920, leetcode, pattern, recall]
---
## Q
给定 0-based 排列 nums，要求 O(1) 额外空间构造 ans[i] = nums[nums[i]]，思路是什么？

## A
利用约束 0 <= nums[i] < n，把新旧值编码进同一个整数里：遍历时令 nums[i] += (nums[nums[i]] % n) * n（此时右侧的 nums[nums[i]] 还未被覆盖，取模拿到原值），第二轮遍历再对每个元素做 nums[i] //= n 取出高位存的新值。本质是用 value = old + new*n 这种双基编码在同一数组内原地保存新旧两份信息，第一轮读的都是低位（原值），第二轮统一转成高位（新值）。

**Evidence**

nums[i] += (nums[nums[i]] % 1000) * 1000 后再 nums[i] //= 1000，其中 1000 取自约束 nums.length <= 1000 的上界

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1920%20-%20Build%20Array%20from%20Permutation)
