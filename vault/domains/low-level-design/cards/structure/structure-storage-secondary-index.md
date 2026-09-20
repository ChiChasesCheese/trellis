---
id: structure-storage-secondary-index
node: structure.storage
type: qa
step: 3
---
## Q
仓储内部是 `Dict[OrderId, Order]`，但 `find_by_user(user_id)` 被频繁调用，怎样避免每次 O(n) 扫描？引入索引之后最容易踩的正确性陷阱是什么？

## A
在仓储内部维护一个**二级索引**：

```python
self._by_id: dict[OrderId, Order] = {}
self._by_user: dict[UserId, set[OrderId]] = {}
```

`_by_user` 只存 id，真正的数据仍然通过 `_by_id` 取。

陷阱：主表和索引必须**一起**改——每次 `save`、`delete`，以及任何会改变被索引字段的更新（订单被重新分配给另一个用户：要从旧用户的集合里移除，再加进新用户的集合），都必须同时更新两张表，并且在同一把锁/同一次原子操作下完成。把索引的读写限制在仓储**内部**，正是仓储这个边界存在的意义——调用方不可能忘记同步写第二张表，因为调用方根本碰不到它。
