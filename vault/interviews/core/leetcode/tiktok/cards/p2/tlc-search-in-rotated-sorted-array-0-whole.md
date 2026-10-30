---
id: tlc-search-in-rotated-sorted-array-0-whole
node: p2.search-in-rotated-sorted-array
type: qa
---
## Q
**LC 33 搜索旋转排序数组**｜Medium · LC TikTok 热度 75/100（近 6 个月） · 近一年被问：美国 3 次、国内 4 次 · CodeTop 国内累计 162 次 · 最近 2026-10-15（国内 CodeTop）

整数数组 `nums` 原本按升序排列且值**互不相同**，在某个未知的下标 `k`（`0 <= k < nums.length`）处向左旋转，变成 `[nums[k], nums[k+1], ..., nums[n-1], nums[0], ..., nums[k-1]]`。给旋转后的 `nums` 和目标值 `target`，返回 `target` 的下标，不存在返回 `-1`，要求 `O(log n)`。`1 <= nums.length <= 5000`，`-10^4 <= nums[i] <= 10^4`，`nums` 中每个值都独一无二，`-10^4 <= target <= 10^4`。例：`[4,5,6,7,0,1,2]`，`target = 0` → `4`；同一个数组 `target = 3` → `-1`；`[1]`，`target = 0` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分查找，关键观察是：把旋转数组从中点劈成两半，**至少有一半是有序的**；判断哪一半有序（`nums[lo] <= nums[mid]` 说明左半有序），再看 `target` 是否落在这一半的值域里，在就去这一半，不在就去另一半。`O(log n)`。

**识别。** 「有序数组（旋转过）」+「要求 `O(log n)`」就是二分。旋转破坏了整体有序，但保留了局部有序；`n <= 5000`，线性扫描能过但不符合题目要求。

**推导。** 暴力：线性扫描 `O(n)`。另一种两步法：先二分找旋转点（最小值的位置），再在某一段上普通二分，两次 `O(log n)`。一步法的洞察：每次取中点后，`[lo, mid]` 和 `[mid, hi]` 中必有一个是普通的升序区间（旋转点只可能在其中一个里）。若左半有序，`target` 在 `[nums[lo], nums[mid])` 内就在左半，否则在右半；若右半有序同理。每次排除一半，对数次结束。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:                  # 左半 [lo, mid] 是有序的
            if nums[lo] <= target < nums[mid]:     # target 落在有序的左半里：去左边
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                      # 否则右半 [mid, hi] 一定有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

运行：`[4,5,6,7,0,1,2], 0` → `4`；`[4,5,6,7,0,1,2], 3` → `-1`；`[1], 0` → `-1`；`[1], 1` → `0`；`[3,1], 1` → `1`；`[5,1,3], 5` → `0`。

**复杂度。** 时间 `O(log n)`；空间 `O(1)`。

**易错点。**
- 判断左半有序必须用 `nums[lo] <= nums[mid]`（带等号）。写成 `<`，遇到 `lo == mid`（区间只剩两个元素）会误判：`[3,1], target = 1` 得到 `-1`，正确是 `1`。
- 区间端点的比较要一端闭一端开：左半是 `nums[lo] <= target < nums[mid]`，因为 `mid` 已经检查过不等于 `target`。
- 数组没有旋转（旋转点在 0）时，左半总是有序，逻辑仍然正确，不用特判。

**追问。**
- 有重复元素（LC 81）：当 `nums[lo] == nums[mid] == nums[hi]` 时无法判断哪半有序，只能两端各缩一格，最坏 `O(n)`。
- 找旋转后数组的最小值（LC 153）：`nums[mid] > nums[hi]` 就往右，否则往左。
- 用 `bisect` 的 `key` 参数把二分写成两行：先找旋转点，再在"虚拟有序数组"上二分。

**同模式。** LC 81 搜索旋转排序数组 II、LC 153 寻找旋转排序数组中的最小值、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 162 寻找峰值、LC 74 搜索二维矩阵。
