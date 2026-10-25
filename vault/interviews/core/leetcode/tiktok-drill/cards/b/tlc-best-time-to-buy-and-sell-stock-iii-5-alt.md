---
id: tlc-best-time-to-buy-and-sell-stock-iii-5-alt
node: b.best-time-to-buy-and-sell-stock-iii
type: qa
step: 5
---
## Q
**LC 123 买卖股票的最佳时机 III**｜另一种解法

不用四个状态变量，还有什么思路？它为什么正确，什么时候应该选它而不是状态机？

## A
**思路：前缀 + 后缀分解。** 两笔交易互不重叠，所以一定存在一个分界日 `i`，第一笔完全发生在 `prices[:i+1]` 内，第二笔完全发生在 `prices[i:]` 内（允许某一笔为空）。先从左到右算出 `left[i]` = 只在前 `i+1` 天里做**一笔**交易的最大利润（维护最低价）；再从右到左维护"只在后缀里做一笔"的最大利润，并在每个 `i` 处与 `left[i]` 相加取最大。

```python
def max_profit_split(prices: list[int]) -> int:
    n = len(prices)
    left = [0] * n                         # left[i]：只在 prices[:i+1] 里做一次交易的最大利润
    low = prices[0]
    for i in range(1, n):
        low = min(low, prices[i])
        left[i] = max(left[i - 1], prices[i] - low)
    best = right = 0                       # right：只在 prices[i:] 里做一次交易的最大利润
    high = prices[-1]
    for i in range(n - 1, -1, -1):
        high = max(high, prices[i])
        right = max(right, high - prices[i])
        best = max(best, left[i] + right)  # 在第 i 天分界：前一段加后一段
    return best
```

运行：`[3,3,5,0,0,3,1,4]` → `6`，`[1,2,3,4,5]` → `4`，`[7,6,4,3,1]` → `0`，`[1]` → `0`，`[1,5,2,10]` → `12`，与状态机版本的结果相同。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（`left` 数组）。

**什么时候选哪个。**
- 状态机：`O(1)` 空间，能直接推广到 `k` 笔、冷冻期、手续费，是这一类题的通用做法，面试里优先写。
- 前缀 / 后缀分解：思路最直观，容易向面试官解释正确性，也容易调试（可以单独打印 `left`）；但只适用于"恰好两笔、互不重叠"这种可以按分界线拆开的结构，推广到更多笔会变成区间 DP。
- 两种思路互为检验：写出一个之后，用另一个的思路手算样例，可以快速发现边界错误。

**Python 提醒**：`left[i - 1]` 在 `i = 1` 时指向 `left[0] = 0`，别漏掉 `left` 的初值；反向循环写成 `range(n - 1, -1, -1)`，最后一个下标是 `0` 而不是 `1`，写成 `range(n - 1, 0, -1)` 会漏掉 `i = 0` 的分界。
