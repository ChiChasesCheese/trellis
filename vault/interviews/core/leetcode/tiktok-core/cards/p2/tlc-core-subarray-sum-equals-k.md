---
id: tlc-core-subarray-sum-equals-k
node: p2.subarray-sum-equals-k
type: qa
---
## Q
**LC 560 和为 K 的子数组**｜Medium · LC TikTok 近 6 个月热度 50/100（全时段 75） · 近一年被问：美国 2 次、国内 1 次 · CodeTop 国内累计 30 次 · 最近 2026-10-26（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100

给整数数组 `nums` 和整数 `k`，统计并返回该数组中**和为 `k` 的子数组的个数**。子数组是数组中元素的连续非空序列。`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`，`-10^7 <= k <= 10^7`。例：`nums = [1,1,1], k = 2` → `2`；`nums = [1,2,3], k = 3` → `2`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前缀和（prefix sum）加哈希表：记 `pre` 为到当前位置的前缀和，以当前位置结尾、和为 `k` 的子数组个数，等于此前出现过前缀和 `pre - k` 的次数。`O(n)`。

**识别。** 「连续子数组的和」= 两个前缀和之差，`sum(i..j) = pre[j] - pre[i-1]`。元素可以是**负数**，所以滑动窗口失效（窗口和不再随右端扩大而单调变大）。要的是「个数」而不是「是否存在」，哈希表要存次数。

**推导。** 暴力枚举所有 `(i, j)` 并求和，`O(n^3)`；用前缀和 `O(1)` 求区间和，`O(n^2)` → 浪费：固定右端 `j` 后，在左端里一个个找 `pre[i-1] = pre[j] - k` → 这是一个「确定的值出现过几次」的查询，哈希表 `O(1)` 回答 → 边扫边查边存，`O(n)`。

**简单解法。** 暴力：固定左端点，右端点向右走并累加，和等于 `k` 就计数；不能提前停，因为有负数。

```python
def subarray_sum(nums: list[int], k: int) -> int:
    ans = 0
    for left in range(len(nums)):
        total = 0
        for right in range(left, len(nums)):
            total += nums[right]                    # [left, right] 的和，边走边累加
            if total == k:
                ans += 1                            # 有负数，后面还可能再回到 k，所以继续走
    return ans
```

时间 `O(n^2)`，空间 `O(1)`；`n` 到 `2 * 10^4` 量级时约 `2 * 10^8` 步，Python 里会超时，作开场答案，再引到「固定右端点，查前缀和 `pre - k` 出现过几次」。

最优解：

```python
from collections import Counter

def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```

运行：`([1,1,1], 2)` → `2`，`([1,2,3], 3)` → `2`，`([1,-1,1], 1)` → `3`，`([0,0,0], 0)` → `6`，`([1], 0)` → `0`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（最多 `n + 1` 个不同的前缀和）。

**拓展优化。**
- 求最长的和为 `k` 的子数组长度（LC 325）：字典存前缀和第一次出现的下标，不存次数：
```python
def longest_subarray_sum(nums: list[int], k: int) -> int:
    first = {0: -1}                                 # 前缀和 -> 第一次出现的下标；空前缀在 -1
    pre = best = 0
    for i, x in enumerate(nums):
        pre += x
        if pre - k in first:
            best = max(best, i - first[pre - k])    # 起点越靠前越长，所以只留第一次
        first.setdefault(pre, i)                    # 已有就不覆盖
    return best
```
- 元素全是非负数时可以用滑动窗口，`O(1)` 空间：「和恰好 `k`」= 「和至多 `k`」减「和至多 `k-1`」（有负数时窗口不单调，这个方法失效）：
```python
def subarray_sum_nonneg(nums: list[int], k: int) -> int:
    def at_most(limit: int) -> int:                 # 和 <= limit 的子数组个数
        if limit < 0:
            return 0
        left = total = count = 0
        for right, x in enumerate(nums):
            total += x
            while total > limit:                    # 非负数：窗口和随右端单调增，超了就收左端
                total -= nums[left]
                left += 1
            count += right - left + 1
        return count

    return at_most(k) - at_most(k - 1)
```

**易错点。**
- 初始必须有 `{0: 1}`：代表空前缀，否则从下标 0 开始的子数组数不到。`[3]`、`k = 3` 会返回 `0`，正确是 `1`。
- 必须先查后存：先 `seen[pre] += 1` 再查，`k = 0` 时会把「空子数组」算进去。`[1]`、`k = 0` 会返回 `1`，正确是 `0`。
- 不能用滑动窗口：有负数时，`[1,-1,1]`、`k = 1` 的窗口法只数到 `2` 个，正确是 `3`。

**追问。**
- 和能被 `k` 整除（LC 974）：把 `pre % k` 当键，同余的两个前缀和之差被 `k` 整除。
- 二维矩阵里和为 `k` 的子矩阵（LC 1074）：固定上下边，把每列压成一维数组，再套用同样的前缀和做法。

**同模式。** LC 523 连续的子数组和、LC 525 连续数组（0/1 换成 ±1）、LC 974 和可被 K 整除的子数组、LC 1 两数之和（同样是「查补数」）。
