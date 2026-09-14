---
id: storage-search-not-sot
node: storage.search
type: qa
---
## Q
Why is a search cluster the wrong system of record, even though it stores full documents?

## A
- **No real transactions or strong consistency**: writes become visible only after a refresh (near-real-time, ~1s), and multi-document updates aren't atomic.
- **Rebuildability is the design assumption**: mapping changes, analyzer changes, and version upgrades routinely require a full reindex — trivial if the truth lives elsewhere, catastrophic if it doesn't.
- Durability and dedup/versioning stories are weaker than a proper database's.

Treat search as a **derived view**: source of truth in the DB, index rebuilt from it at will.

## Q zh
为什么搜索集群是错误的记录系统，即使它存储完整文档？

## A zh
- **无真正事务或强一致性**：写仅在刷新后变可见（近实时，~1 秒），多文档更新不是原子的。
- **可重建性是设计假设**：映射改变、分析器改变、版本升级日常需要完整重索引——如果真实住在别处是平凡的，如果不是就是灾难性的。
- 持久性和 dedup/版本故事比适当数据库的更弱。

把搜索作为**衍生视图**：DB 中的真实来源，按意愿从它重建索引。
