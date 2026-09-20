---
id: problems-stock-brokerage-price-level-dict-fifo
node: problems.marketplaces.stock-brokerage
type: qa
step: 3
tags: [grown]
---
## Q
股票订单簿要支持四个操作：取最优价、按价格-时间优先取下一张该成交的单、挂新单、**撤单**。用「每侧一个堆（heap）」还是「有序价位表 + 每个价位一个 FIFO」？撤单分别要多少代价？

## A
选**有序价位表 + 每价位一个 FIFO**。分水岭就是撤单——真实市场里撤单笔数远超成交笔数。

**堆**：挂单 O(log n)、取最优 O(1)，但堆不支持按单号删除。只能「惰性删除」：打个已撤标记，等它浮到堆顶再丢。于是堆的大小与**历史报单量**同阶而不是与当前挂单量同阶——一个本该有界的容器在无声地无限增长。

**两级结构**：Python 的 `dict` 从 3.7 起保证保持插入顺序，所以一个价位的 FIFO 直接用 `dict[order_id, Order]`——它既是先进先出队列，又白送 O(1) 的按单号删除（`deque` 从中间删是 O(n)）。价位集合用一条 `list` 加 `bisect` 维持有序：

```python
level = self._levels.get(price)
if level is None:
    level = self._levels[price] = {}
    bisect.insort(self._prices, price)
level[order.id] = order
```

代价：挂到已存在的价位 O(1)，开新价位 O(L)（L = 活跃价位数），取最优价 O(1)（取列表端点），撤单 O(1) 删键、价位空了再 O(L) 摘掉价位。L 是几十到几百而订单数是几万，所以这笔账划算，而且**没有垃圾**。

副作用：同价先后由 `dict` 插入序决定，因此这个设计**不需要序号字段**。
