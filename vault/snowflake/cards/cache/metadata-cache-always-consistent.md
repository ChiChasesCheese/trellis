---
id: metadata-cache-always-consistent
node: cache.metadata-cache-pruning-stats
type: qa
tags: [grown]
---
## Q
结果缓存会因数据变化而失效，那用于剪枝的元数据统计会不会在表刚被 INSERT 或 UPDATE 后变得过时、导致 COUNT(*) 返回旧值？

## A
不会。微分区（micro-partition）是不可变的：每次 DML 都生成新分区，并在同一次提交中把新分区连同其统计信息写入元数据、把被替换的旧分区标记为移除。统计信息与表版本原子地一起提交，所以任何查询看到的表版本和它的统计永远一致，不存在需要单独失效或刷新的陈旧期。
