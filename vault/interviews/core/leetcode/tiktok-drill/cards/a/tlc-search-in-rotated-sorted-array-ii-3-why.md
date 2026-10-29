---
id: tlc-search-in-rotated-sorted-array-ii-3-why
node: a.search-in-rotated-sorted-array-ii
type: qa
step: 3
---
## Q
**LC 81 搜索旋转排序数组 II**｜Medium · 字节高频｜正确性

为什么三个端点相等时可以把 `lo` 和 `hi` 各缩一格而不丢答案？没有这个分支会在什么输入上出错？

## A
**不变量。** 若 `target` 在数组里，它一定在当前区间 `[lo, hi]` 内。每一轮的操作都不能把 `target` 排除出区间。

**为什么可以缩。** 走到这个分支时 `nums[mid] != target`（上一行已经判断过）。三个端点值相同，所以 `nums[lo]` 和 `nums[hi]` 也不等于 `target`，丢掉这两个位置不会丢答案。其余的元素依旧留在区间里。

**为什么必须有这个分支。** 三个端点相同时，断点可能在 `mid` 的任一侧，`nums[lo] <= nums[mid]` 会把「左半有序」误判成真。

**反例：`[1,0,1,1,1]` 找 `0`。** 没有这个分支：`lo = 0, hi = 4, mid = 2`，`nums[lo] <= nums[mid]`（`1 <= 1`），认为左半 `[1,0,1]` 有序；`0` 不在 `[1, 1)` 里，丢掉左半，在 `[1,1]` 里找，返回 `False`。正确答案是 `True`（下标 `1`）。有这个分支时，第一轮把区间缩成 `[1, 3]`，下一轮 `mid = 2`，`nums[lo] = 0`，`nums[mid] = 1`，继续二分，找到 `0`。
