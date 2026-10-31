---
id: tlc-partition-array-for-maximum-sum-0-whole
node: p2.partition-array-for-maximum-sum
type: qa
---
## Q
**LC 1043 分隔数组以得到最大和**｜Medium · LC TikTok 近 3 个月热度 62/100（全时段 38）

给整数数组 `arr`，把它分隔成若干段**连续**子数组，每段长度**至多**为 `k`。分隔后，每段中的所有值都变成该段的最大值。求变换后数组元素之和的最大值（测试保证答案在 32 位整数范围内）。

约束：`1 <= arr.length <= 500`，`0 <= arr[i] <= 10^9`，`1 <= k <= arr.length`。

例：`arr = [1,15,7,9,2,5,10], k = 3` → `84`（变成 `[15,15,15,9,10,10,10]`）；`arr = [1,4,1,5,7,3,6,1,9,9,3], k = 4` → `83`；`arr = [1], k = 1` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 线性分段 DP：`dp[i]` 是前 `i` 个元素的最大和；枚举最后一段的长度 `j ≤ k`，这一段贡献 `j × 段内最大值`，从后往前扩段时顺便滚动维护最大值。`O(n·k)`。

**识别。** 「把数组切成连续段，每段按某种规则计价，求总价值最大」是**线性分段 DP**（前缀 DP）的标志：最后一段是什么，决定了转移。段长上限 `k` 给出了转移的枚举范围；`n ≤ 500` 允许 `O(n·k)`、甚至 `O(n^2)`，不需要优化。段的价值 `j × max` 依赖整段，所以必须在枚举段长时增量维护最大值。

**推导。** 暴力：递归枚举每一段的长度，`O(k^n)`。观察：切完前 `i` 个元素后，后面怎么切只取决于 `i`，与前面怎么切无关（无后效性）→ 记忆化 / DP：`dp[i] = max over j in 1..min(k,i) of dp[i-j] + j × max(arr[i-j..i-1])`。每个状态 `k` 种转移，每种转移的段最大值若用 `max(arr[i-j:i])` 要 `O(j)`，总 `O(n·k^2)`；改成从 `j = 1` 逐步增大，`seg_max = max(seg_max, arr[i-j])` 就是 `O(1)`，总 `O(n·k)`。答案是 `dp[n]`。

**简单解法。** 自顶向下记忆化：`best(i)` 是从下标 `i` 起的后缀的最大和，枚举第一段长度，段最大值直接 `max(arr[i:i+j])` 重算。

```python
from functools import cache


def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    n = len(arr)

    @cache
    def best(i: int) -> int:                        # 从下标 i 起的后缀，分隔后的最大和
        if i == n:
            return 0
        ans = 0
        for length in range(1, min(k, n - i) + 1):  # 第一段取 length 个，全变成段内最大值
            ans = max(ans, max(arr[i:i + length]) * length + best(i + length))
        return ans

    return best(0)
```

时间 `O(n * k^2)`（`n * k` 个转移，每个切片求最大 `O(k)`），空间 `O(n)`；`n = 500` 时递归深度 500，低于默认约 1000 层，约束内够用；`n` 更大要改自底向上，并把段最大值改成滚动维护。

最优解：

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

运行：`arr=[1,15,7,9,2,5,10], k=3` → `84`，`arr=[1,4,1,5,7,3,6,1,9,9,3], k=4` → `83`，`arr=[1], k=1` → `1`，`arr=[0,0,0], k=2` → `0`，`arr=[10**9]*500, k=500` → `500000000000`。

**复杂度。** 时间 `O(n·k)`：`n` 个状态，每个状态枚举最后一段的长度至多 `k` 种，滚动最大值使每次转移 `O(1)`；`n = k = 500` 时约 `1.25·10^5` 次转移。空间 `O(n)`。

**拓展优化。**
- 输出具体的分隔方案：多记一个 `choice[i]`（最优的最后一段长度），再从 `n` 往回走：
```python
def partition_plan(arr: list[int], k: int) -> tuple[int, list[int]]:
    n = len(arr)
    dp = [0] + [-1] * n                             # -1：还没有任何方案（元素非负，任何方案都 >= 0）
    choice = [0] * (n + 1)                          # choice[i]：前 i 个元素最优分隔里最后一段的长度
    for i in range(1, n + 1):
        seg_max = 0
        for length in range(1, min(k, i) + 1):
            seg_max = max(seg_max, arr[i - length])
            if dp[i - length] + seg_max * length > dp[i]:
                dp[i] = dp[i - length] + seg_max * length
                choice[i] = length
    lengths: list[int] = []
    i = n
    while i > 0:                                    # 从末尾沿 choice 一段段往回走
        lengths.append(choice[i])
        i -= choice[i]
    return dp[n], lengths[::-1]
```

**易错点。**
- 贪心「每段都取满 `k` 个」：`arr=[1,15,7,9,2,5,10]`, `k=3` 得 `82`（`[1,15,7]` `[9,2,5]` `[10]`），而最优是 `84`（`[1,15,7]` `[9]` `[2,5,10]`）。段边界必须靠 DP 选。
- 段最大值每次用切片 `max(arr[i-j:i])` 重算：结果对，但复杂度升到 `O(n·k^2)`；虽然 `n=500` 仍能过，面试里应当写滚动最大值。
- `dp[i]` 初值为 `0` 而非 `-inf`：此处 `arr[i] >= 0` 且至少有一种转移，所以安全；若值可为负，要用 `-inf` 初始化。
- 下标：`dp` 长度是 `n + 1`，第 `length` 个元素是 `arr[i - length]`（`i` 是前缀长度），写成 `arr[i - length + 1]` 会错位。

**追问。**
- `n` 到 `10^5`、`k` 也很大：`O(n·k)` 不够，需要单调栈 / 凸包技巧（斜率优化）把转移降到摊还 `O(n)` 或 `O(n log n)`；面试里说明思路即可。

**同模式。** LC 139 单词拆分、LC 91 解码方法、LC 132 分割回文串 II、LC 1105 填充书架、LC 410 分割数组的最大值、LC 1335 工作计划的最低难度。
