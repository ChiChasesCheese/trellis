---
id: hl-j18-orderbook-priority
node: java21.j18-comparators-interfaces
type: qa
step: 18
---
## Q
订单簿的买盘优先级是「价高者优先，同价先到者优先」，怎么写比较器？为什么最后要加 id 兜底？

## A
```java
static final Comparator<Order> BUY_PRIORITY = Comparator
        .comparingLong(Order::px).reversed()   // 价高者优先
        .thenComparingLong(Order::ts)          // 同价，先到者优先
        .thenComparingLong(Order::id);         // 再相同按 id，保证全序
```
结果示例：`[#3(101@t1), #5(101@t1), #2(101@t3), #1(100@t5), #4(99@t2)]`；`#3` 和 `#5` 价格、时间都相同，按 id 排，3 在 5 前。

用唯一的 `id` 兜底，使比较器成为**全序**，否则放进 `TreeSet`/`TreeMap` 会丢订单（见下一张卡）。
