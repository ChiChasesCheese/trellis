---
id: hl-j18-comparing-boxing
node: java21.j18-comparators-interfaces
type: qa
step: 14
---
## Q
`Comparator.comparing(Order::px)` 与 `comparingLong(Order::px)` 在性能上有什么区别？

## A
`comparing(Order::px)` 的键是 `Long` 装箱对象，每次比较两次装箱（小值有缓存，大值要分配）；`comparingLong` 直接比 `long`。

**热路径用基本类型版本**：`comparingInt` / `comparingLong` / `comparingDouble`、`thenComparingInt/Long/Double`。
