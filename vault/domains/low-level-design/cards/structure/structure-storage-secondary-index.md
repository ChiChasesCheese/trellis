---
id: structure-storage-secondary-index
node: structure.storage
type: qa
---
## Q
你的存储库存储 `Map<OrderId, Order>` 但 `findByUser(userId)` 被不断调用。你怎样避免 O(n) 扫描，索引引入的正确性陷阱是什么?

## A
在存储库内维护一个**二级索引**:

```java
Map<OrderId, Order> byId;
Map<UserId, Set<OrderId>> byUser;   // 索引持有 id，通过 byId 解决
```

陷阱: 索引和主地图必须一起改变 — 每个 `save`、`delete` 和任何改变索引字段的更新（订单重新分配给另一用户: 从旧集合移除、添加到新的）必须改变两者，在同一个锁/原子操作下。保持索引写**内部**存储库正是为什么存储库边界存在的 — 调用者不能忘记第二次写。
