---
id: oop-bidirectional-association
node: oop.relationships
type: qa
---
## Q
`Order` 持有 `Customer`，`Customer` 又持有 `List<Order>`。这种双向关联会出什么问题，有哪两种有纪律的做法？

## A
没有任何机制保证两端一致：`order.setCustomer(c)` 而没有 `c.getOrders().add(order)`，就留下一条半截链接，而且此后每一条修改路径都必须记得同时改两边。它还制造了一个**引用环**，会让朴素的 `equals`/`hashCode`/`toString` 无限递归。

- **做法 A —— 只留一个拥有方**：只存在 `Customer.addOrder(order)`，由它自己设置反向指针，并且是*唯一*的修改入口。`Order.setCustomer` 降为包级私有或直接删掉。
- **做法 B —— 干脆去掉反向指针**：只保留 `Order → Customer` 这一个引用，"某个客户的所有订单"由仓储里的索引来回答。

机考里默认选 B：一条能推导出来的可导航链接，比一条必须靠人维护的便宜。
