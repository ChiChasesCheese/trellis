---
id: tlc-subarrays-with-k-different-integers-0-whole
node: c.subarrays-with-k-different-integers
type: qa
---
## Q
**LC 992 K 个不同整数的子数组**｜Hard · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 1 次 · 最近 2023-03-20（国内 CodeTop）

给定正整数数组 `nums` 和整数 `k`，返回 `nums` 中「好子数组」的数目：子数组是连续的，且其中不同整数的个数恰好为 `k`。`1 <= nums.length <= 2 * 10^4`，`1 <= nums[i], k <= nums.length`。例：`nums = [1,2,1,2,3], k = 2` → `7`；`nums = [1,2,1,3,4], k = 3` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 「恰好 `k` 个不同」不满足滑动窗口的单调性，但「至多 `k` 个」满足，所以答案是 `atMost(k) - atMost(k - 1)`。

**识别。** 子数组计数 + 「不同整数个数」约束：窗口右移只会增加或保持不同数个数，左移只会减少，可以用双指针；但「恰好」不单调，要拆成两个「至多」的差。

**推导。** 暴力：枚举所有子数组并统计不同数，`O(n^2)`，`n = 2 * 10^4` 约 2 * 10^8 次集合操作。洞察：固定右端 `right`，使「至多 `limit` 个不同」成立的左端是一段连续范围 `[left, right]`，贡献 `right - left + 1` 个子数组，`left` 只增不减；恰好 `k` 个 = 至多 `k` 个 - 至多 `k-1` 个。

```python
from collections import defaultdict


def subarrays_with_k_distinct(nums: list[int], k: int) -> int:
    def at_most(limit: int) -> int:              # 不同整数个数 <= limit 的子数组数
        count: defaultdict[int, int] = defaultdict(int)
        distinct = left = total = 0
        for right, x in enumerate(nums):
            if count[x] == 0:
                distinct += 1
            count[x] += 1
            while distinct > limit:              # 窗口超限：左端收缩直到合法
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    distinct -= 1
                left += 1
            total += right - left + 1            # 以 right 结尾、左端在 [left, right] 的子数组都合法
        return total

    return at_most(k) - at_most(k - 1)           # 「恰好 k 个」= 「至多 k 个」 - 「至多 k-1 个」
```

运行：`[1,2,1,2,3]`, `k = 2` → `7`；`[1,2,1,3,4]`, `k = 3` → `3`；`[1]`, `k = 1` → `1`；`[1,1,1]`, `k = 1` → `6`；`[1,2,3]`, `k = 4` → `0`。

**复杂度。** 时间 `O(n)`（两次扫描，每个下标进出窗口各一次），空间 `O(n)`。

**拓展优化。**
- 一次遍历：维护窗口的同时记录左端还能「多缩几位」的数量 `prefix`，每个右端贡献 `prefix + 1`：

```python
def subarrays_with_k_distinct_one_pass(nums: list[int], k: int) -> int:
    count: defaultdict[int, int] = defaultdict(int)
    distinct = left = prefix = result = 0        # prefix：窗口左端可以多缩的位置数（这些数在窗口内出现不止一次）
    for x in nums:
        count[x] += 1
        if count[x] == 1:
            distinct += 1
        if distinct > k:                         # 刚好多出一个新数：窗口最左边的数此时只出现一次，删掉它
            count[nums[left]] -= 1
            left += 1
            distinct -= 1
            prefix = 0
        if distinct == k:
            while count[nums[left]] > 1:         # 左端是重复数字：可以删而不改变 distinct
                count[nums[left]] -= 1
                left += 1
                prefix += 1
            result += prefix + 1                 # 左端取 left-prefix .. left 都是恰好 k 个
    return result
```

**易错点。**
- 直接用「恰好 `k`」收缩窗口：`[1,2,1,2,3]`, `k = 2` 时窗口恰好 2 个后，缩左端可能仍是 2 个也可能变 1 个，没有单调性，会漏掉子数组。
- 把贡献写成 `1`（只数窗口本身）：应数以 `right` 结尾的所有合法左端，`right - left + 1`。
- `at_most(0)`：`k = 1` 时要算 `at_most(0)`，窗口会一直收缩到空，结果为 `0`，不要特判成别的值。

**追问。**
- 把「恰好 k 个」问题推广：LC 1248 统计优美子数组、LC 930 和相同的二元子数组，同样是「至多」之差。
- 最长的恰好 `k` 个不同的子数组：直接滑动窗口，窗口合法时记录长度即可，因为是求最长，单调性够用（LC 340）。

**同模式。** LC 340 至多包含 K 个不同字符的最长子串、LC 904 水果成篮、LC 930 和相同的二元子数组、LC 1248 统计优美子数组、LC 3 无重复字符的最长子串。
