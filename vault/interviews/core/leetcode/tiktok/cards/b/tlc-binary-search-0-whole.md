---
id: tlc-binary-search-0-whole
node: b.binary-search
type: qa
---
## Q
**LC 704 二分查找**｜Easy · 近一年被问：美国 0 次、国内 1 次 · CodeTop 国内累计 26 次 · 最近 2026-09（面试记录）

给升序整型数组 `nums`（元素互不相同）和目标值 `target`，若 `target` 在 `nums` 中返回下标，否则返回 `-1`，要求 `O(log n)` 时间。`1 <= n <= 10^4`，`-9999 <= nums[i] <= 9999`。例：`nums = [-1,0,3,5,9,12]`、`target = 9` → `4`；`target = 2` → `-1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用「左闭右开」区间 `[lo, hi)` 找第一个 `>= target` 的位置：中点太小就 `lo = mid + 1`，否则 `hi = mid`；区间收缩为空时 `lo` 就是候选位置，最后检查它是否真的等于 `target`。`O(log n)`。

**识别。** 「有序数组 + 查找」→ 二分；要求 `O(log n)` 时间是直接信号。每次比较能排除一半候选，因为数组的单调性让"中点太小则左边全都太小"成立。

**推导。** 暴力：线性扫描 `O(n)` → 浪费：数组有序，中点 `nums[mid]` 一次比较就能排除一整半 → 每步区间缩小一半，`log2(10^4) ≈ 14` 步 → 容易出错的是区间的开闭和边界更新：统一使用「搜索区间 `[lo, hi)`」、「循环条件 `lo < hi`」、「`lo = mid + 1` 或 `hi = mid`」这一套，每一步区间严格缩小，不会死循环，退出时 `lo == hi`，正是"第一个 `>= target` 的位置"，等同于 `bisect_left`。

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                  # 搜索区间 [lo, hi)，左闭右开
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1                   # mid 太小，排除 [lo, mid]
        else:
            hi = mid                       # mid 可能就是答案，保留 [lo, mid)
    return lo if lo < len(nums) and nums[lo] == target else -1
```

运行：`([-1,0,3,5,9,12], 9)` → `4`，`([-1,0,3,5,9,12], 2)` → `-1`，`([5], 5)` → `0`，`([5], 2)` → `-1`，`([5], 9)` → `-1`；`[-9999, ..., 0]` 中查 `0` → `9999`，查 `1` → `-1`。

**复杂度。** 时间 `O(log n)`；空间 `O(1)`。

**易错点。**
- 闭区间 `[lo, hi]` 配 `while lo <= hi` 却写 `hi = mid`：区间不收缩，死循环。`nums = [5]`、`target = 2` 永远不返回。
- 左闭右开却写 `lo = mid`（没加一）：`nums = [1,2]`、`target = 2` 时 `lo` 停在 `0`，死循环。
- 退出后必须检查 `lo < len(nums)`：`target` 比所有元素都大时 `lo == len(nums)`，直接 `nums[lo]` 会 `IndexError`。

**追问。**
- 有重复元素，找第一个 / 最后一个位置：第一个就是 `bisect_left`；最后一个是 `bisect_right(nums, target) - 1`。
- 插入位置（LC 35）：返回 `lo` 本身，不用最后的检查。
- 答案空间上的二分（如 LC 69 平方根、LC 875 爱吃香蕉的珂珂）：把"有序数组"换成"单调的判定函数"，同一个模板。

**同模式。** LC 35 搜索插入位置、LC 34 在排序数组中查找元素的第一个和最后一个位置、LC 33 搜索旋转排序数组、LC 74 搜索二维矩阵。
