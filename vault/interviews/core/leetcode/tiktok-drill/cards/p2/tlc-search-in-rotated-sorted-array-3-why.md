---
id: tlc-search-in-rotated-sorted-array-3-why
node: p2.search-in-rotated-sorted-array
type: qa
step: 3
---
## Q
**LC 33 搜索旋转排序数组**｜正确性

为什么取中点后总有一半是有序的？判断"左半有序"的条件为什么必须带等号 `nums[lo] <= nums[mid]`？给一个去掉等号就出错的输入。

## A
**不变量。** 若 `target` 在数组里，它一定在当前区间 `[lo, hi]` 内。每轮根据哪半有序、`target` 是否在有序那半的值域里来缩小区间，始终保持这个性质。

**为什么总有一半有序。** 旋转后的数组是两段升序的拼接，中间只有一个"下降点"（最大值之后紧接着最小值）。中点 `mid` 把区间分成 `[lo, mid]` 和 `[mid, hi]`，下降点至多落在其中一半里，另一半就是纯升序。`nums[lo] <= nums[mid]` 说明从 `lo` 到 `mid` 没有下降，左半有序；否则下降点在左半，右半一定有序。

**为什么要带等号。** 当区间只剩两个元素时 `lo == mid`，此时 `nums[lo] == nums[mid]`，左半 `[lo, mid]` 只有一个元素，当然是有序的。去掉等号就会把它误判成"右半有序"。

**反例：`nums[lo] < nums[mid]`。** 输入 `nums = [3,1]`，`target = 1`，正确答案 `1`。`lo = 0`，`hi = 1`，`mid = 0`，`nums[0] = 3 != 1`。去掉等号后 `3 < 3` 为假，走到右半有序的分支，判断 `nums[mid] < target <= nums[hi]`，即 `3 < 1` 为假，于是 `hi = mid - 1 = -1`，循环结束，返回 `-1`。带等号时判定左半（单个元素）有序，`3 <= 1 < 3` 不成立，转去右半：`lo = 1`，下一轮 `mid = 1` 命中，返回 `1`。

**为什么 `target` 的范围一端开一端闭。** `nums[mid]` 已经与 `target` 比较过且不相等，所以左半检查用 `nums[lo] <= target < nums[mid]`，右半检查用 `nums[mid] < target <= nums[hi]`。
