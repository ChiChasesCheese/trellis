---
id: hl-j18-treeset-drop
node: java21.j18-comparators-interfaces
type: qa
step: 19
---
## Q
`TreeSet<Order>` 用只比较价格的比较器，放入价格相同的两个不同订单，结果如何？为什么？

## A
只保留第一个，后加入的被**静默丢弃**，不报错。实验：价格都是 101 的订单 `#2, #3, #5`，只比价格时 5 个订单在 `TreeSet` 里只剩 **3** 个；完整 tie-break 的剩 **5** 个。

原因：`TreeSet`/`TreeMap`（以及 `PriorityQueue`）判断「同一个元素」**完全靠比较器**（`compare == 0`），不是 `equals`。比较器与 `equals` 不一致会让集合违反 `Set` 的约定。所以订单簿比较器必须是全序，排序一定写全 tie-break。
