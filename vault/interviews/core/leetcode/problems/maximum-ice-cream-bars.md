---
slug: maximum-ice-cream-bars
---
## Q
**LC 1833 雪糕的最大数量**｜Medium

`costs[i]` 是第 `i` 支雪糕的价格，现金 `coins`，求最多买几支；要求用计数排序。价格 `≤ 10^5`。

## A
**一句话。** 买得最多就先买最便宜的；价格值域小，用桶按价格从低到高扫，每个价格能买 `min(剩余支数, 钱 // 价格)`。

```python
def max_ice_cream(costs, coins):
    cnt = [0] * (max(costs) + 1)   # 计数排序：下标是价格
    for c in costs:
        cnt[c] += 1
    ans = 0
    for price, k in enumerate(cnt):
        if price == 0 or k == 0:
            continue
        take = min(k, coins // price)
        if take == 0:              # 这个价都买不起，更贵的也不行
            break
        ans += take
        coins -= take * price
    return ans
```

**复杂度。** 时间 `O(n + U)`，空间 `O(U)`，`U = max(costs)`。

**易错点。**
- 一支一支地买：同价格可以一次 `coins // price` 算完。
- 钱不够就 `continue`：价格递增，买不起当前价就买不起后面的，可以直接停。

**追问。**
- 不限计数排序？：`sorted(costs)` 后前缀和，二分找最多能买到的位置。
- 为什么贪心对？：任何方案把一支贵的换成没买的便宜的，钱不增、支数不变。

**同模式。** LC 75 颜色分类、LC 1122 数组的相对排序、LC 274 H 指数
