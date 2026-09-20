---
id: problems-stock-brokerage-feed-and-shrinking-containers
node: problems.marketplaces.stock-brokerage
type: qa
step: 8
tags: [grown]
---
## Q
股票交易系统加「盘口行情（top of book）推送给订阅者」这一关时，怎么证明设计是可扩展的？推送该在锁内还是锁外？这个系统里哪些容器必须会缩小？

## A
**可扩展的证据是：加行情推送没有动撮合的任何一行。** 新增的只有一个不可变事件类和门面上的 `subscribe`。

事件要**自带订阅者需要的全部内容**（买一价量、卖一价量、最新成交价、时刻），订阅者读事件就够，不必回头去问撮合服务要数据——那等于绕过它的锁去读一份正在被改的状态。

**快照在锁内生成（必须一致），推送在锁外进行**：订阅者是外部代码，握着撮合锁调它，一个慢订阅者就能让全场停摆。

```python
def _publish(self, event: TopOfBook) -> None:
    with self._lock:
        subscribers = tuple(self._subscribers)
    for subscriber in subscribers:
        subscriber(event)
```

三个必须会缩小的容器，每个都要有明确的出口：

1. **价位表**——价位上最后一张单被摘走时，价位本身立刻从两张表里一起删掉。
2. **订单索引**——终结的单靠一个 `purge_terminal_orders_before(cutoff)` 定期清出；没有它，索引随报单量无限增长。
3. **订阅者表**——`subscribe` 返回一个**退订函数**，把退订手段和订阅一起交出去。

成交流水是故意只增的账（它记单号而不是订单引用，所以订单被清掉后流水仍然完整），真实系统把它流式写出去，内存里只留当日。
