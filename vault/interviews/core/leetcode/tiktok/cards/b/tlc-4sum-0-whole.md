---
id: tlc-4sum-0-whole
node: b.4sum
type: qa
---
## Q
**LC 18 四数之和**｜Medium · CodeTop 国内累计 14 次 · 最近 2026-06-17（国内 CodeTop）

给由 `n` 个整数组成的数组 `nums` 和目标值 `target`，返回所有和为 `target` 且**不重复**的四元组 `[nums[a], nums[b], nums[c], nums[d]]`，要求 `a`、`b`、`c`、`d` 互不相同；两个四元组元素一一对应就算重复；答案顺序不限。`1 <= nums.length <= 200`，`-10^9 <= nums[i] <= 10^9`，`-10^9 <= target <= 10^9`。例：`nums = [1,0,-1,0,-2,2], target = 0` → `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`；`nums = [2,2,2,2,2], target = 8` → `[[2,2,2,2]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先排序，用两层循环固定前两个数（各自跳过重复值），剩下两个数在有序数组上用对撞双指针找；k 数之和的通用做法就是「固定 k-2 个数 + 双指针」。`O(n^3)`。

**识别。** 「找 k 个数使和为目标」+「结果不能重复」是排序加双指针的信号（与三数之和同源）。`n <= 200` 正好为 `O(n^3)`（约 `8 * 10^6`）设计，`O(n^4)`（`1.6 * 10^9`）不行；值域到 `10^9`，不能开计数数组。

**推导。** 暴力：四层循环加集合去重，`O(n^4)`。排序之后固定 `a`、`b`，问题变成「在剩下的有序数组里找两个数，和为 `target - a - b`」，对撞双指针一趟 `O(n)`：和小了左指针右移，和大了右指针左移。总共 `O(n^2) * O(n) = O(n^3)`。去重靠排序：相同的值相邻，第一、第二个数遇到与前一个相同的就跳过，找到解后左指针跳过相同值（右指针随之唯一确定）。剪枝：有序数组里，当前 `nums[i]` 与紧随其后三个数的和已大于 `target` 就整体 `break`；与最大三个数的和仍小于 `target` 就 `continue`，第二层同理。

```python
def four_sum(nums: list[int], target: int) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:           # 第一个数去重
            continue
        if sum(nums[i:i + 4]) > target:                # 最小的四数之和已超过：之后只会更大
            break
        if nums[i] + sum(nums[-3:]) < target:          # 与最大的三个数相加仍不够：换更大的 i
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:   # 第二个数去重：注意是 j > i + 1
                continue
            if nums[i] + sum(nums[j:j + 3]) > target:
                break
            if nums[i] + nums[j] + sum(nums[-2:]) < target:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[j] + nums[lo] + nums[hi]
                if total < target:
                    lo += 1
                elif total > target:
                    hi -= 1
                else:
                    result.append([nums[i], nums[j], nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:   # 跳过重复的第三个数
                        lo += 1
    return result
```

运行：`[1,0,-1,0,-2,2], 0` → `[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]`，`[2,2,2,2,2], 8` → `[[2,2,2,2]]`，`[0,0,0,0], 0` → `[[0,0,0,0]]`，`[1,2,3], 6` → `[]`，`[10^9,10^9,-10^9,-10^9], 0` → `[[-1000000000,-1000000000,1000000000,1000000000]]`。

**复杂度。** 时间 `O(n^3)`：排序 `O(n log n)`，两层循环 `O(n^2)` 次、内层双指针 `O(n)`，`n = 200` 约 `8 * 10^6` 步；空间 `O(1)` 额外（不计排序副本和结果）。

**易错点。**
- 第二层去重条件是 `j > i + 1`，不是 `j > 0`。写成 `j > 0`，`[2,2,2,2,2]`、`8` 会把所有 `j` 都跳过，得到 `[]`（正确 `[[2,2,2,2]]`）。
- 找到解后左右指针都要移动，并跳过左边的重复值；只动一个会重复输出或死循环。
- 剪枝的方向：最小四数和 `> target` 才能 `break`；最大那组仍 `< target` 只能 `continue`（更大的 `i` 可能够），写成 `break` 会漏解。

**追问。**
- 通用 k 数之和：递归固定 `k - 2` 个数，`k == 2` 时双指针，`O(n^(k-1))`。
- 只数个数、不要求去重（LC 454 四数相加 II）：四个数组分成两半，哈希表存两两之和，`O(n^2)`。
- 输入有 `10^9` 级别的数：Python 整数不会溢出，Java/C++ 要用 `long` 累加。

**同模式。** LC 1 两数之和、LC 15 三数之和、LC 16 最接近的三数之和、LC 454 四数相加 II、LC 167 两数之和 II。
