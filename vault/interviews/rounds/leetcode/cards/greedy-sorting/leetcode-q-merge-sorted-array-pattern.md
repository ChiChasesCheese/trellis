---
id: leetcode-q-merge-sorted-array-pattern
node: greedy-sorting.sorting
type: qa
anki: 1787613695038
tags: [lc::88, leetcode, pattern, recall]
---
## Q
合并两个有序数组到 nums1（原地，O(m+n)）时，为什么要从后往前双指针，而不是从前往后？

## A
从前往后写会覆盖 nums1 中还未读取的元素（因为 nums1 前 m 位是有效数据，后面才是空位）。从后往前写：i=m-1, j=n-1 分别指向两数组末尾有效元素，写入位置从 nums1 末尾 (i+j+1) 开始递减，这样永远只覆盖已经处理过或空闲的位置，不会破坏未读数据。循环结束后若 nums2 还有剩余（j>=0），说明这些元素都比 nums1 剩余部分小，直接复制到 nums1 开头 nums1[:j+1] = nums2[:j+1]；若 nums1 有剩余（i>=0）则天然已在正确位置，无需处理。

**Evidence**

merge/merge0 解法：`i, j = m - 1, n - 1` 从末尾双指针，`nums1[i + j + 1] = ...` 写入尾部；循环后 `if j >= 0: nums1[:j+1] = nums2[:j+1]` 处理 nums2 剩余，`if i1 >= 0: pass` 说明 nums1 剩余无需处理。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F88%20-%20Merge%20Sorted%20Array)
