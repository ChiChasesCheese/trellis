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
- LC 473 火柴拼正方形（装箱：回溯加剪枝，位掩码 DP 也可）

**完全背包（最少 / 能否）**
- LC 322 零钱兑换
- LC 139 单词拆分（"物品"是词典里的词，目标是拼出整个字符串）

**以步数 / 次数为状态的计数**
- LC 887 鸡蛋掉落
- LC 70 爬楼梯（完全背包的特例：物品是步长 1、2）

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

**例题：** LC 473 火柴拼正方形

`matchsticks[i]` 是火柴长度，每根恰好用一次、不可折断，判断能否拼成正方形；`1 <= matchsticks.length <= 15`，`matchsticks[i] <= 10^8`。

```python
def makesquare(matchsticks: list[int]) -> bool:
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True)
    if sticks[0] > side:
        return False
    sides = [0] * 4
    def dfs(i: int) -> bool:
        if i == len(sticks):
            return True
        tried: set[int] = set()
        for j in range(4):
            if sides[j] + sticks[i] > side or sides[j] in tried:
                continue
            tried.add(sides[j])
            sides[j] += sticks[i]
            if dfs(i + 1):
                return True
            sides[j] -= sticks[i]
        return False
    return dfs(0)
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

**例题：** LC 887 鸡蛋掉落

`k` 个鸡蛋、`n` 层楼，求最坏情况下确定临界楼层的最少操作次数；`1 <= k <= 100`，`1 <= n <= 10^4`。

```python
def super_egg_drop(k: int, n: int) -> int:
    dp = [[0] * (k + 1)]
    while dp[-1][k] < n:
        m = len(dp)
        dp.append([0] * (k + 1))
        for j in range(1, k + 1):
            dp[m][j] = dp[m - 1][j - 1] + dp[m - 1][j] + 1
    return len(dp) - 1
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
