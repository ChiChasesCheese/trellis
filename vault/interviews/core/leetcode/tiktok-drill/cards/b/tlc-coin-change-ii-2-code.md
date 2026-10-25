---
id: tlc-coin-change-ii-2-code
node: b.coin-change-ii
type: qa
step: 2
---
## Q
**LC 518 零钱兑换 II**｜写出 Python 实现

`coins` 是 `1` 到 `300` 个互不相同的面额（每个在 `[1, 5000]`），`amount` 在 `[0, 5000]`，每种硬币有无限个。返回凑成 `amount` 的硬币组合数，凑不出返回 `0`。

## A
**思路。** 一维数组 `ways[a]` 表示凑出金额 `a` 的组合数，`ways[0] = 1`。外层遍历每种硬币，内层从 `coin` 到 `amount` 正序更新 `ways[a] += ways[a - coin]`；处理完一种硬币后，`ways` 就是只用到目前为止这些硬币的组合数。

```python
def change(amount: int, coins: list[int]) -> int:
    ways = [0] * (amount + 1)          # ways[a]：凑出金额 a 的组合数
    ways[0] = 1                        # 凑出 0 元只有一种：什么都不拿
    for coin in coins:                 # 外层枚举硬币：每种硬币只「决定一次」用多少，组合不会因顺序重复
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]  # 正序：同一种硬币可以重复使用
    return ways[amount]
```

运行：`(5, [1,2,5])` → `4`，`(3, [2])` → `0`，`(10, [10])` → `1`，`(0, [7])` → `1`；`amount = 5000`、`coins = 1..300` 不到 `0.1` 秒。

**复杂度。** 时间 `O(len(coins) · amount)`，约 `1.5 * 10^6` 次加法；空间 `O(amount)`。

**写法要点。** `range(coin, amount + 1)` 从 `coin` 开始，小于面额的金额不可能用这种硬币，省掉 `if a >= coin`；`ways[a] += ...` 是原地累加，所以遍历方向决定语义（正序：可重复用；倒序：只能用一次）；初值 `[0] * (amount + 1)` 对不可变的整数安全；`amount = 0` 时 `range` 为空，直接返回 `ways[0] = 1`。
