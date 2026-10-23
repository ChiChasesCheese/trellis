---
id: hl-j18-chain-code
node: java21.j18-comparators-interfaces
type: qa
step: 6
---
## Q
用 `Comparator` 组合子写：先按价格降序，价格相同按时间升序，时间也相同按 id 升序（三个字段都是 `long`，`Order` 是 record）。

## A
```java
Comparator<Order> c = Comparator
        .comparingLong(Order::px).reversed()   // 价格降序
        .thenComparingLong(Order::ts)          // 同价按 ts 升序
        .thenComparingLong(Order::id);         // 还相同按 id，保证全序
```
读法：1. 按价格比；2. 反过来（降序）；3. 价格相同按 ts；4. 还相同按 id。用基本类型版本避免装箱。
