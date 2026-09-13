---
id: leetcode-q-smallest-stable-index-i-pattern
node: arrays-hash-prefix.prefix-sum
type: qa
anki: 1788564025722
tags: [lc::3903, leetcode, pattern, recall]
---
## Q
给定数组，需要对每个下标 i 同时知道「前缀最值」和「后缀最值」，如何在 O(n) 内完成？

## A
预处理后缀最小值数组 sufMin（从右往左递推：sufMin[i] = min(nums[i], sufMin[i+1])），然后从左往右遍历同时维护滚动的前缀最大值 preMax，在每个 i 处直接用 preMax - sufMin[i] 判断条件，避免对每个 i 重复调用 max()/min() 造成 O(n²)。

**Evidence**

firstStableIndex 中先构建 sufMin 数组，再单次遍历维护 preMax，对比暴力版 firstStableIndex0 每次调用 max(nums[:i+1]) 和 min(nums[i:]) 是 O(n²)。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3903%20-%20Smallest%20Stable%20Index%20I)
