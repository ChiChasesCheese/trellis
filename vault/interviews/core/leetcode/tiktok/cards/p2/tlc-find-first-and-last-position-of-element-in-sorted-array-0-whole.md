---
id: tlc-find-first-and-last-position-of-element-in-sorted-array-0-whole
node: p2.find-first-and-last-position-of-element-in-sorted-array
type: qa
---
## Q
**LC 34 在排序数组中查找元素的第一个和最后一个位置**｜Medium · LC TikTok 近 3 个月热度 62/100（全时段 53） · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 24 次 · 最近 2026-03-30（国内 CodeTop）

给一个按**非递减**顺序排列的整数数组 `nums` 和目标值 `target`，找出 `target` 在数组中的开始位置和结束位置，不存在则返回 `[-1, -1]`。必须设计并实现时间复杂度 `O(log n)` 的算法。`0 <= nums.length <= 10^5`，`-10^9 <= nums[i] <= 10^9`，`-10^9 <= target <= 10^9`。例：`nums = [5,7,7,8,8,10]`，`target = 8` → `[3,4]`；`target = 6` → `[-1,-1]`；`nums = []`，`target = 0` → `[-1,-1]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两次二分：第一次找「第一个 `>= target` 的位置」（下界，lower bound），若越界或该位置的值不是 `target` 就不存在；第二次找「第一个 `> target` 的位置」再减 `1` 就是最后一个。Python 里就是 `bisect_left` 和 `bisect_right`。`O(log n)`。

**识别。** 「有序数组」加「要求 `O(log n)`」就是二分查找。因为有重复元素，要找的是**边界**而不是任意一个等于 `target` 的位置，这是「二分找边界」的标准题：把「找 `target`」改写成「找第一个满足某条件的位置」，条件 `nums[i] >= target` 随下标单调（先假后真）。

**推导。** 暴力：线性扫描 `O(n)`，不满足要求。普通二分找到一个 `target` 后，向左右扩张找边界，在全是 `target` 的数组里退化成 `O(n)`。所以把两个边界各自当成一个“单调条件的分界点”：`lo = 第一个 >= target 的下标`，`hi = 第一个 > target 的下标 - 1`。标准库 `bisect_left` 就是下界，`bisect_right` 就是第一个 `> target` 的位置。

```python
from bisect import bisect_left, bisect_right

def search_range(nums: list[int], target: int) -> list[int]:
    lo = bisect_left(nums, target)          # 第一个 >= target 的位置
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]                     # 越界或该位置不是 target：不存在
    hi = bisect_right(nums, target) - 1     # 第一个 > target 的位置再减 1 = 最后一个 target
    return [lo, hi]
```

运行：`([5,7,7,8,8,10], 8)` → `[3, 4]`，`([5,7,7,8,8,10], 6)` → `[-1, -1]`，`([], 0)` → `[-1, -1]`，`([1], 1)` → `[0, 0]`，`([2,2], 2)` → `[0, 1]`，`([1,3], 4)` → `[-1, -1]`。

**复杂度。** 时间 `O(log n)`：两次二分；空间 `O(1)`。

**拓展优化。**
- 面试官不让用 `bisect` 时手写下界（lower bound）：整数里「第一个 `> target`」就是「第一个 `>= target + 1`」，同一个函数调两次。

```python
def search_range(nums: list[int], target: int) -> list[int]:
    def lower_bound(x: int) -> int:                # 第一个 >= x 的下标；全都 < x 时返回 len(nums)
        lo, hi = 0, len(nums)                      # 左闭右开：答案可能是 len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < x:
                lo = mid + 1                       # mid 太小，答案一定在右边，且不含 mid
            else:
                hi = mid                           # mid 可能就是答案，保留它
        return lo

    lo = lower_bound(target)
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    return [lo, lower_bound(target + 1) - 1]       # 第一个 >= target + 1 的前一个 = 最后一个 target
```

**易错点。**
- 不检查存在性：`[5,7,7,8,8,10]`，`target = 6`，`bisect_left` 得 `1`，`bisect_right - 1` 得 `0`，直接返回 `[1, 0]`，而正确是 `[-1, -1]`。`lo` 位置的值不等于 `target`，或 `lo == len(nums)`，都必须返回 `[-1, -1]`。
- 手写二分时搜索区间用闭区间 `hi = len(nums) - 1`，却写“找第一个 `> target`”：`([1,3], 3)` 得到 `[1, 0]`，`([5,7,7,8,8,10], 10)` 得到 `[5, 4]`（正确 `[1, 1]` 和 `[5, 5]`）。边界答案可能是 `len(nums)`，区间必须是左闭右开 `[0, len(nums))`。
- 空数组：`bisect_left([], x)` 返回 `0`，等于 `len(nums)`，被越界检查拦住。

**追问。**
- 只问 `target` 出现了几次：`bisect_right(nums, target) - bisect_left(nums, target)`，`O(log n)`。
- 插入位置（LC 35）：`bisect_left(nums, target)` 就是答案，保持有序插入。
- 旋转后的有序数组里找（LC 33）：先判断哪半边有序，再决定往哪边走，仍是 `O(log n)`。

**同模式。** LC 35 搜索插入位置、LC 704 二分查找、LC 540 有序数组中的单一元素、LC 162 寻找峰值、LC 153 / 33 旋转排序数组。
