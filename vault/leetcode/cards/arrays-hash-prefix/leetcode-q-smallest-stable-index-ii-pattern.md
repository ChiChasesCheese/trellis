---
id: leetcode-q-smallest-stable-index-ii-pattern
node: arrays-hash-prefix.prefix-sum
type: qa
anki: 1788743830036
tags: [lc::3904, leetcode, pattern, recall]
---
## Q
如何用 O(n) 求出最小的稳定下标 i，使得 max(nums[0..i]) - min(nums[i..n-1]) <= k？

## A
前后缀分解：先从右往左预处理后缀最小值数组 sufMin（sufMin[i] = min(nums[i:])）；再从左往右扫描，维护前缀最大值 preMax，一旦 preMax - sufMin[i] <= k 就返回当前下标 i，否则返回 -1。核心思路是把 O(n^2) 的暴力（每个 i 都重新算 max 和 min）拆成前缀 max 与后缀 min 两个独立方向的信息，各自 O(n) 预处理，合并只需 O(1)。

**Evidence**

暴力解 firstStableIndex0 对每个 i 都调用 max(nums[:i+1]) 和 min(nums[i:])，是 O(n^2)；优化解 firstStableIndex 先倒序算出 sufMin 数组，再正序维护 preMax，整体 O(n)。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3904%20-%20Smallest%20Stable%20Index%20II)
