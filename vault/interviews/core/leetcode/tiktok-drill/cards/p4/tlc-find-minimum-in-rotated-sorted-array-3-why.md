---
id: tlc-find-minimum-in-rotated-sorted-array-3-why
node: p4.find-minimum-in-rotated-sorted-array
type: qa
step: 3
---
## Q
**LC 153 寻找旋转排序数组中的最小值**｜正确性

为什么要拿 `nums[mid]` 和右端点 `nums[hi]` 比，而不是左端点 `nums[lo]`？为什么更新是 `hi = mid` 而不是 `hi = mid - 1`？各给出一个错误输入。

## A
**不变量。** 每轮开始，最小值一定在 `[lo, hi]` 内。

**为什么和 `nums[hi]` 比。** 最小值是整个数组「唯一的断崖」右侧的第一个元素。`nums[mid] > nums[hi]` 意味着 `mid` 到 `hi` 之间发生了下降，断崖在 `(mid, hi]`，最小值也在那里。`nums[mid] < nums[hi]`（元素不同，不会相等，因为 `mid < hi`）意味着 `mid..hi` 是一段递增，断崖不在其中，最小值在 `[lo, mid]`。这个判断对「完全没旋转」也成立：整个数组递增，永远走 `hi = mid`，收缩到 `lo`，返回首元素。

**反例一：和 `nums[lo]` 比。** 判据写成「`nums[mid] >= nums[lo]` 就右移」。没旋转的 `[11,13,15,17]`：`mid` 总是 `>= nums[lo]`，`lo` 一路右移，返回 `17`；正确是 `11`。

**为什么是 `hi = mid`。** `nums[mid] < nums[hi]` 时 `mid` 自己可能就是最小值（它可能恰好在断崖右侧第一个位置）。丢掉它就找不回来了。

**反例二：`hi = mid - 1`（配 `lo <= hi`）。** `[4,5,1,2,3]`：`mid = 2` 时 `nums[2] = 1 < nums[4] = 3`，`hi` 变成 `1`，最小值 `1` 被排除；后续只在 `4, 5` 里找，返回 `4`；正确是 `1`。
