---
id: clone-billing-retained-for-clone
node: continuity.clone-storage-billing
type: qa
tags: [grown]
---
## Q
源表删除了大量旧数据（甚至整张表被 DROP），但存储费用几乎没降。如果这张表之前被克隆过，原因可能是什么？

## A
被删除的微分区（micro-partition）如果仍被某个克隆表引用，就不能被物理清除，存储会继续计费，只是归属从源表转到了克隆表名下。在 `TABLE_STORAGE_METRICS` 视图中这部分体现为 `RETAINED_FOR_CLONE_BYTES`。遗忘的旧克隆因此会悄悄长期保留大量本应被清理的数据。
