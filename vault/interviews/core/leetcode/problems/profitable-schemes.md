---
slug: profitable-schemes
---
## Q
**LC 879 盈利计划**｜Hard

有 `n` 名成员，第 `i` 个计划需要 `group[i]` 人、产生 `profit[i]` 利润，每人只能参加一个计划。选若干计划，使总利润 `≥ minProfit` 且总人数 `≤ n`，求方案数（对 `1e9+7` 取模）。

## A
**一句话。** 0/1 背包：`f[j][k]` 是恰用 `j` 人、利润（封顶到 `minProfit`）为 `k` 的方案数，人数倒序避免重复选。

```python
def profitable_schemes(n, min_profit, group, profit):
    MOD = 10 ** 9 + 7
    # f[j][k]：恰用 j 人、利润封顶后为 k 的方案数
    f = [[0] * (min_profit + 1) for _ in range(n + 1)]
    f[0][0] = 1
    for g, p in zip(group, profit):
        for j in range(n, g - 1, -1):   # 人数倒序：每个计划只选一次
            for k in range(min_profit + 1):
                t = min(min_profit, k + p)   # 利润封顶
                f[j][t] = (f[j][t] + f[j - g][k]) % MOD
    return sum(f[j][min_profit] for j in range(n + 1)) % MOD
```

**复杂度。** 时间 `O(len · n · minProfit)`，空间 `O(n · minProfit)`。

**易错点。**
- 利润不封顶：状态只在意「是否 `≥ minProfit`」，封顶才能让第二维不超过 `minProfit`。
- 人数正序遍历：同一个计划被重复选。
- 答案只取 `f[n][min_profit]`：`n` 是人数上限，要把所有 `j ≤ n` 的方案加起来。

**追问。**
- 为什么初值是 `f[0][0] = 1`？：什么都不选算一个方案，利润为 `0`，后面靠转移累加。
- 利润 `p = 0` 的计划会怎样？：`t = k`，转移到同一格，仍然正确，因为 `j - g < j` 读的是旧值。

**同模式。** LC 474 一和零、LC 494 目标和、LC 416 分割等和子集
