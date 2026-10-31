---
id: tlc-find-first-and-last-position-of-element-in-sorted-array-3-why
node: p2.find-first-and-last-position-of-element-in-sorted-array
type: qa
step: 3
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜正确性

手写下界二分 `lower_bound(nums, x)` 时，为什么要用左闭右开区间 `[lo, hi)`、更新写成 `lo = mid + 1` 和 `hi = mid`？区间写成 `hi = len(nums) - 1` 会在哪里出错？

## A
**手写的下界函数。**
```python
def lower_bound(nums: list[int], x: int) -> int:
    lo, hi = 0, len(nums)                   # 搜索区间 [lo, hi)，答案可能是 len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < x:
            lo = mid + 1                    # mid 一定不是答案
        else:
            hi = mid                        # mid 可能是答案，保留
    return lo
```
**不变量。** 下标 `< lo` 的元素都 `< x`；下标 `>= hi` 的元素都 `>= x`。初始 `lo = 0`、`hi = len(nums)` 时两条空成立。每轮 `mid` 落在 `[lo, hi)` 内：`nums[mid] < x` 说明 `mid` 及其左边都 `< x`，`lo` 推到 `mid + 1`；否则 `mid` 及其右边都 `>= x`，`hi` 收到 `mid`（保留 `mid`，它可能就是第一个）。区间长度严格变小，循环必然结束于 `lo == hi`，此时恰好是“第一个 `>= x` 的位置”。

**为什么是左闭右开。** 答案可能是 `len(nums)`（所有元素都 `< x`），它不是合法下标，只有开区间的右端 `hi = len(nums)` 才能表示它。

**反例：`hi = len(nums) - 1`。** 区间写成闭区间 `[0, len-1]` 且仍用 `while lo < hi`：
- `nums = [1,3]`，`target = 3`：下界得 `1`，求“第一个 `>= 4`”时本应返回 `2`，却只能返回 `1`，最后下标 `1 - 1 = 0`，结果 `[1, 0]`；正确是 `[1, 1]`。
- `nums = [5,7,7,8,8,10]`，`target = 10`：同样得到 `[5, 4]`，正确是 `[5, 5]`。

“目标是数组里最大值”的输入恰好触发这个边界，所以用例要包含目标在末尾的情形。
