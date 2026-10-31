---
id: tlc-3sum-smaller-0-whole
node: c.3sum-smaller
type: qa
---
## Q
**LC 259 较小的三数之和**｜Medium · LC TikTok 全时段热度 25/100

给定长度为 `n` 的整数数组 `nums` 和目标值 `target`，统计满足 `0 <= i < j < k < n` 且 `nums[i] + nums[j] + nums[k] < target` 的三元组 `(i, j, k)` 的个数。`n == nums.length`，`0 <= n <= 3500`，`-100 <= nums[i] <= 100`，`-100 <= target <= 100`，保证答案不超过 `10^9`。例：`nums = [-2,0,1,3], target = 2` → `2`（`[-2,0,1]`、`[-2,0,3]`）；`nums = [], target = 0` → `0`；`nums = [0], target = 0` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 排序后固定第一个数，用左右双指针在剩余部分里数对：和小于目标时 `right - left` 个右端点全部满足，一次累加。

**识别。** 「三数之和」类题排序 + 双指针；计数小于号的变体可以一次数一批，因为数组有序后单调。

**推导。** 暴力：三重循环 `O(n^3)`，`n = 3500` 约 4 * 10^10。浪费：固定 `i`、`left` 后，右端点越小和越小，满足条件的右端点是一段连续区间。洞察：排序后，若 `nums[i] + nums[left] + nums[right] < target`，则 `right` 换成 `left+1 .. right` 里任何一个都满足，计 `right - left` 个并推进 `left`；否则 `right` 左移。

```python
def three_sum_smaller(nums: list[int], target: int) -> int:
    nums = sorted(nums)                          # 只统计个数、不关心下标，排序不影响答案
    count = 0
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            if nums[i] + nums[left] + nums[right] < target:
                count += right - left            # right 取 left+1..right 都满足：一次统计一批
                left += 1
            else:
                right -= 1                       # 和太大，右端往小的方向缩
    return count
```

运行：`[-2,0,1,3]`, `2` → `2`；`[]`, `0` → `0`；`[0]`, `0` → `0`；`[0,0,0]`, `1` → `1`；`[0,0,0]`, `0` → `0`；`n = 3500` 的随机数组在不到 1 秒内完成。

**复杂度。** 时间 `O(n^2)`（排序 `O(n log n)` 之外，每个 `i` 双指针扫一遍），空间 `O(1)`（不计排序）。

**拓展优化。**
- 对固定的 `i, left` 用 `bisect_left` 在 `nums[left+1:]` 里二分，总时间 `O(n^2 log n)`，不如双指针。
- 把「小于」换成「等于」就是 LC 15 三数之和，需要去重；换成「最接近」是 LC 16。

**易错点。**
- 满足条件后只累加 `1`：应累加 `right - left`；示例一只加 `1` 会得到 `1` 而不是 `2`。
- 条件不满足时移动了 `left`：和太大只能缩 `right`；移动 `left` 会让和更大。
- 空数组或长度小于 3：外层 `range(len(nums) - 2)` 为空，直接返回 `0`；不要对空数组取 `nums[-1]`。

**追问。**
- 返回具体的三元组：满足时枚举 `right` 到 `left+1`，输出规模可能是 `O(n^3)`。
- 四数之和小于目标：固定两个数再双指针，`O(n^3)`。

**同模式。** LC 15 三数之和、LC 16 最接近的三数之和、LC 18 四数之和、LC 167 两数之和 II、LC 611 有效三角形的个数。
