---
id: tlc-patterns-dp-knapsack-1-signals
node: patterns.dp-knapsack
type: qa
step: 1
---
## Q
**动态规划：背包与计数（Knapsack）｜信号**

什么样的题面是背包问题？0-1 背包、完全背包、计数型分别怎么识别？

## A
背包（Knapsack）模型：有一批"物品"，每个物品有"重量"（占用某种容量），要在**容量限制**下达成某个目标。

**触发信号：**
- 「**能否凑出**某个和」「分成两份和相等」：每个数选或不选，每个数**最多用一次** ⇒ **0-1 背包**（例：LC 416 分割等和子集）。
- 「用**最少**硬币凑出金额」「物品可以**无限次**使用」 ⇒ **完全背包**（例：LC 322 零钱兑换）。
- 「**有多少种**方式凑出」 ⇒ **计数**背包；要区分"组合"（顺序无关）和"排列"（顺序有关）（例：LC 518 零钱兑换 II）。
- 「给每个数加 `+` 或 `-` 使结果为 `target`」 ⇒ 转成"选一部分使其和为某个值"（例：LC 494 目标和）。
- 数据范围：个数几十到两百、总和 `10^3` 到 `10^4`，状态数 `n × 容量` 在 `10^5` 到 `10^6` 量级，表放得下，如 `n <= 30`、每块 `<= 100`、和不超过 `3000`（例：LC 1049 最后一块石头的重量 II）。

**状态**：`dp[i][s]` = 只用前 `i` 个物品、容量（和）恰好为（或至多为）`s` 时的最优值 / 方案数 / 能否。

**三个要素**：
1. 行是物品、列是容量：物品遍历在外层，容量遍历在内层（求组合与 0-1）。
2. 转移读**哪一行**决定每个物品能用一次还是多次：读上一行 `dp[i-1]` 只能用一次，读本行 `dp[i]` 可以重复用。
3. 初值：基础行 `dp[0][0]` 是空集的结果（`True` / `0` / `1`），其余列按"不可达"处理。

**近似信号：**
- 数据范围 `n <= 15` 且要列出方案 ⇒ 回溯（例：LC 77 组合）。
- 容量是 `10^9` 级别 ⇒ 背包表开不下，换思路（贪心 / 数学 / 二分）：状态搜索随容量膨胀，而 `gcd(x, y)` 的判断与容量大小无关（例：LC 365 水壶问题）。
- 物品之间有依赖或次序 ⇒ 不是纯背包：选了父节点就不能选孩子（例：LC 337 打家劫舍 III；高频：LC 198 打家劫舍）。

**例题：** LC 416 分割等和子集

给一个只包含**正整数**的非空数组 `nums`，判断能否把它分成两个子集，使两个子集的元素和相等。`1 <= nums.length <= 200`，`1 <= nums[i] <= 100`。

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                           # 总和是奇数，不可能平分
    n, half = len(nums), total // 2
    # dp[i][j]：只用前 i 个数，能否凑出和恰好为 j
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True                            # 基础行：一个数都不选，只能凑出 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(half + 1):
            dp[i][j] = dp[i - 1][j] or (j >= x and dp[i - 1][j - x])   # 不选第 i 个 / 选第 i 个
    return dp[n][half]                         # 答案格：用全部 n 个数，凑出 half
```

**例题：** LC 322 零钱兑换

给整数数组 `coins`（不同面额的硬币）和整数 `amount`（总金额），返回凑成总金额所需的**最少**硬币个数；凑不出来返回 `-1`。每种硬币的数量无限。`1 <= coins.length <= 12`，`1 <= coins[i] <= 2^31 - 1`，`0 <= amount <= 10^4`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1                      # 哨兵：比任何真实答案都大
    dp = [0] + [inf] * amount             # dp[a] = 凑成金额 a 的最少硬币数
    for c in coins:                       # 完全背包：外层硬币，内层金额正序（同一枚硬币可重复用）
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**例题：** LC 518 零钱兑换 II

给整数数组 `coins`（不同面额的硬币）和整数 `amount`，求能凑成总金额的**硬币组合数**，凑不出返回 `0`；每种面额的硬币有无限个，结果保证在 32 位有符号整数内。`1 <= coins.length <= 300`，`1 <= coins[i] <= 5000`，`coins` 中的值互不相同，`0 <= amount <= 5000`。

```python
def change(amount: int, coins: list[int]) -> int:
    m = len(coins)
    # dp[i][a]：只用前 i 种硬币，凑出金额 a 的组合数
    dp = [[0] * (amount + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1                        # 凑出 0 元只有一种：什么都不拿
    for i, coin in enumerate(coins, 1):
        for a in range(1, amount + 1):
            dp[i][a] = dp[i - 1][a]         # 不用第 i 种
            if a >= coin:
                dp[i][a] += dp[i][a - coin]  # 至少用一枚：剩下的仍可再用第 i 种（同一行）
    return dp[m][amount]
```

**例题：** LC 494 目标和

给非负整数数组 `nums` 和整数 `target`。在每个数前面添加 `+` 或 `-`，再串联成表达式（如 `nums = [2,1]` 可得到 `"+2-1"`）。返回结果等于 `target` 的不同表达式的数目。`1 <= nums.length <= 20`，`0 <= nums[i] <= 1000`，`0 <= sum(nums[i]) <= 1000`，`-1000 <= target <= 1000`。

```python
def find_target_sum_ways(nums: list[int], target: int) -> int:
    total = sum(nums)
    need, odd = divmod(total + target, 2)    # 正数子集之和 P = (total + target) / 2
    if odd or need < 0 or target > total:    # 奇偶不对，或 target 超出 [-total, total]，直接无解
        return 0
    n = len(nums)
    # dp[i][j]：从前 i 个数里选若干个、和恰为 j 的方案数
    dp = [[0] * (need + 1) for _ in range(n + 1)]
    dp[0][0] = 1                             # 一个数都不选，和为 0：一种
    for i, x in enumerate(nums, 1):
        for j in range(need + 1):
            dp[i][j] = dp[i - 1][j]          # 不选第 i 个
            if j >= x:
                dp[i][j] += dp[i - 1][j - x]  # 选第 i 个：只能从上一行转移，所以每个数只用一次
    return dp[n][need]
```

**例题：** LC 1049 最后一块石头的重量 II

有一堆石头，`stones[i]` 是第 `i` 块石头的重量。每一回合从中**任选**两块石头一起粉碎：设重量分别为 `x` 和 `y`（`x <= y`），若 `x == y` 两块都被粉碎；若 `x != y`，重量 `x` 的石头被粉碎，重量 `y` 的石头变成 `y - x`。最后最多剩下一块石头，返回它**最小的可能重量**；没有石头剩下则返回 `0`。`1 <= stones.length <= 30`，`1 <= stones[i] <= 100`。

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

**例题：** LC 77 组合

给两个整数 `n` 和 `k`，返回范围 `[1, n]` 中所有可能的 `k` 个数的组合，顺序任意。`1 <= n <= 20`，`1 <= k <= n`。

```python
def combine(n: int, k: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int) -> None:
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)                       # 还差几个数
        for x in range(start, n - need + 2):       # 剪枝：x 之后剩的数不够就别进
            path.append(x)
            dfs(x + 1)                             # 只往后选，保证组合不重复
            path.pop()
    dfs(1)
    return res
```

**例题：** LC 365 水壶问题

有两个容量分别为 `x` 升和 `y` 升的水壶，水源无限。判断能否用这两个壶**恰好**得到 `target` 升水（两个壶里的水加起来是 `target` 即可）。允许的操作：装满任一水壶；清空任一水壶；把一个壶的水倒进另一个，直到接水的壶满或倒水的壶空。`1 <= x, y, target <= 10^3`。

```python
from math import gcd

def can_measure_water(x: int, y: int, target: int) -> bool:
    return target <= x + y and target % gcd(x, y) == 0
```

**例题：** LC 337 打家劫舍 III

房屋排成一棵二叉树，`root` 是入口。如果**两个直接相连（父子）的房子在同一晚被偷**，就会报警。给定二叉树的 `root`，返回不触发警报时能偷到的最高金额。树的节点数在 `[1, 10^4]`，`0 <= Node.val <= 10^4`。

```python
def rob(root: TreeNode | None) -> int:
    def go(node: TreeNode | None) -> tuple[int, int]:   # (偷 node 时子树最大收益, 不偷 node 时子树最大收益)
        if node is None:
            return 0, 0
        take_l, skip_l = go(node.left)
        take_r, skip_r = go(node.right)
        take = node.val + skip_l + skip_r                # 偷它：孩子必须不偷
        skip = max(take_l, skip_l) + max(take_r, skip_r) # 不偷它：孩子偷不偷都行，各取较大
        return take, skip

    return max(go(root))
```

**例题：** LC 198 打家劫舍

沿街有一排房屋，`nums[i]` 是第 `i` 间房里的现金。相邻的两间房同一晚上都被偷会触发报警，求不触发警报的前提下一晚最多能偷到多少钱。`1 <= nums.length <= 100`，`0 <= nums[i] <= 400`。

```python
def rob(nums: list[int]) -> int:
    skip = take = 0                         # skip：不偷当前房的最优；take：偷当前房的最优
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
```
