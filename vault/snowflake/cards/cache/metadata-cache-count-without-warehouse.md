---
id: metadata-cache-count-without-warehouse
node: cache.metadata-cache-pruning-stats
type: qa
tags: [grown]
---
## Q
在 Snowflake 中对一张普通表执行 `SELECT COUNT(*) FROM t`（不带 WHERE），为什么即使虚拟仓库（virtual warehouse，计算集群）处于挂起状态，查询也能几乎瞬间返回？

## A
Snowflake 在云服务层（Cloud Services，负责元数据和优化的常驻服务层）的元数据存储中为每个微分区（micro-partition，不可变的列式数据文件）记录了行数等统计信息。全表行数只需把这些计数相加即可得到，不必打开任何数据文件，所以查询由元数据直接回答，不需要启动仓库，也不消耗仓库计算信用点（credit）。
