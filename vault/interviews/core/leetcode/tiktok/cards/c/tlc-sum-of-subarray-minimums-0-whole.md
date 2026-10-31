---
id: tlc-sum-of-subarray-minimums-0-whole
node: c.sum-of-subarray-minimums
type: qa
---
## Q
**LC 907 子数组的最小值之和**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 4 次 · 最近 2024-09-18（国内 CodeTop）

给定整数数组 `arr`，求 `min(b)` 的总和，其中 `b` 取遍 `arr` 的每个连续子数组。答案可能很大，返回模 `10^9 + 7` 的结果。`1 <= arr.length <= 3 * 10^4`，`1 <= arr[i] <= 3 * 10^4`。例：`arr = [3,1,2,4]` → `17`（各子数组最小值为 3、1、2、4、1、1、2、1、1、1）；`arr = [11,81,94,43,3]` → `444`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 反过来算每个元素的贡献：`arr[i]` 乘以「以它为最小值的子数组个数」，个数 = 左边能延伸的长度 × 右边能延伸的长度，边界用一趟单调栈（monotonic stack）求出，`O(n)`。

**识别。** 「所有子数组的最小值（最大值）之和」是单调栈 + 贡献法的固定信号：子数组有 `O(n²)` 个，但每个子数组恰有一个最小值位置，按位置分组后只剩 `n` 次乘法。

**推导。** 暴力：固定左端点，右端点前进并维护最小值，`O(n²)`；浪费在许多子数组共用同一个最小值，却被逐个累加。设 `L` 是 `i` 左边第一个**小于** `arr[i]` 的下标，`R` 是右边第一个**小于等于** `arr[i]` 的下标，则贡献 `arr[i] * (i - L) * (R - i)`；一侧严格、一侧不严格，并列最小值只归一个位置，不重不漏。

```python
def sum_subarray_mins(arr: list[int]) -> int:
    MOD = 10**9 + 7
    stack: list[int] = []                        # 下标栈，对应的值严格递增
    total = 0
    for i, x in enumerate(arr + [0]):            # 末尾哨兵 0（元素都 >= 1）把栈全部弹空
        while stack and arr[stack[-1]] >= x:     # x 是 arr[j] 右边第一个 <= 它的数
            j = stack.pop()
            left = stack[-1] if stack else -1    # 弹出后的栈顶是左边第一个 < arr[j] 的数
            total += arr[j] * (j - left) * (i - j)   # 左端点 j-left 种，右端点 i-j 种
        stack.append(i)
    return total % MOD                           # Python 整数不溢出，最后取模一次
```

运行：`[3,1,2,4]` → `17`，`[11,81,94,43,3]` → `444`；`[1]` → `1`，`[2,2,2]` → `12`，`[30000] * 30000` → `449905500`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**拓展优化。**
- DP 写法：`dp[i]` 是以 `i` 结尾的所有子数组的最小值之和，同样一趟单调栈。

```python
def sum_subarray_mins_dp(arr: list[int]) -> int:
    stack: list[int] = []
    dp = [0] * len(arr)                          # dp[i]：以 i 结尾的子数组最小值之和
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] >= x:
            stack.pop()
        prev = stack[-1] if stack else -1        # prev 左边的子数组最小值不受 x 影响
        dp[i] = x * (i - prev) + (dp[prev] if prev >= 0 else 0)   # prev 右边（含 i）的 i-prev 个子数组最小值都是 x
        stack.append(i)
    return sum(dp) % (10**9 + 7)
```

**易错点。**
- 两侧都用严格比较：并列最小值被重复计数，`[2,2,2]` 会算成 `20`。
- 忘了哨兵：栈里剩下的元素没结算，漏掉右边延伸到数组末尾的子数组。
- 长度多加减 1：左边 `j - left`、右边 `i - j` 都已含 `j` 自身。

**追问。**
- 最大值之和：比较方向反过来；两者相减就是所有子数组极差之和（LC 2104）。
- 子数组长度受限：`(j - left)` 与 `(i - j)` 要换成满足长度的配对数。

**同模式。** LC 2104 子数组范围和、LC 84 柱状图中最大的矩形、LC 496 下一个更大元素 I、LC 739 每日温度、LC 1856 子数组最小乘积的最大值。
