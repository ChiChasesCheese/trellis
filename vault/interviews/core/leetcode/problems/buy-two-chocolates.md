---
slug: buy-two-chocolates
---
## Q
**LC 2706 购买两块巧克力**｜Easy

整数数组 `prices` 和整数 `money`。恰好买两块巧克力，使剩余的钱非负且尽量多。返回剩余的钱；买不起任意两块时返回 `money`。

## A
**一句话。** 价格最小的两块之和最省钱；够买就返回 `money - 和`，否则原样返回 `money`。

```python
def buy_choco(prices, money):
    a, b = sorted(prices)[:2]        # 最便宜的两块
    left = money - a - b
    return left if left >= 0 else money
```

**复杂度。** 时间 `O(n log n)`（可用一次扫描做到 `O(n)`），空间 `O(n)`。

**易错点。**
- 买不起时返回 `0` 或负数：应返回原来的 `money`。
- 取最贵的两块：要尽量省钱，取最便宜的。

**追问。**
- 怎么做到 `O(n)`？：遍历一次，维护最小值和次小值两个变量。

**同模式。** LC 1 两数之和、LC 1005 K 次取反后最大化的数组和
