---
slug: maximum-total-importance-of-roads
---
## Q
**LC 2285 道路的最大总重要性**｜Medium

`n` 个城市分别赋值 `1..n`（各不相同），道路的重要性是两端值之和。求所有道路重要性之和的最大值。

## A
**一句话。** 总和 = 每个城市的值 × 它的度数之和，度数大的城市分配大的值（排序不等式）。

```python
def maximum_importance(n, roads):
    deg = [0] * n
    for a, b in roads:
        deg[a] += 1
        deg[b] += 1
    deg.sort()                 # 度数小的配小值
    return sum(d * v for v, d in enumerate(deg, 1))
```

**复杂度。** 时间 `O(n log n + m)`，空间 `O(n)`。

**易错点。**
- 按道路贪心分配：每个城市的值会在它所有道路上重复计入，看的是度数。
- `enumerate` 从 0 开始：值是 `1..n`，要 `enumerate(deg, 1)`。

**追问。**
- 为什么大配大最好？：两个城市交换值，若度数大的拿了小值，交换后总和增加（度数差 × 值差）`>= 0`。
- 度数范围小？：计数排序，`O(n + m)`。

**同模式。** LC 274 H 指数、LC 1402 做菜顺序、LC 1589 所有排列中的最大和
