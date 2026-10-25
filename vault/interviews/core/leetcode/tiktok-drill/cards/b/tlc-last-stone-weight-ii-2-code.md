---
id: tlc-last-stone-weight-ii-2-code
node: b.last-stone-weight-ii
type: qa
step: 2
---
## Q
**LC 1049 最后一块石头的重量 II**｜写出 Python 实现

整数数组 `stones`（长度 `1` 到 `30`，每个值 `1` 到 `100`）。每回合任选两块石头，重量 `x <= y`：相等则都粉碎，否则剩下重量 `y - x` 的一块。返回最后剩下的石头的最小可能重量（全部粉碎则为 `0`）。

## A
**思路。** 最终重量是 `|S1 - S2|`，`S1 + S2` 等于总重。用布尔数组 `dp[s]` 表示能否挑出总重恰为 `s` 的一堆，容量上限取 `总重 // 2`；对每块石头倒序更新（每块只用一次）；取不超过上限的最大可达 `s`，答案是 `总重 - 2 * s`。

```python
def last_stone_weight_ii(stones: list[int]) -> int:
    total = sum(stones)
    half = total // 2                      # 较小的一堆最多是 total // 2
    dp = [False] * (half + 1)              # dp[s]：能否从石头里挑出总重恰为 s 的一堆
    dp[0] = True
    for w in stones:
        for s in range(half, w - 1, -1):   # 倒序：每块石头只用一次（0/1 背包）
            dp[s] = dp[s] or dp[s - w]
    best = next(s for s in range(half, -1, -1) if dp[s])   # 不超过 half 的最大可达重量
    return total - 2 * best
```

运行：`[2,7,4,1,8,1]` → `1`，`[31,26,33,21,40]` → `5`，`[1]` → `1`，`[1,1]` → `0`，`[100] * 30` → `0`。

**复杂度。** 时间 `O(n · total / 2)`：每块石头扫一遍容量；空间 `O(total / 2)`。

**写法要点。** `range(half, w - 1, -1)` 既倒序又自动跳过容量小于 `w` 的位置，省掉 `if s >= w`；`dp[s] = dp[s] or dp[s - w]` 用短路表达「不选 / 选」两种来源；`next(生成器)` 取第一个满足条件的值，`dp[0]` 恒为 `True`，所以一定能找到，不需要默认值；`sum(stones) // 2` 的整除保证容量是整数。
