---
id: leetcode-q-find-k-closest-elements-pattern
node: advanced-ds-heap.heap-priority-queue
type: qa
anki: 1787102263158
tags: [lc::658, leetcode, pattern, recall]
---
## Q
在有序数组中用二分查找找到与 x 最接近的 k 个连续元素的起始位置，核心比较条件是什么？

## A
在区间 [0, n-k] 上二分查找窗口左端点 lo。判断窗口 [mid, mid+k) 是否应该右移：若 x - arr[mid] > arr[mid+k] - x，说明左边界元素比右边界候选元素离 x 更远，应舍弃左边（lo = mid + 1）；否则 hi = mid。收敛后答案即为 arr[lo: lo+k]。这是「在答案位置上二分」的经典模式：不是直接比较元素值和 x，而是比较窗口左右两端到 x 的距离，用单调性质缩小候选窗口起点范围，时间复杂度 O(log(n-k))，优于排序法 O(n log n) 和双指针扩展法 O(n)。

**Evidence**

findClosestElements 方法：`lo, hi = 0, len(arr) - k` 二分，`if x - arr[mid] > arr[mid + k] - x: lo = mid + 1 else: hi = mid`，最终 `return arr[lo: lo + k]`

[原文 ↗](obsidian://open?vault=lc&file=questions%2F658%20-%20Find%20K%20Closest%20Elements)
