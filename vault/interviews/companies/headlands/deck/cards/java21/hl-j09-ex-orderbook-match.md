---
id: hl-j09-ex-orderbook-match
node: java21.j09-sequenced-collections
type: qa
step: 24
---
## Q
订单簿撮合循环（买单吃卖盘）怎么用 `firstEntry` / `pollFirstEntry` 实现？空簿怎么处理？部分成交时队头怎么更新？

## A
```java
while (left > 0) {
    var top = asks.firstEntry();                         // 最优卖价；空簿返回 null
    if (top == null || top.getKey() > limit) break;
    Level lv = top.getValue();
    var head = lv.fifo.firstEntry();                     // 该价位排最前的订单（价格-时间优先里的「时间」）
    long fill = Math.min(left, head.getValue());
    if (fill == head.getValue()) {
        lv.fifo.pollFirstEntry();                        // 队头成交完，出队
        if (lv.fifo.isEmpty()) asks.pollFirstEntry();    // 这个价位空了，整档删掉
    } else {
        lv.fifo.put(head.getKey(), head.getValue() - fill);   // 部分成交：put 只改值，位置不变，仍在队头
    }
    left -= fill;
}
```
空簿 `firstEntry()` 返回 `null`，所以先判 `top == null`。
