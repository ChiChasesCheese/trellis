---
id: tlc-patterns-dp-knapsack-8-problems
node: patterns.dp-knapsack
type: qa
step: 8
---
## Q
**动态规划：背包与计数｜本组用到背包或计数 DP 的题**

按变形分类，这个题组里哪些题属于背包或计数型 DP？

## A
**0-1 背包（能否 / 方案数）**
- LC 416 分割等和子集

**完全背包（最少 / 能否）**
- LC 322 零钱兑换
- LC 139 单词拆分（"物品"是词典里的词，目标是拼出整个字符串）
- LC 518 零钱兑换 II（高频）

**以步数 / 次数为状态的计数**
- LC 70 爬楼梯（完全背包的特例：物品是步长 1、2）
- LC 746 使用最小花费爬楼梯（高频）

**数位计数**
- LC 902 最大为 N 的数字组合

提示：先问"每个物品用几次"决定方向，再问"求最优 / 能否 / 方案数"决定转移和初值，最后问"顺序算不算"决定循环嵌套。

**例题：** LC 416 分割等和子集

只含正整数的数组 `nums`，判断能否分成两个和相等的子集；`1 <= nums.length <= 200`，`1 <= nums[i] <= 100`。

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    n, half = len(nums), total // 2
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(half + 1):
            dp[i][j] = dp[i - 1][j] or (j >= x and dp[i - 1][j - x])
    return dp[n][half]
```

**例题：** LC 322 零钱兑换

`coins` 是面额（每种数量无限），求凑成 `amount` 的最少硬币数，凑不出返回 `-1`；`coins.length <= 12`，`amount <= 10^4`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1
    dp = [0] + [inf] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**例题：** LC 139 单词拆分

判断字符串 `s` 能否拆成字典 `wordDict` 中的若干单词（可重复使用）；`s.length <= 300`，`wordDict.length <= 1000`，单词长度 `<= 20`。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    max_len = max(map(len, words))
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 70 爬楼梯

每次爬 `1` 或 `2` 阶，求爬到第 `n` 阶的方法数；`1 <= n <= 45`。

```python
def climb_stairs(n: int) -> int:
    prev, cur = 1, 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur
    return cur
```

**例题：** LC 902 最大为 N 的数字组合

给升序的数字字符数组 `digits`（每个数字可重复使用），求能拼出的、不大于 `n` 的正整数个数；`digits.length <= 9`，`1 <= n <= 10^9`。

```python
from bisect import bisect_left
def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    s, size = str(n), len(digits)
    total = sum(size ** length for length in range(1, len(s)))
    for i, ch in enumerate(s):
        total += bisect_left(digits, ch) * size ** (len(s) - 1 - i)
        if ch not in digits:
            return total
    return total + 1
```

**例题：** LC 518 零钱兑换 II

硬币面额数组 `coins`（每种数量无限）和总金额 `amount`，返回凑成 `amount` 的**组合数**，凑不出返回 `0`；`1 <= coins.length <= 300`，`0 <= amount <= 5000`。

```python
def change(amount: int, coins: list[int]) -> int:
    m = len(coins)
    dp = [[0] * (amount + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i, coin in enumerate(coins, 1):
        for a in range(1, amount + 1):
            dp[i][a] = dp[i - 1][a]
            if a >= coin:
                dp[i][a] += dp[i][a - coin]
    return dp[m][amount]
```

**例题：** LC 746 使用最小花费爬楼梯

`cost[i]` 是从第 `i` 级台阶向上爬要付的费用，付费后可爬一级或两级，起点可选下标 `0` 或 `1`，求到达楼梯顶部（下标 `len(cost)`）的最低花费；`2 <= cost.length <= 1000`。

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    two_back = one_back = 0
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    return one_back
```
