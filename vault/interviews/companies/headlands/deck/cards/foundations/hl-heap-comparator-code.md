---
id: hl-heap-comparator-code
node: foundations.heap-priority-queue
type: qa
step: 23
---
## Q
订单 `record Order(long id, int price, int qty)`：写出「价格升序、价格相同按 id 升序」的比较器，以及买盘「价格降序、同价 id 小的先出」的 `PriorityQueue`。

## A
```java
Comparator<Order> byPriceThenId =
    Comparator.comparingInt(Order::price).thenComparingLong(Order::id);

Comparator<Order> byPriceDesc =
    Comparator.comparingInt(Order::price).reversed();
PriorityQueue<Order> bids =
    new PriorityQueue<>(byPriceDesc.thenComparingLong(Order::id));
```
放入（id 2, 价 100）、（id 1, 价 100）、（id 3, 价 101），出队顺序：id 3（价 101 最优），然后价 100 里 id 小的 id 1，最后 id 2。

要点：`thenComparingLong` 做平局裁决（先到先得）；降序用 `.reversed()` 或 `Comparator.reverseOrder()`。
