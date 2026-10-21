---
id: amz-in-memory-db-index-maintenance
node: amazon.amz-in-memory-db
type: qa
step: 8
tags: [grown]
---
## Q
在内存数据库里，`WHERE id = 7` 在大表上太慢，怎么加哈希索引？维护时最容易漏什么？

## A
索引是「列值 → 主键集合」的字典，等值查询 O(1)，不再扫全表 O(n)；计划器找到 `AND` 中「有索引的列 = 常量」的一项，取候选主键，再对候选行应用完整的 WHERE。

维护上两处易漏：每个写操作（`insert` / `update` / `delete`）都要同步索引，`update` 先删旧值再加新值；桶空了要删掉，否则索引只增不减。NULL 不进索引，因为它不等于任何值。

```python
bucket.discard(pk)
if not bucket:
    del self.buckets[value]
```
