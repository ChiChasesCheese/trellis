---
slug: sell-diminishing-valued-colored-balls
---
## Q
**LC 1648 销售价值减少的颜色球**｜Medium

某色球卖出时的价值是此刻剩余的同色球数。卖出 `orders` 个球，求最大总价值，模 `10^9+7`。

## A
**一句话。** 每次卖最贵的：把库存最高的几种颜色按层削平，整层用等差数列求和，最后一层只卖一部分。

```python
def max_profit(inventory, orders):
    inv = sorted(inventory, reverse=True) + [0]
    total = 0
    for i in range(len(inv) - 1):
        w = i + 1              # 前 w 种已削到同一高度 inv[i]
        cur, nxt = inv[i], inv[i + 1]
        layer = w * (cur - nxt)
        if orders >= layer:    # 整层卖完：价值 nxt+1..cur
            total += w * (cur + nxt + 1) * (cur - nxt) // 2
            orders -= layer
        else:
            full, rest = divmod(orders, w)
            total += w * (2 * cur - full + 1) * full // 2
            total += rest * (cur - full)   # 多卖一个的 rest 种
            break
    return total % (10**9 + 7)
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 漏掉最后一层多卖的 `rest * (cur - full)`：`[2,5]`, `orders=4` 得 `12`，应为 `14`。
- 用堆一个个模拟：`orders=10^9` 时超时，必须按层用公式。
- 数组末尾忘了补 `0`：最后一层没法一路卖到价值 `1`。

**追问。**
- 还有别的做法吗？：二分一个阈值 `t`，卖掉所有高于 `t` 的球，剩余订单按价值 `t` 补齐。
- 为什么贪心最贵的对？：卖出价只取决于该色剩余数，先卖高的不会让后面的价值变低。

**同模式。** LC 1642 可以到达的最远建筑、LC 2208 将数组和减半的最少操作次数、LC 1167 连接木棍的最低费用
