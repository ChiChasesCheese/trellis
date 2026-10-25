---
id: tlc-coin-change-ii-4-followup
node: b.coin-change-ii
type: qa
step: 4
---
## Q
**LC 518 零钱兑换 II**｜追问

面试官接着问：（1）问排列数（LC 377）怎么改？（2）求最少硬币个数（LC 322）？（3）每种硬币只能用一次？（4）`amount` 很大（比如 `10^9`）而硬币面额很少？

## A
1. **排列数**：互换两层循环，外层金额、内层硬币；每个金额的最后一枚硬币可以是任意一种，不同顺序分别计数。

```python
def combination_sum4(nums: list[int], target: int) -> int:
    ways = [0] * (target + 1)
    ways[0] = 1
    for a in range(1, target + 1):
        for x in nums:
            if x <= a:
                ways[a] += ways[a - x]
    return ways[target]
```

`combination_sum4([1,2], 3)` → `3`。
2. **最少个数**：状态变成最小值，初值设成无穷：`dp[a] = min(dp[a], dp[a - coin] + 1)`，`dp[0] = 0`，循环顺序无关紧要（求最优值不会重复计数）。
3. **每种只用一次**：内层金额倒序 `range(amount, coin - 1, -1)`，这样 `ways[a - coin]` 还是没用过当前硬币的值（`(5, [1,2,5])` 会得到 `1`）。
4. **`amount` 很大**：DP 数组装不下。面额很少时用矩阵快速幂 / 生成函数（母函数）：答案是 `1 / ∏(1 - x^c)` 展开后 `x^amount` 的系数，可以用线性递推加快速幂求解；面试里通常只需要说出这个方向。

**Python 提醒**：二维写法要用 `[[0] * (amount + 1) for _ in coins]`，不要写 `[[0] * (amount + 1)] * len(coins)`——后者每一行都是同一个列表的引用，改一行就改全部。
