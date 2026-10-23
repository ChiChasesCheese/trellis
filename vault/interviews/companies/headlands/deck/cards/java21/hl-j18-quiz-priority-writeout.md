---
id: hl-j18-quiz-priority-writeout
node: java21.j18-comparators-interfaces
type: qa
step: 23
---
## Q
补全 `Comparator<Order>`，要求价格降序、价格相同按时间升序、时间也相同按 id 升序，并说出各行的作用。

## A
```java
Comparator<Order> byPriority =
    Comparator.comparingLong(Order::px).reversed()
              .thenComparingLong(Order::ts)
              .thenComparingLong(Order::id);
```
`comparingLong(...).reversed()` 先把价格比较反转（降序）；`thenComparingLong(Order::ts)` 在价格相等时按时间升序；`thenComparingLong(Order::id)` 作为最后的唯一兜底，保证全序。`reversed()` 放在 `thenComparing` 之前，只反转价格。
