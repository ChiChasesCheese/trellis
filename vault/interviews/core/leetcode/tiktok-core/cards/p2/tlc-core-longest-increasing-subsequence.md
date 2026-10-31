---
id: tlc-core-longest-increasing-subsequence
node: p2.longest-increasing-subsequence
type: qa
---
## Q
**LC 300 最长递增子序列**｜Medium · LC TikTok 近 6 个月热度 88/100（全时段 88） · 近一年被问：美国 1 次、国内 3 次 · CodeTop 国内累计 109 次 · 最近 2026-09-16（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给整数数组 `nums`，求其中**最长严格递增子序列**的长度。子序列是删除（或不删除）若干元素、不改变其余元素相对顺序得到的序列，不要求连续。`1 <= nums.length <= 2500`，`-10^4 <= nums[i] <= 10^4`。进阶：能否做到 `O(n log n)`？例：`[10,9,2,5,3,7,101,18]` → `4`（如 `[2,3,7,101]`）；`[0,1,0,3,2,3]` → `4`；`[7,7,7,7,7,7,7]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 维护数组 `tails`，`tails[k]` 是「长度为 `k+1` 的递增子序列的最小可能结尾」；它永远严格递增，每来一个数用二分（`bisect_left`）找到第一个 `>= x` 的位置：找不到就追加（最长长度加一），找到就替换（让该长度的结尾更小）。答案是 `len(tails)`。`O(n log n)`。

**识别。** 「子序列（不连续）+ 最长 + 递增」是最长递增子序列。`n <= 2500` 允许 `O(n^2)` 动态规划，题目进阶明确要 `O(n log n)`，信号就是「某个长度的最优结尾」这类单调结构上的二分。

**推导。** 暴力：枚举所有子序列 `O(2^n)`。动态规划：`dp[i]` 表示以 `nums[i]` 结尾的最长长度，`dp[i] = 1 + max(dp[j])`（`j < i` 且 `nums[j] < nums[i]`），`O(n^2)`。浪费在于每个 `i` 都扫描全部 `j`。洞察：对每个长度，只需要记住"结尾最小"的那个子序列，因为结尾越小，后面越容易接上去。这些最小结尾随长度严格递增，所以可以二分。新数 `x` 能接在所有结尾 `< x` 的序列之后，因此落在第一个 `>= x` 的位置。

**简单解法。** 一维动态规划：`dp[i]` 是以 `nums[i]` 结尾的最长长度，取前面所有满足 `nums[j] < nums[i]` 的 `dp[j]` 的最大值加一。

```python
def length_of_lis(nums: list[int]) -> int:
    n = len(nums)
    dp = [1] * n                                   # 每个元素自己至少是长度 1
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:                  # 严格递增：相等不能接
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

时间 `O(n^2)`、空间 `O(n)`；`n <= 2500` 能过，是最稳的开场答案，但进阶问 `O(n log n)`。

最优解：

```python
from bisect import bisect_left


def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for x in nums:
        i = bisect_left(tails, x)                  # 严格递增：第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)                        # x 比所有结尾都大：最长长度 +1
        else:
            tails[i] = x                           # 让长度 i+1 的结尾变得更小，对后面更有利
    return len(tails)
```

运行：`[10,9,2,5,3,7,101,18]` → `4`；`[0,1,0,3,2,3]` → `4`；`[7,7,7,7,7,7,7]` → `1`；`[5]` → `1`；`[1,2,3,4]` → `4`；`[4,3,2,1]` → `1`。

**复杂度。** 时间 `O(n log n)`：每个元素一次二分；空间 `O(n)`。

**拓展优化。**
- 输出一个最长序列本身：`tails` 存下标，再用 `prev[i]` 记下落位时左邻的下标，最后沿 `prev` 回溯。

```python
from bisect import bisect_left

def lis_sequence(nums: list[int]) -> list[int]:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列最小结尾的下标
    prev = [-1] * len(nums)                        # prev[i] = 以 nums[i] 结尾时，前一个元素的下标
    for i, x in enumerate(nums):
        k = bisect_left(tails, x, key=lambda t: nums[t])
        if k:
            prev[i] = tails[k - 1]                 # x 接在长度 k 的那条序列后面
        if k == len(tails):
            tails.append(i)
        else:
            tails[k] = i
    res: list[int] = []
    i = tails[-1]
    while i != -1:                                 # 沿前驱回溯，得到逆序
        res.append(nums[i])
        i = prev[i]
    return res[::-1]
```

**易错点。**
- 严格递增用 `bisect_left`。写成 `bisect_right` 就变成了「非严格递增」：`[7,7,7,7,7,7,7]` 得到 `7`，正确是 `1`。
- `tails` 不是一条真实的子序列，只有长度有意义。`[4,5,1]` 处理后 `tails = [1, 5]`，但 `1` 在 `5` 后面，`[1,5]` 并不是子序列；长度 `2` 是对的。
- 想要序列本身，必须额外记录每个元素的前驱下标。

**追问。**
- 非严格递增（允许相等）：把 `bisect_left` 换成 `bisect_right`；`[7]*7` 得 `7`。
- 俄罗斯套娃信封（LC 354）：按宽度升序、宽度相同时高度降序排序，再对高度求严格 LIS。

**同模式。** LC 673 最长递增子序列的个数、LC 354 俄罗斯套娃信封问题、LC 1671 得到山形数组的最少删除次数、LC 646 最长数对链、LC 1143 最长公共子序列。
