---
slug: max-consecutive-ones
---
## Q
**LC 485 最大连续 1 的个数（Max Consecutive Ones）**｜Easy

给定一个二进制数组 `nums`，计算其中最大连续 `1` 的个数。`1 <= nums.length <= 10^5`，`nums[i]` 不是 `0` 就是 `1`。例：`nums = [1,1,0,1,1,1]` → `3`；`nums = [1,0,1,1,0,1]` → `2`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 一次扫描维护当前连续段长度（running count）。

**一句话。** 遇到 `1` 当前段长加一，遇到 `0` 清零，全程记录最大值。

**识别。** 「最长连续段」且只需要长度：当前段的状态只有一个计数，一遍扫描 `O(n)`、`O(1)` 空间。

**推导。** 枚举所有子数组再检查是不是全 1，`O(n^2)` 到 `O(n^3)`；但连续 1 的段互不重叠，每个位置只会属于一个段，边扫边累计即可。

```python
def find_max_consecutive_ones(nums: list[int]) -> int:
    best = run = 0
    for x in nums:
        run = run + 1 if x == 1 else 0     # 遇 1 延长当前连续段，遇 0 清零
        best = max(best, run)
    return best
```

运行：`[1,1,0,1,1,1]` → `3`，`[1,0,1,1,0,1]` → `2`，`[0]` → `0`，`[1]` → `1`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 最多可以把 `k` 个 `0` 翻成 `1`（LC 1004）：滑动窗口，窗口内 `0` 的个数不超过 `k`，窗口长度的最大值就是答案。

```python
def longest_ones(nums: list[int], k: int) -> int:     # LC 1004：最多翻转 k 个 0
    left = zeros = best = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:                  # 窗口里的 0 超过 k 个：左端收缩
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)
    return best
```

**易错点。**
- 只在遇到 `0` 时才更新最大值：数组以 `1` 结尾（`[1,1,1]`）时漏掉最后一段，输出 `0`，正确 `3`。每步都更新，或循环后再取一次。
- 忘记遇到 `0` 把计数清零：`[1,1,0,1]` 会得到 `3`，正确 `2`。

**同模式。** LC 1004 最大连续 1 的个数 III、LC 487 最大连续 1 的个数 II、LC 1446 连续字符、LC 53 最大子数组和。
