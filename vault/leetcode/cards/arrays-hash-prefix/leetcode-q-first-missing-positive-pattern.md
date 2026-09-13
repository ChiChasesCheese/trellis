---
id: leetcode-q-first-missing-positive-pattern
node: arrays-hash-prefix.hash-table
type: qa
anki: 1787102262932
tags: [lc::41, leetcode, pattern, recall]
---
## Q
如何在 O(n) 时间、O(1) 空间内求数组中缺失的最小正整数（First Missing Positive）？

## A
利用『原地下标哈希』（cyclic sort）：数组长度为 n，答案必然落在 [1, n+1] 内。遍历数组，把每个值为 v（1≤v≤n）的元素通过交换放到下标 v-1 的位置，直到 nums[i]==i+1 或无法再交换（值超界或已就位）。交换后再扫描一遍，第一个 nums[i] != i+1 的位置即为答案 i+1；若全部就位则答案是 n+1。核心不变量：交换循环用 while 而非 for，因为每次交换后 nums[i] 会变化，需要重新判断同一位置。

**Evidence**

代码：`while i < n: correctIdx = nums[i] - 1; if 0 < nums[i] <= n and nums[i] != nums[correctIdx]: nums[i], nums[correctIdx] = nums[correctIdx], nums[i] else: i += 1` 随后 `return next((i + 1 for i in range(n) if nums[i] != i + 1), n + 1)`，Runtime 59ms 提交通过。

[原文 ↗](obsidian://open?vault=lc&amp;file=questions%2F41%20-%20First%20Missing%20Positive)
