---
slug: stone-game-ii
---
## Q
**LC 1140 石子游戏 II**｜Medium

一排石子堆，Alice 先手，当前上限 `M`（初始 1）时可拿剩下最前面的 `X` 堆（`1 ≤ X ≤ 2M`），之后 `M = max(M, X)`。双方最优，求 Alice 最多拿多少。

## A
**一句话。** 博弈 DP：`dfs(i, m)` 是从第 `i` 堆起、上限 `m` 时当前玩家最多拿多少 = 剩余总和 - 对手在下一状态的最优值。

```python
def stone_game_ii(piles):
    n = len(piles)
    suf = list(accumulate(piles[::-1]))[::-1] + [0]

    @cache
    def dfs(i, m):               # 当前玩家从 i 起最多拿多少
        if i + 2 * m >= n:
            return suf[i]        # 能全拿就全拿
        return max(suf[i] - dfs(i + x, max(m, x))
                   for x in range(1, 2 * m + 1))

    return dfs(0, 1)
```

**复杂度。** 时间 `O(n^3)`，空间 `O(n^2)`。

**易错点。**
- 分别记两人的分数：状态翻倍且容易混；用「总和 - 对手最优」只需一个值。
- 能全拿时还去枚举：`i + 2m ≥ n` 时直接返回后缀和，否则会越界或多算。

**追问。**
- 为什么是 `O(n^3)`？：状态 `n × n`，每个枚举 `O(n)` 个 `x`。
- 递推写法？：`i` 从大到小、`m` 任意顺序填表，`m` 只需到 `n`。

**同模式。** LC 877 石子游戏、LC 486 预测赢家、LC 1406 石子游戏 III
