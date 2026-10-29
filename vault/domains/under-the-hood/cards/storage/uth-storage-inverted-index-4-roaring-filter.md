---
id: uth-storage-inverted-index-4-roaring-filter
node: storage.inverted-index
type: qa
step: 4
---
## Q
**过滤器缓存：Roaring 位图**｜Lucene · 10.5

查询里的过滤条件（如 `status:active`）会缓存成一个文档集合。怎么存才既省内存又能快速求交？

## A
**结构。** 查询缓存（`LRUQueryCache`）：命中文档占比达到 1% 用普通位图（`FixedBitSet`），更稀疏的用 `RoaringDocIdSet`。

**细节。**

- Roaring 把文档号空间切成每块 65536 个，每块独立选格式：命中不超过 4096 个用有序 `short[]`；超过 65536 − 4096 个，存“没命中的”那份 `short[]`；其余用位图。
- 完全没命中的块不分配空间。

**为什么。** 4096 个 `short` 正好 8 KB，和 65536 位的位图一样大：稀疏时数组更小，稠密时位图更小，4096 是两者相等的临界点。

**对应 LeetCode：** LC 349 两个数组的交集 · LC 705 设计哈希集合
