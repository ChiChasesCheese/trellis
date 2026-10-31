---
id: tlc-best-time-to-buy-and-sell-stock-using-strategy-0-whole
node: c.best-time-to-buy-and-sell-stock-using-strategy
type: qa
---
## Q
**LC 3652 按策略买卖股票的最佳时机**｜Medium · LC TikTok 全时段热度 26/100

给你两个整数数组 `prices` 和 `strategy`：`prices[i]` 是第 `i` 天某股票的价格；`strategy[i]` 是第 `i` 天的交易策略，`-1` 表示买入一单位，`0` 表示持有，`1` 表示卖出一单位。再给你一个**偶数**整数 `k`，你可以对 `strategy` 进行**最多一次**修改：选择 `strategy` 中恰好 `k` 个连续元素，把前 `k / 2` 个设为 `0`（持有），后 `k / 2` 个设为 `1`（卖出）。利润定义为所有天数中 `strategy[i] * prices[i]` 的总和。返回可以获得的最大可能利润。没有预算或持股数量的限制，所有买入卖出都可行。`2 <= prices.length == strategy.length <= 10^5`，`1 <= prices[i] <= 10^5`，`-1 <= strategy[i] <= 1`，`2 <= k <= prices.length`，`k` 是偶数。例：`prices = [4,2,8], strategy = [-1,0,1], k = 2` → `10`（修改 `[0, 1]` 得 `[0,1,1]`）；`prices = [5,4,3], strategy = [1,1,0], k = 2` → `9`（不修改最好）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 利润 = 原利润 + 这次修改带来的增益；对每个长度为 `k` 的窗口，增益 = 窗口后半段的价格和 - 窗口内原来的 `strategy * price` 之和，用前缀和 `O(1)` 求出，枚举所有窗口取最大增益（至少为 0，即不修改），`O(n)`。

**识别。** 「最多一次、改一个定长连续窗口、窗口内按固定规则重写」：改动只影响窗口内的值，先算全局基础值，再单独算每个窗口的增益，窗口求和用前缀和。

**推导。** 窗口 `[i, i + k)` 修改后：前半段每天贡献 `0`，后半段每天贡献 `prices[j]`（因为 `1 * prices[j]`）。窗口原来的贡献是 `Σ strategy[j] * prices[j]`。所以增益 = `Σ_{j=i+k/2}^{i+k-1} prices[j] - Σ_{j=i}^{i+k-1} strategy[j] * prices[j]`，两个区间和都可以用前缀和得到。答案 = 原利润 + `max(0, 所有窗口的最大增益)`。

**简单解法。** 同样的「基础利润 + 最大增益」，但每个窗口的两个区间和直接用切片求和，不建前缀和。

```python
def max_profit_window_sum(prices: list[int], strategy: list[int], k: int) -> int:
    half = k // 2
    base = sum(p * s for p, s in zip(prices, strategy))
    best_gain = 0                                # 不修改：增益为 0
    for i in range(len(prices) - k + 1):         # 窗口 [i, i+k)
        old = sum(p * s for p, s in zip(prices[i:i + k], strategy[i:i + k]))   # 窗口原来的利润
        new = sum(prices[i + half:i + k])        # 修改后：后半段全部卖出
        best_gain = max(best_gain, new - old)
    return base + best_gain
```

`O(nk)`，`k` 接近 `n / 2` 时约 `2.5 * 10^9` 步，超时；每个窗口重复求和，正是前缀和要消掉的。

最优解：

```python
from itertools import accumulate


def max_profit(prices: list[int], strategy: list[int], k: int) -> int:
    n, half = len(prices), k // 2
    pp = list(accumulate(prices, initial=0))                         # pp[i]：prices 前 i 天之和
    qq = list(accumulate((p * s for p, s in zip(prices, strategy)), initial=0))   # 原策略的利润前缀和
    best_gain = 0                                # 不修改：增益为 0
    for i in range(n - k + 1):                   # 窗口 [i, i+k)
        sell_part = pp[i + k] - pp[i + half]     # 修改后：后半段全部卖出，收入 = 价格和
        old_part = qq[i + k] - qq[i]             # 修改前这一窗口的利润
        best_gain = max(best_gain, sell_part - old_part)
    return qq[n] + best_gain
```

运行：`([4,2,8], [-1,0,1], 2)` → `10`，`([5,4,3], [1,1,0], 2)` → `9`；`([1,1], [-1,-1], 2)` → `1`，`([3,1,4,1], [1,-1,1,-1], 4)` → `5`。

**复杂度。** 时间 `O(n)`，空间 `O(n)`（两个前缀和数组）。

**拓展优化。**
- 滑动窗口，把空间降到 `O(1)`：窗口右移一格时增益只增减四项。

```python
def max_profit_sliding(prices: list[int], strategy: list[int], k: int) -> int:
    n, half = len(prices), k // 2
    base = sum(p * s for p, s in zip(prices, strategy))
    gain = sum(prices[half:k]) - sum(p * s for p, s in zip(prices[:k], strategy[:k]))   # 窗口 [0, k) 的增益
    best = max(0, gain)
    for i in range(n - k):                       # 窗口从 [i, i+k) 右移到 [i+1, i+k+1)
        gain += prices[i + k] - prices[i + half]                     # 后半段：进来 i+k，出去 i+half
        gain += prices[i] * strategy[i] - prices[i + k] * strategy[i + k]   # 原利润部分：出去 i，进来 i+k
        best = max(best, gain)
    return base + best
```

**易错点。**
- 不和 `0` 取最大：不修改也是合法选择，`([5,4,3], [1,1,0], 2)` 每个窗口增益都为负，会得到 `8`，正确是 `9`。
- 把窗口前半段也算进卖出：前半段是「持有」，贡献 `0`，只有后半段是 `prices`；多算前半段会让 `([4,2,8], [-1,0,1], 2)` 得到 `14`，正确是 `10`。
- 窗口数写成 `n - k`：漏掉最后一个窗口，`([2,8], [-1,0], 2)` 得到 `-2`，正确是 `8`。

**追问。**
- 最多修改 `m` 次且窗口不重叠：增益数组上选 `m` 个不重叠窗口，用 DP。
- `k` 不要求偶数、前后半段比例可变：增益公式里把 `half` 换成相应的分界点。

**同模式。** LC 121 买卖股票的最佳时机、LC 1423 可获得的最大点数、LC 643 子数组最大平均数 I、LC 209 长度最小的子数组、LC 2461 长度为 K 子数组中的最大和。
