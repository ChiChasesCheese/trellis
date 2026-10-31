---
id: tlc-maximum-size-subarray-sum-equals-k-0-whole
node: c.maximum-size-subarray-sum-equals-k
type: qa
---
## Q
**LC 325 和等于 k 的最长子数组长度**｜Medium · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 3 次 · 最近 2022-11-24（国内 CodeTop）

给定数组 `nums` 和目标值 `k`，找到和等于 `k` 的最长连续子数组的长度，不存在则返回 `0`。`1 <= nums.length <= 2 * 10^5`，`-10^4 <= nums[i] <= 10^4`，`-10^9 <= k <= 10^9`。例：`nums = [1,-1,5,-2,3]`，`k = 3` → `4`（子数组 `[1,-1,5,-2]`）；`nums = [-2,-1,2,1]`，`k = 1` → `2`（子数组 `[-1,2]`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前缀和加哈希表：只记录每个前缀和第一次出现的下标，遍历到第 `i` 位时查 `前缀和 - k` 是否出现过，出现过就得到一个以 `i` 结尾的候选长度。

**识别。** 「连续子数组的和等于目标」且元素有负数：滑动窗口失效（窗口和不单调），转前缀和哈希。要「最长」所以哈希里只存最早出现的位置。

**推导。** 暴力：枚举所有起止点，`O(n²)`，`n = 2 * 10^5` 太慢。设前缀和 `P[i]`，子数组 `(j, i]` 的和是 `P[i] - P[j]`，等于 `k` 当且仅当 `P[j] = P[i] - k`。对固定的 `i`，要长度最大就要 `j` 最小，即 `P[j]` 第一次出现的位置。

```python
def max_sub_array_len(nums: list[int], k: int) -> int:
    first_seen = {0: -1}                         # 前缀和 -> 最早出现的下标；空前缀的和 0 在下标 -1
    prefix = 0
    best = 0
    for i, x in enumerate(nums):
        prefix += x
        if (start := first_seen.get(prefix - k)) is not None:
            best = max(best, i - start)          # 子数组 (start, i]，长度 i - start
        first_seen.setdefault(prefix, i)         # 只在第一次出现时记录，保证子数组尽可能长
    return best
```

运行：`([1,-1,5,-2,3], 3)` → `4`，`([-2,-1,2,1], 1)` → `2`；`([1,2,3], 7)` → `0`；`([0,0,0], 0)` → `3`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- 元素全为正数时前缀和递增，双指针滑动窗口 `O(1)` 空间。
- 计数而不是求最长（LC 560 和为 K 的子数组）：哈希表存每个前缀和出现的次数，用 `Counter` 累计。

```python
from collections import Counter


def subarray_sum_count(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})                       # 前缀和 -> 出现次数
    prefix = count = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]                # 每个更早的相同前缀和都对应一个合法起点
        seen[prefix] += 1
    return count
```

**易错点。**
- 用 `first_seen[prefix] = i` 覆盖：记录的是最近出现的位置，得到的是最短子数组，`[0,0,0]`、`k = 0` 会返回 `1` 而不是 `3`。
- 忘了 `{0: -1}`：从开头就满足的子数组（如 `[1,-1,5,-2]`）算不出来，示例 1 会得到 `2`。

**追问。**
- 最短的和为 `k` 的子数组：哈希表存最近出现的位置，且元素有负数时仍用此法；全正数用滑动窗口。
- 数据流式到来：哈希表是增量的，每来一个数 `O(1)` 更新。

**同模式。** LC 560 和为 K 的子数组、LC 525 连续数组、LC 523 连续的子数组和、LC 974 和可被 K 整除的子数组、LC 930 和相同的二元子数组。
