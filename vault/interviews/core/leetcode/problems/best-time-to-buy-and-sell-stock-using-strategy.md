---
slug: best-time-to-buy-and-sell-stock-using-strategy
---
## Q
**LC 3652 按策略买卖股票的最佳时机**｜Medium

`strategy[i]` 为 `-1` 买、`0` 持有、`1` 卖，利润是 `strategy[i] * prices[i]` 之和。可选恰好 `k`（偶数）个连续天，把前半设为 `0`、后半设为 `1`（最多一次），求最大利润。

## A
**一句话。** 原利润加最大增益；窗口增益 = 后半段价格和 - 窗口内原利润，前缀和 `O(1)` 求，枚举窗口。

```python
def max_profit(prices, strategy, k):
    n, half = len(prices), k // 2
    pp = list(accumulate(prices, initial=0))
    qq = [0, *accumulate(map(mul, prices, strategy))]
    gain = 0                          # 不修改：增益 0
    for i in range(n - k + 1):
        sell = pp[i + k] - pp[i + half]   # 后半段全卖
        old = qq[i + k] - qq[i]
        gain = max(gain, sell - old)
    return qq[n] + gain
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 增益不和 `0` 取最大：不修改也合法，`([5,4,3], [1,1,0], 2)` 会得 `8`，应为 `9`。
- 把前半段也算成卖出：前半是持有，贡献 `0`，`([4,2,8], [-1,0,1], 2)` 会得 `14`，应为 `10`。
- 窗口数写成 `n - k`：漏掉最后一个窗口，`([2,8], [-1,0], 2)` 得 `-2`，应为 `8`。

**追问。**
- 最多改 `m` 次且窗口不重叠？：在增益数组上选 `m` 个不重叠窗口，做 DP。
- 为什么用前缀和而不是每个窗口重算？：重算是 `O(nk)`，前缀和把每个窗口降到 `O(1)`。

**同模式。** LC 121 买卖股票的最佳时机、LC 1423 可获得的最大点数、LC 643 子数组最大平均数 I
