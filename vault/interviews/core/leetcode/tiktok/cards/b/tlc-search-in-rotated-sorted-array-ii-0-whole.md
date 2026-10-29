---
id: tlc-search-in-rotated-sorted-array-ii-0-whole
node: b.search-in-rotated-sorted-array-ii
type: qa
---
## Q
**LC 81 搜索旋转排序数组 II**｜Medium · CodeTop 国内累计 3 次 · 最近 2026-04-16（CodeTop）

有一个按**非降序**排列的整数数组 `nums`，值**可能重复**。它在某个未知的下标 `k`（`0 <= k < nums.length`）上被旋转，变成 `[nums[k], ..., nums[n-1], nums[0], ..., nums[k-1]]`，例如 `[0,1,2,4,4,4,5,6,6,7]` 在下标 `5` 旋转后可能是 `[4,5,6,6,7,0,1,2,4,4]`。给旋转后的 `nums` 和整数 `target`，判断 `target` 是否在数组中，返回 `true` 或 `false`，操作步骤尽量少。`1 <= nums.length <= 5000`，`-10^4 <= nums[i] <= 10^4`，`-10^4 <= target <= 10^4`。例：`nums = [2,5,6,0,0,1,2], target = 0` → `true`；`target = 3` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分查找：每轮判断 `[lo, mid]` 和 `[mid, hi]` 哪一半有序，看 `target` 是否落在有序那一半的值域里，来决定丢掉哪一半；重复值导致 `nums[lo] == nums[mid] == nums[hi]` 时看不出哪半有序，就把两端各缩一格。无重复或重复少时 `O(log n)`，最坏 `O(n)`。

**识别。** 「已排序、被旋转、查找」是二分的标志，旋转只是让「整体有序」变成「局部有序」。「值可能重复」是这道变种的关键：它会让二分在某些输入上无法判断方向，复杂度退化。

**推导。** 暴力：`target in nums`，`O(n)`，对 `n <= 5000` 能过，但没有用上有序性。浪费：旋转数组从任意位置切开，**至少有一半是有序的**（断点只有一个），这个事实没被利用。洞察：比较 `nums[lo]` 与 `nums[mid]` 判断左半是否有序；有序的半边用端点值就能判断 `target` 在不在里面，不在就整体丢掉。重复破坏了这个判断：`nums[lo] == nums[mid] == nums[hi]` 时，断点可能在左边也可能在右边（`[1,1,1,0,1]` 与 `[1,0,1,1,1]` 的三个端点都是 `1`）。此时 `mid` 已经不是 `target`，同值的 `lo` 和 `hi` 也不是，各缩一格不会丢答案。

```python
def search(nums: list[int], target: int) -> bool:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:      # 看不出哪半边有序：两端各缩一格（mid 不是 target）
            lo, hi = lo + 1, hi - 1
        elif nums[lo] <= nums[mid]:                # 左半 [lo, mid] 有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                      # 右半 [mid, hi] 有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
```

运行：`[2,5,6,0,0,1,2]` 找 `0` → `True`，找 `3` → `False`；`[1,0,1,1,1]` 找 `0` → `True`；`[1]` 找 `1` → `True`，找 `0` → `False`；`[1,1,1,1,1,2,1,1]` 找 `2` → `True`。

**复杂度。** 平均 `O(log n)`；最坏 `O(n)`：`[1] * 2500 + [2] + [1] * 2499` 里找 `3`，循环要走 2501 轮，而同样长度的有序数组只要 13 轮。空间 `O(1)`。

**易错点。**
- 漏掉「三者相等就缩」的分支：`[1,0,1,1,1]` 找 `0`，第一轮 `nums[lo] <= nums[mid]`（`1 <= 1`）被当成左半有序，`0` 不在 `[1, 1)` 里就丢掉左半，返回 `False`（正确 `True`）。
- 判断左半有序要用 `<=`：`[3,1]` 找 `1` 时 `lo == mid`，写成 `<` 会把右半当成有序，返回 `False`（正确 `True`）。
- 有序半边的区间一端闭一端开：`nums[lo] <= target < nums[mid]`，`mid` 已经比较过。

**追问。**
- 进阶问题：重复元素会让最坏情况从 `O(log n)` 退化为 `O(n)`，因为全是相同值时无法判断断点在哪边，只能逐个排除。
- 求最小值（LC 154）：`nums[mid] == nums[hi]` 时 `hi -= 1`，同样最坏 `O(n)`。
- 要最左的下标：先二分找断点，再在两段有序区间里各用 `bisect_left`，取较小的那个。

**同模式。** LC 33 搜索旋转排序数组、LC 153 / 154 寻找旋转排序数组中的最小值、LC 34 在排序数组中查找首尾位置、LC 162 寻找峰值。
