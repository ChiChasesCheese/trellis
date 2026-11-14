---
slug: minimum-cost-to-connect-sticks
---
## Q
**LC 1167 连接木棍的最低费用**｜Medium

每次把两根长 `x`、`y` 的木棍接成一根，费用 `x + y`，直到只剩一根，求最小总费用。

## A
**一句话。** 哈夫曼合并：越早合成的木棍会被重复计费越多次，所以每次合并最短的两根，用小根堆。

```python
def connect_sticks(sticks):
    heapify(sticks)
    cost = 0
    while len(sticks) > 1:
        x = heappop(sticks) + heappop(sticks)   # 最短两根
        cost += x
        heappush(sticks, x)
    return cost
```

**复杂度。** 时间 `O(n log n)`，空间 `O(1)`（原地建堆）。

**易错点。**
- 一次排序后从左往右累加：合成的新木棍可能比后面的长，必须放回堆里重排。
- 只有一根时返回它的长度：不需要合并，费用是 `0`。

**追问。**
- 为什么最短两根先合？：每根木棍被计费的次数等于它在合并树中的深度，最短的放最深最省。
- 每次合并 `k` 根（LC 1000 类）？：要补长度为 0 的木棍凑满，或用区间 DP。

**同模式。** LC 1046 最后一块石头的重量、LC 2208 将数组和减半的最少操作次数、LC 1962 移除石子使总数最小
