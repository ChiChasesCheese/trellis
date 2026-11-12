---
slug: maximum-spending-after-buying-items
---
## Q
**LC 2931 购买物品的最大开销**｜Hard

`m` 个商店的物品各自按价值非递增排好，每天只能买某店最右边（最便宜）的未买物品，第 `d` 天花费 `价值 × d`。求买完所有物品的最大总开销。

## A
**一句话。** 全体物品升序排序，第 `d` 天买第 `d` 小的：越贵越晚买，且顺序总是合法。

```python
def max_spending(values):
    items = sorted(v for row in values for v in row)
    return sum(d * v for d, v in enumerate(items, 1))
```

**复杂度。** 时间 `O(mn log(mn))`，空间 `O(mn)`。

**易错点。**
- 排序方向写反：贵的先买，示例 1 得 `165`，应为 `285`。
- 天数从 `0` 数起：第一天乘数是 `1`，`enumerate` 要从 `1` 开始。

**追问。**
- 为什么升序总是合法？：每个商店内右边的更便宜，升序天然先买右边。
- 求最小开销呢？：降序不合法（只能先买最右边的），要在合法顺序里取最小，是另一道题。

**同模式。** LC 455 分发饼干、LC 1029 两地调度、LC 1402 做菜顺序
