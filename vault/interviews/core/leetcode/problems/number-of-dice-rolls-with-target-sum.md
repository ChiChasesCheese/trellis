---
slug: number-of-dice-rolls-with-target-sum
---
## Q
**LC 1155 掷骰子等于目标和的方法数**｜Medium

有 `n` 个骰子，每个有 `k` 个面（点数 `1..k`）。求掷出后点数之和恰为 `target` 的方法数，结果对 `10⁹+7` 取模。

## A
**一句话。** 分组背包式 DP：`f[i][t]` 是前 `i` 个骰子点数和为 `t` 的方法数，第 `i` 个骰子掷出 `x`，就来自 `f[i-1][t-x]`。

```python
def num_rolls_to_target(n, k, target):
    MOD = 10**9 + 7
    f = [[0] * (target + 1) for _ in range(n + 1)]
    f[0][0] = 1                        # 0 个骰子和为 0：一种
    for i in range(1, n + 1):
        for t in range(1, target + 1):
            for x in range(1, min(k, t) + 1):
                f[i][t] = (f[i][t] + f[i - 1][t - x]) % MOD
    return f[n][target]
```

**复杂度。** 时间 `O(n·target·k)`，空间 `O(n·target)`。

**易错点。**
- `x` 的上界：`x` 不能超过 `t`，否则 `t - x` 为负，用 `min(k, t)`。
- 初始值：`f[0][0] = 1`，其余 `f[0][t]` 为 0，写错整个表全是 0。
- 忘了取模：方法数增长极快。

**追问。**
- 怎么优化到 `O(n·target)`？：对 `f[i-1]` 做前缀和，`f[i][t]` 等于一段区间和，省掉对 `x` 的枚举。
- 能压成一维吗？：能，但转移依赖上一行，要倒着更新或用两行滚动。

**同模式。** LC 518 零钱兑换 II、LC 494 目标和、LC 377 组合总和 IV、LC 629 K 个逆序对数组
