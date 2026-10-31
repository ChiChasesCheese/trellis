---
id: tlc-patterns-dp-linear-1-signals
node: patterns.dp-linear
type: qa
step: 1
---
## Q
**动态规划：线性与状态机（DP）｜信号**

什么样的题面该想到线性 DP？怎样用"状态、转移、初值、遍历顺序"四步把题目翻译成递推？

## A
动态规划（Dynamic Programming）适用于：问题能拆成**重叠的子问题**，且大问题的最优解由小问题的最优解组合而成（**最优子结构**）。

**触发信号：**
- 问**最大 / 最小值**、**方案个数**、**能否做到**，并且暴力枚举是指数级（回溯会超时）（例：LC 322 零钱兑换；高频：LC 518 零钱兑换 II）。
- 一维序列，"到第 `i` 个为止"的答案由前面的答案推出：爬楼梯 LC 70、打家劫舍 LC 198、最大子数组和 LC 53（例：LC 70 爬楼梯；高频：LC 746 使用最小花费爬楼梯）。
- **选与不选**的决策、**相邻元素互相约束**（例：LC 198 打家劫舍）。
- 每一天有几种"状态"（持有 / 不持有股票）：买卖股票 LC 121、122（例：LC 188 买卖股票的最佳时机 IV）。
- 把序列切成若干段，每段有代价：分隔数组以得到最大和 LC 1043（例：LC 1043 分隔数组以得到最大和）。
- 数据范围 `n` 到 `10^3` 到 `10^5`，要求 `O(n)` 或 `O(n k)`（例：LC 188 买卖股票的最佳时机 IV；高频：LC 1043 分隔数组以得到最大和）。

**四步法：**
1. **状态**：`dp[i]` 表示什么？（"前 `i` 个""以第 `i` 个结尾"）
2. **转移**：`dp[i]` 由哪些更小的状态得到？
3. **初值**：最小的状态是多少？
4. **顺序**：算 `dp[i]` 时它依赖的状态必须已算好。

只依赖前一两项时，把数组压成两三个变量（滚动变量），空间 `O(1)`。

**近似信号：**
- 要**列出所有**方案 ⇒ 回溯（例：LC 46 全排列）。
- 每步局部最优就全局最优 ⇒ 贪心（LC 55、134）（例：LC 134 加油站）。
- 不要求最优、只要连续段和 ⇒ 前缀和（例：LC 974 和可被 K 整除的子数组）。

**例题：** LC 322 零钱兑换

硬币面额数组 `coins`（`1 <= coins.length <= 12`）和总金额 `amount`（`0 <= amount <= 10^4`），每种硬币数量无限，求凑成 `amount` 所需的最少硬币数，凑不出返回 `-1`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1                      # 哨兵：比任何真实答案都大
    dp = [0] + [inf] * amount             # dp[a] = 凑成金额 a 的最少硬币数
    for c in coins:                       # 完全背包：外层硬币，内层金额正序（同一枚硬币可重复用）
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**例题：** LC 70 爬楼梯

每次爬 1 或 2 级台阶，爬到第 `n` 级（`1 <= n <= 45`）有多少种不同的方法。

```python
def climb_stairs(n: int) -> int:
    prev, cur = 1, 1                   # f(0) = 1（站着不动算一种），f(1) = 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur    # f(k) = f(k-1) + f(k-2)：最后一步迈 1 阶或 2 阶
    return cur
```

**例题：** LC 198 打家劫舍

沿街房屋存放金额为非负整数数组 `nums`（`1 <= nums.length <= 100`，`0 <= nums[i] <= 400`），相邻两间不能同时偷，求能偷到的最高金额。

```python
def rob(nums: list[int]) -> int:
    skip = take = 0                         # skip：不偷当前房的最优；take：偷当前房的最优
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
```

**例题：** LC 1043 分隔数组以得到最大和

把数组 `arr`（`1 <= arr.length <= 500`）分成若干长度至多为 `k` 的连续段，每段的所有值都变成该段最大值，求变换后元素和的最大值。

```python
def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)                  # dp[i]：前 i 个元素分隔后的最大和
    for i in range(1, n + 1):
        seg_max = 0
        for length in range(1, min(k, i) + 1):    # 枚举最后一段的长度
            seg_max = max(seg_max, arr[i - length])   # 滚动维护这一段的最大值
            dp[i] = max(dp[i], dp[i - length] + seg_max * length)
    return dp[n]
```

**例题：** LC 188 买卖股票的最佳时机 IV

数组 `prices`（`1 <= prices.length <= 1000`）是每天股价，最多完成 `k` 笔交易（`1 <= k <= 100`），不能同时持有多笔，求最大利润。

```python
from math import inf
def max_profit(k: int, prices: list[int]) -> int:
    n = len(prices)
    buy = [[-inf] * (k + 1) for _ in range(n + 1)]    # 第 0 天不可能有货：-inf
    sell = [[0] * (k + 1) for _ in range(n + 1)]      # 第 0 天没做过交易：收益 0
    for i, p in enumerate(prices, 1):
        for j in range(1, k + 1):
            buy[i][j] = max(buy[i - 1][j], sell[i - 1][j - 1] - p)   # 继续拿着 / 今天开第 j 笔
            sell[i][j] = max(sell[i - 1][j], buy[i - 1][j] + p)      # 继续空仓 / 今天卖掉
    return sell[n][k]
```

**例题：** LC 46 全排列

给定不含重复数字的数组 `nums`（`1 <= nums.length <= 6`），返回它的所有全排列，顺序不限。

```python
def permute(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    def backtrack(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # 换回去恢复现场
    backtrack(0)
    return result
```

**例题：** LC 134 加油站

环路上有 `n` 个加油站（`1 <= n <= 10^5`），第 `i` 站有汽油 `gas[i]`，开往下一站耗油 `cost[i]`，油箱无限、起始为空。返回能绕一圈的出发站编号，不存在返回 `-1`，若有解则唯一。

```python
def can_complete_circuit(gas: list[int], cost: list[int]) -> int:
    total = tank = start = 0
    for i, (g, c) in enumerate(zip(gas, cost)):
        diff = g - c                        # 在 i 站净得多少油
        total += diff
        tank += diff
        if tank < 0:                        # 从 start 出发走不到 i+1：start..i 都不能当起点
            start, tank = i + 1, 0
    return start if total >= 0 else -1      # 总油量够，从最后一次重置的位置出发一定可行
```

**例题：** LC 974 和可被 K 整除的子数组

整数数组 `nums`（`1 <= nums.length <= 3 * 10^4`，可含负数）和整数 `k`（`2 <= k <= 10^4`），求元素和可被 `k` 整除的非空连续子数组个数。

```python
from collections import Counter
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})                  # 前缀和模 k 的出现次数；空前缀的余数是 0
    prefix = ans = 0
    for x in nums:
        prefix = (prefix + x) % k           # Python 的 % 对负数也返回 [0, k)，不用再补 + k
        ans += seen[prefix]                 # 以当前位置结尾、余数相同的前缀每个对应一个合法子数组
        seen[prefix] += 1
    return ans
```

**例题：** LC 518 零钱兑换 II

给整数数组 `coins`（不同面额的硬币）和整数 `amount`，求能凑成总金额的**硬币组合数**，凑不出返回 `0`；每种面额的硬币有无限个，结果保证在 32 位有符号整数内。`1 <= coins.length <= 300`，`1 <= coins[i] <= 5000`，`coins` 中的值互不相同，`0 <= amount <= 5000`。

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

整数数组 `cost`，`cost[i]` 是从第 `i` 级台阶向上爬需要支付的费用。支付后可以向上爬**一级或两级**。你可以选择从下标 `0` 或下标 `1` 的台阶出发。返回到达楼梯顶部（下标 `cost.length`，最后一级之后的位置）的最低总花费。`2 <= cost.length <= 1000`，`0 <= cost[i] <= 999`。

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    two_back = one_back = 0
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    return one_back
```
