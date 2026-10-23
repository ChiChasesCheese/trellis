---
id: hl-hc05-matching-loop
node: problems.hc05-market-order-book
type: qa
step: 8
---
## Q
价格-时间优先的撮合循环怎么写？限价单与市价单怎么复用同一份循环？

## A
```java
while (left > 0) {
    var top = opp.firstEntry();                    // 对面最优档
    if (top == null) break;
    long px = top.getKey();
    boolean crosses = side == Side.BUY ? px <= limit : px >= limit;
    if (!crosses) break;
    var level = top.getValue();
    var maker = level.fifo.firstEntry().getValue(); // 队头
    long fill = Math.min(left, maker.qty);
    out.add(new Trade(takerId, maker.id, side, px, fill));   // 成交价 = maker 价
    left -= fill; maker.qty -= fill; level.total -= fill;
    if (maker.qty == 0) {
        level.fifo.pollFirstEntry(); byId.remove(maker.id);
        if (level.fifo.isEmpty()) opp.pollFirstEntry();      // 档空连价位一起删
    }
}
```
- 买单交叉条件：最低卖价 ≤ 限价；卖单：最高买价 ≥ 限价。
- 终止性：每轮要么吃光 maker（被移除）要么吃光新单；每个成交 O(1)，每吃光一档 O(log L)，满足价格-时间优先。
- 循环后若 `left > 0`：限价单挂簿（`Rested`），市价单作废（`Cancelled(id, remaining)`）。
- **市价单 = 限价设成「无穷」**（买 `Long.MAX_VALUE`，卖 `0`），`crosses` 永远为真，避免写两份循环（迟早改漏一份）。
- 部分成交的 maker 留在队头，只是数量减少；价位空了必须从 `TreeMap` 删，否则 `bestBid` 返回空档。

手算：卖盘 101:[#1×5,#2×3]、102:[#3×4]。`LIMIT 4 BUY 101 6` → `Trade(4,1,BUY,101,5)`、`Trade(4,2,BUY,101,1)`，#2 剩 2 仍在队头。
