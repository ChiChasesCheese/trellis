---
id: structure-storage-secondary-index
node: structure.storage
type: qa
---
## Q
Your repo stores `Map<OrderId, Order>` but `findByUser(userId)` is called constantly. How do you avoid the O(n) scan, and what's the correctness trap the index introduces?

## A
Maintain a **secondary index** inside the repository:

```java
Map<OrderId, Order> byId;
Map<UserId, Set<OrderId>> byUser;   // index holds ids, resolve via byId
```

The trap: the index and primary map must change **together** — every `save`, `delete`, and any update that changes the indexed field (order reassigned to another user: remove from old set, add to new) must update both, under the same lock/atomic operation. Keeping index writes *inside* the repository is exactly why the repository boundary exists — callers can't forget the second write.


## Q zh
你的存储库存储 `Map<OrderId, Order>` 但 `findByUser(userId)` 被不断调用。你怎样避免 O(n) 扫描，索引引入的正确性陷阱是什么?

## A zh
在存储库内维护一个**二级索引**:

```java
Map<OrderId, Order> byId;
Map<UserId, Set<OrderId>> byUser;   // 索引持有 id，通过 byId 解决
```

陷阱: 索引和主地图必须一起改变 — 每个 `save`、`delete` 和任何改变索引字段的更新（订单重新分配给另一用户: 从旧集合移除、添加到新的）必须改变两者，在同一个锁/原子操作下。保持索引写**内部**存储库正是为什么存储库边界存在的 — 调用者不能忘记第二次写。
