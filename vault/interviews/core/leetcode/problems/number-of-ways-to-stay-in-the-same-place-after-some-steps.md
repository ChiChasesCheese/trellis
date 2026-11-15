---
slug: number-of-ways-to-stay-in-the-same-place-after-some-steps
---
## Q
**LC 1269 停在原地的方案数**｜Hard

长度为 `arrLen` 的数组，指针从下标 `0` 出发。每步可向左、向右移动一格或原地不动，不能出界。求恰好 `steps` 步后指针回到 `0` 的方案数（对 `1e9+7` 取模）。

## A
**一句话。** `f[t][j]` 是走 `t` 步停在 `j` 的方案数，来自上一步的 `j-1`、`j`、`j+1`；位置只需保留到 `steps // 2`（走太远回不来）。

```python
def num_ways(steps, arr_len):
    MOD = 10 ** 9 + 7
    n = min(arr_len, steps // 2 + 1)      # 走太远就回不来了
    f = [[0] * n for _ in range(steps + 1)]
    f[0][0] = 1                           # f[t][j]：t 步后在 j
    for t in range(1, steps + 1):
        for j in range(n):
            f[t][j] = f[t - 1][j]         # 原地
            if j:
                f[t][j] += f[t - 1][j - 1]    # 从左边来
            if j + 1 < n:
                f[t][j] += f[t - 1][j + 1]    # 从右边来
            f[t][j] %= MOD
    return f[steps][0]
```

**复杂度。** 时间 `O(steps · min(arrLen, steps/2))`，空间 `O(steps · min(arrLen, steps/2))`。

**易错点。**
- 位置维度开到 `arrLen`：`arrLen` 可达 `10^6`，会超时爆内存，只需到 `steps // 2`。
- 忘了出界判断：`j - 1` 要检查 `j > 0`，`j + 1` 要检查 `j + 1 < n`。
- 只取模一次：每个格子累加三项后立刻取模，避免大整数拖慢。

**追问。**
- 为什么只需 `steps // 2` 个位置？：走出去还要走回来，最远只能到 `steps // 2`。
- 空间能压到 `O(n)` 吗？：`f[t]` 只依赖 `f[t-1]`，可以用两行滚动。

**同模式。** LC 70 爬楼梯、LC 62 不同路径、LC 576 出界的路径数
