---
slug: water-and-jug-problem
---
## Q
**LC 365 水壶问题**｜Medium

容量 `x`、`y` 的两个水壶，水源无限，可装满、清空、互相倒。能否让两壶水量之和恰好为 `target`？

## A
**一句话。** 裴蜀定理：能量出的水量恰是 `gcd(x, y)` 的倍数，且不超过 `x + y`。

```python
def can_measure_water(x, y, target):
    return target <= x + y and target % gcd(x, y) == 0
```

**复杂度。** 时间 `O(log min(x, y))`，空间 `O(1)`。

**易错点。**
- 漏掉 `target <= x + y`：`x=1, y=2, target=4` 会错答 `True`。
- 只判断 `target` 是不是 `x`、`y`、`x+y`、`|x-y|` 之一：`(7, 11, 3)` 是 `True`。

**追问。**
- 不记得数学结论怎么办？：BFS，节点是 `(a, b)`，可达状态约 `2(x+y)` 个。
- 要输出倒水步骤？：BFS 时记录父状态和操作。

**同模式。** LC 1250 检查「好数组」、LC 1071 字符串的最大公因子、LC 780 到达终点
