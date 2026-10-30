---
id: tlc-last-stone-weight-ii-2-code
node: a.last-stone-weight-ii
type: qa
step: 2
---
## Q
**LC 1049 最后一块石头的重量 II**｜写出 Python 实现

整数数组 `stones`（长度 `1` 到 `30`，每个值 `1` 到 `100`）。每回合任选两块石头，重量 `x <= y`：相等则都粉碎，否则剩下重量 `y - x` 的一块。返回最后剩下的石头的最小可能重量（全部粉碎则为 `0`）。

## A
**思路。** 最终重量是 `|S1 - S2|`，`S1 + S2` 等于总重。用布尔表 `dp[i][s]` 表示只用前 `i` 块石头能否挑出总重恰为 `s` 的一堆，容量上限取 `总重 // 2`；基础行 `dp[0][0] = True`；第 `i` 块石头选或不选，分别读上一行的 `dp[i-1][s-w]` 和 `dp[i-1][s]`；取最后一行里不超过上限的最大可达 `s`，答案是 `总重 - 2 * s`。

```python
def last_stone_weight_ii(stones: list[int]) -> int:
    n = len(stones)
    total = sum(stones)
    half = total // 2                      # 较小的一堆最多是 total // 2
    # dp[i][s]：只用前 i 块石头，能否挑出总重恰为 s 的一堆
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True                        # 基础行：一块都不选，只能凑出 0
    for i in range(1, n + 1):
        w = stones[i - 1]
        for s in range(half + 1):
            dp[i][s] = dp[i - 1][s] or (s >= w and dp[i - 1][s - w])   # 不选第 i 块 / 选第 i 块
    best = max(s for s in range(half + 1) if dp[n][s])   # 最后一行里不超过 half 的最大可达重量
    return total - 2 * best
```

运行：`[2,7,4,1,8,1]` → `1`，`[31,26,33,21,40]` → `5`，`[1]` → `1`，`[1,1]` → `0`，`[100] * 30` → `0`。

**复杂度。** 时间 `O(n · total / 2)`：每块石头填一行容量；空间 `O(n · total / 2)`，整张表。

**写法要点。** `[[False] * (half + 1) for _ in range(n + 1)]` 每行是独立的列表，多出的第 `0` 行是基础行（一块都不选）；第 `i` 行对应 `stones[i - 1]`，所以先取 `w = stones[i - 1]`；`dp[i - 1][s] or (s >= w and dp[i - 1][s - w])` 用短路表达「不选 / 选」两种来源，`s >= w and` 放在前面，避免 `s - w` 变成负下标而悄悄回绕；`max(生成器)` 取最后一行里最大的可达重量，`dp[n][0]` 恒为 `True`，所以一定非空；`sum(stones) // 2` 的整除保证容量是整数。
