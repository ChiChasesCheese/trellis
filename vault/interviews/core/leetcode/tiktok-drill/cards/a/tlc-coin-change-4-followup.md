---
id: tlc-coin-change-4-followup
node: a.coin-change
type: qa
step: 4
---
## Q
**LC 322 零钱兑换**｜追问

面试官接着问：（1）输出具体用了哪些硬币，不只是个数？（2）问有多少种凑法（组合数）？（3）能不能用 BFS 做，什么时候更合适？

## A
1. **输出方案**：多一个数组 `pick[a]` 记录凑成 `a` 时最后加的那枚硬币，最后从 `amount` 往回走。`[1,2,5]`、`11` 得到 `[1, 5, 5]`。
```python
def coin_change_path(coins: list[int], amount: int) -> list[int]:
    inf = amount + 1
    dp = [0] + [inf] * amount
    pick = [0] * (amount + 1)             # pick[a]：凑成 a 时最后加的那枚硬币
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a], pick[a] = dp[a - c] + 1, c
    if dp[amount] == inf:
        return []
    ans: list[int] = []
    while amount:
        ans.append(pick[amount])
        amount -= pick[amount]
    return ans
```
2. **组合数**（LC 518）：状态含义改成「凑成 `a` 的方法数」，转移改成 `dp[a] += dp[a - c]`，`dp[0] = 1`。外层必须是硬币、内层是金额，这样每种组合只按硬币顺序计一次；`[1,2,5]`、`5` 得到 `4`。外层金额、内层硬币则计的是排列（LC 377）。
```python
def change_ways(coins: list[int], amount: int) -> int:
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
```
3. **BFS**：节点是已凑出的金额，每枚硬币是一条边，第一次到达 `amount` 的层数就是最少枚数，用 `deque` 按层展开并用集合去重。复杂度同样 `O(amount × 硬币数)`，没有渐近优势；适合想要早停（答案很小）时，最坏情况不如 DP 稳定。

**Python 提醒**：`dp = [[0] * n] * m` 这类二维初始化会让所有行共享同一个列表；这里是一维，`[inf] * amount` 复制的是不可变的整数，安全。`min(..., default=...)` 在生成器可能为空时必须给 `default`，否则抛 `ValueError`。
