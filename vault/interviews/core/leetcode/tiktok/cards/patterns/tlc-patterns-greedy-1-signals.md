---
id: tlc-patterns-greedy-1-signals
node: patterns.greedy
type: qa
step: 1
---
## Q
**贪心（Greedy）｜信号**

什么样的题面该想到贪心？怎样判断贪心成立，什么时候要退回 DP？

## A
贪心（Greedy）= 每一步都选当前看起来最好的，且这个选择**不会让后面的选择变差**，最终得到全局最优。它通常比 DP 快（`O(n)` 或 `O(n log n)`）、空间小。

**触发信号：**
- 问**最大 / 最小值**，并且题目有明显的"排序后一次扫描"结构：区间调度、会议室、任务安排（例：LC 452 用最少数量的箭引爆气球）。
- 「**能否到达**」「最少几步到达」，每个位置有一个"可达范围"：跳跃游戏 LC 55、45（例：LC 45 跳跃游戏 II）。
- 「**环形**路线，累计量不能为负」：加油站 LC 134（例：LC 134 加油站）。
- 「**字典序最小 / 数值最大**」，从高位到低位逐位决定：最大交换 LC 670、移掉 K 位数字 LC 402（例：LC 670 最大交换）。
- 「括号序列里有通配符」：只维护未匹配数的范围（例：LC 678 有效的括号字符串）。

**怎样判断贪心成立：**
1. **交换论证**（Exchange Argument）：假设存在一个最优解不含你的贪心选择，把它改成含该选择，结果不会更差。
2. 自己找**反例**：用 3 到 5 个元素的小输入手算贪心与暴力，两者不同则贪心不成立。
3. 如果当前选择会改变后面能选的集合（占用了资源、挡住了更好的组合），多半不是贪心。

**什么时候退回 DP：**
- 硬币面值 `[1, 3, 4]` 凑 `6`：贪心取最大面额得 `4+1+1`（3 枚），最优 `3+3`（2 枚）⇒ 凑数类必须 DP；平方数同理，`12` 贪心得 `9+1+1+1`，最优 `4+4+4`（例：LC 279 完全平方数）。
- 打家劫舍取最大的房子会挡住两侧 ⇒ DP（例：LC 198 打家劫舍）。

**近似信号：**
- 要列出所有方案 ⇒ 回溯（例：LC 78 子集）。
- 选与不选互相影响 ⇒ 背包 DP：按余数记录最优和（例：LC 1262 可被三整除的最大和）。

**例题：** LC 452 用最少数量的箭引爆气球

墙面（XY 平面）上贴着一些球形气球，`points[i] = [xstart, xend]` 表示第 `i` 个气球的水平直径在 `xstart` 到 `xend` 之间，不知道确切的 `y` 坐标。弓箭从 `x` 轴沿竖直方向射出：在坐标 `x` 射出的箭，会引爆所有满足 `xstart <= x <= xend` 的气球；箭的数量不限，射出后可以无限前进。求引爆所有气球所需的**最少**弓箭数。`1 <= points.length <= 10^5`，`points[i].length == 2`，`-2^31 <= xstart < xend <= 2^31 - 1`。

```python
from math import inf
from operator import itemgetter


def find_min_arrow_shots(points: list[list[int]]) -> int:
    arrows = 0
    last = -inf                            # 上一支箭的位置
    for start, end in sorted(points, key=itemgetter(1)):   # 按右端点排序
        if start > last:                   # 上一支箭够不着：新射一支，射在 end（尽量靠右）
            arrows += 1
            last = end
    return arrows
```

**例题：** LC 45 跳跃游戏 II

给长度为 `n` 的非负整数数组 `nums`，初始站在下标 `0`。`nums[i]` 表示从 `i` 出发最多向后跳 `nums[i]` 格（可以跳 `0` 到 `nums[i]` 之间的任意格数，且不越界）。求到达下标 `n - 1` 的**最少跳跃次数**；保证一定能到达。`1 <= nums.length <= 10^4`，`0 <= nums[i] <= 1000`。

```python
def jump(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):      # 最后一格不用再跳，所以不扫它
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                # 当前这一跳的范围走完了，必须再跳一次
            jumps += 1
            cur_end = farthest          # 下一层的右边界
    return jumps
```

**例题：** LC 134 加油站

环形路线上有 `n` 个加油站，第 `i` 个加油站有汽油 `gas[i]` 升。你的油箱容量无限，从第 `i` 个加油站开往第 `i + 1` 个加油站要消耗 `cost[i]` 升汽油（最后一个站开往第 `0` 站）。你从其中一个加油站出发，开始时油箱为空。如果能按顺序绕环路行驶一周，返回出发的加油站编号，否则返回 `-1`；如果存在解，保证它**唯一**。`n == gas.length == cost.length`，`1 <= n <= 10^5`，`0 <= gas[i], cost[i] <= 10^4`。

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

**例题：** LC 670 最大交换

给一个非负整数 `num`，至多交换其中任意两位数字一次，返回能得到的最大值。`0 <= num <= 10^8`。

```python
def maximum_swap(num: int) -> int:
    digits = list(str(num))
    last = {d: i for i, d in enumerate(digits)}   # 每个数字最后一次出现的下标（后写覆盖前写）
    for i, d in enumerate(digits):
        for big in "9876543210":                  # 从最大的数字开始找
            if big <= d:
                break                             # 已经没有比 d 更大的了，这一位不用换
            if last.get(big, -1) > i:             # 右边有更大的数字：换最右边的那个
                digits[i], digits[last[big]] = digits[last[big]], digits[i]
                return int("".join(digits))
    return num
```

**例题：** LC 678 有效的括号字符串

给一个只含 `'('`、`')'` 和 `'*'` 三种字符的字符串 `s`，判断它是否有效。有效的条件：每个 `'('` 都有对应的 `')'`，每个 `')'` 都有对应的 `'('`，`'('` 必须在对应的 `')'` 之前；`'*'` 可以当作单个 `')'`、单个 `'('` 或空串。`1 <= s.length <= 100`，`s[i]` 只能是 `'('`、`')'`、`'*'`。

```python
def check_valid_string(s: str) -> bool:
    lo = hi = 0                        # 还没配对的 '(' 数量的可能区间 [lo, hi]
    for ch in s:
        lo += 1 if ch == '(' else -1   # '*' 当 ')' 或 ')' 都让 lo 减一
        hi += 1 if ch != ')' else -1   # '*' 当 '(' 或 '(' 都让 hi 加一
        if hi < 0:                     # 即使全当 '(' 也配不上这个 ')'
            return False
        lo = max(lo, 0)                # 区间下界不能为负：多出来的 '*' 当空串
    return lo == 0                     # 0 在区间里，说明存在一种取法恰好配平
```

**例题：** LC 279 完全平方数

给整数 `n`，返回和为 `n` 的**完全平方数的最少数量**（完全平方数是某个整数的平方，如 1、4、9、16；同一个可以用多次）。`1 <= n <= 10^4`。

```python
from math import inf, isqrt


def num_squares(n: int) -> int:
    dp = [0] + [inf] * n                    # dp[i]：和为 i 的最少完全平方数个数
    for i in range(1, n + 1):
        dp[i] = 1 + min(dp[i - j * j] for j in range(1, isqrt(i) + 1))   # 枚举最后一个平方数 j²
    return dp[n]
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

**例题：** LC 78 子集

给一个整数数组 `nums`，其中元素**互不相同**，返回它所有可能的子集（幂集）。解集不能包含重复的子集，可以按任意顺序返回。`1 <= nums.length <= 10`，`-10 <= nums[i] <= 10`。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []

    def dfs(start: int) -> None:
        res.append(path[:])                 # 每个节点都是一个子集：进来先记一份快照
        for i in range(start, len(nums)):   # 只往后选，保证同一个子集不会按不同顺序出现两次
            path.append(nums[i])
            dfs(i + 1)
            path.pop()                      # 回溯：撤销选择

    dfs(0)
    return res
```

**例题：** LC 1262 可被三整除的最大和

给整数数组 `nums`，从中选出一些元素（可以一个都不选，和为 `0`），使它们的和能被 `3` 整除，返回这个最大和。`1 <= nums.length <= 4 * 10^4`，`1 <= nums[i] <= 10^4`。

```python
def max_sum_div_three(nums: list[int]) -> int:
    n = len(nums)
    NEG = -(10 ** 18)                          # 「这个余数凑不出来」
    # dp[i][r]：只用前 i 个数、和模 3 等于 r 时的最大和
    dp = [[NEG] * 3 for _ in range(n + 1)]
    dp[0][0] = 0                               # 空集：和为 0，余数 0
    for i, x in enumerate(nums, 1):
        for r in range(3):
            dp[i][r] = max(dp[i - 1][r],                         # 不选 x
                           dp[i - 1][(r - x) % 3] + x)           # 选 x：上一个余数是 (r - x) % 3
    return dp[n][0]
```
