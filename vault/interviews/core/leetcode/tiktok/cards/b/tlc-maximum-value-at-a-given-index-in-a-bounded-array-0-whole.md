---
id: tlc-maximum-value-at-a-given-index-in-a-bounded-array-0-whole
node: b.maximum-value-at-a-given-index-in-a-bounded-array
type: qa
---
## Q
**LC 1802 有界数组中指定下标处的最大值**｜Medium · TikTok 高频

给三个正整数 `n`、`index` 和 `maxSum`。构造数组 `nums`（下标从 `0` 开始），同时满足：`nums.length == n`；每个 `nums[i]` 都是**正整数**；相邻元素之差的绝对值不超过 `1`，即 `abs(nums[i] - nums[i+1]) <= 1`；所有元素之和不超过 `maxSum`；`nums[index]` 的值被**最大化**。返回所构造数组中的 `nums[index]`。`1 <= n <= maxSum <= 10^9`，`0 <= index < n`。例：`n = 4, index = 2, maxSum = 6` → `2`（`[1,1,2,1]` 和 `[1,2,2,1]` 都满足）；`n = 6, index = 1, maxSum = 10` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分答案：对一个候选峰值 `v`，让数组以 `index` 为峰、向两侧每格最多降 `1`、降到 `1` 后保持为 `1`，这样得到的是峰值为 `v` 的**最小和**；最小和随 `v` 单调递增，所以二分找出最小和不超过 `maxSum` 的最大 `v`。最小和用等差数列求和，`O(1)`；总 `O(log maxSum)`。

**识别。** 「最大化某个值，同时受总和限制」是二分答案（binary search on the answer）的标志：如果峰值 `v` 可行，更小的值显然也可行（单调性）。`n, maxSum` 到 `10^9`，不能建数组、不能线性枚举，必须靠公式 + 二分。构造方式也由贪心给出：想让峰最高，其余位置在满足“差不超过 `1`、至少为 `1`”的前提下越小越好。

**推导。** 暴力：从 `1` 开始逐个尝试峰值，每次建数组求和，`O(maxSum · n)`。浪费：峰值的可行性是单调的，不需要全试；求和也不必真的建数组。洞察一：峰值取 `v` 时，各位置的最小值是 `max(v - |i - index|, 1)`——离峰 `d` 格的位置至少是 `v - d`，不能低于 `1`。洞察二：峰一侧 `L` 个位置的和分两种形态：若 `L >= v - 1`，先降到 `1`（等差数列 `v-1, v-2, ..., 1`，和为 `v(v-1)/2`），剩下的位置都是 `1`；若 `L < v - 1`，没降到 `1`，是 `v-1` 到 `v-L` 的等差数列。洞察三：总和 = 左侧 + 峰值 + 右侧，二分最大可行的 `v`。

```python
def max_value(n: int, index: int, max_sum: int) -> int:
    def side(peak: int, length: int) -> int:
        # 峰值一侧 length 个位置的最小和：从 peak-1 逐格降 1，降到 1 后全补 1
        if length >= peak - 1:
            return peak * (peak - 1) // 2 + (length - (peak - 1))
        return (peak - 1 + peak - length) * length // 2

    def total(peak: int) -> int:               # 峰值取 peak 时整个数组的最小和
        return peak + side(peak, index) + side(peak, n - 1 - index)

    lo, hi = 1, max_sum                        # 单调：peak 越大 total 越大
    while lo < hi:
        mid = (lo + hi + 1) // 2               # 上取整，避免 lo = mid 时死循环
        if total(mid) <= max_sum:
            lo = mid                           # mid 放得下，答案至少是 mid
        else:
            hi = mid - 1
    return lo
```

运行：`(4, 2, 6)` → `2`，`(6, 1, 10)` → `3`，`(1, 0, 1)` → `1`，`(3, 0, 3)` → `1`；`(5 * 10^8, 0, 10^9)` → `31623`，`(5 * 10^8, 2 * 10^8, 10^9)` → `22361`，`(10^9, 0, 10^9)` → `1`，均在微秒级完成。

**复杂度。** 时间 `O(log maxSum)`：二分约 `30` 次，每次 `O(1)` 求和；空间 `O(1)`。

**易错点。**
- 一侧求和只用等差数列、不补 `1`：峰值较大而一侧很短时没问题，一侧很长时公式会算出 `0` 或负数项。`(3, 0, 3)` 里峰值取 `2`，右侧两个位置按等差数列算成 `1 + 0 = 1`，总和 `3 <= 3` 误判可行，返回 `2`；但数组必须是正整数，真实最小和是 `2 + 1 + 1 = 4 > 3`，正确答案是 `1`。
- 二分写成 `mid = (lo + hi) // 2` 又用 `lo = mid`：`lo + 1 == hi` 时死循环。求“最大可行”要用上取整 `mid = (lo + hi + 1) // 2`。
- 忘了峰值本身占一格：`total` 里要加 `peak`。

**追问。**
- 标准库二分：`bisect_right(range(1, max_sum + 1), max_sum, key=total)` 返回满足 `total(v) <= max_sum` 的 `v` 的个数，正好等于答案（Python 3.10+ 的 `key` 参数）。
- 求最小和而不是最大值（给定峰值和位置，数组最少需要多少总和）：就是上面的 `total`。
- 差值上限改成 `d`：每格最多降 `d`，等差数列的公差换成 `d`，其余不变。

**同模式。** LC 875 爱吃香蕉的珂珂、LC 1011 在 D 天内送达包裹的能力、LC 410 分割数组的最大值、LC 69 x 的平方根、LC 2517 礼盒的最大甜蜜度。
