---
id: access-history-write-lineage
node: security.data-lineage-and-access-history
type: qa
tags: [grown]
---
## Q
执行 `CREATE TABLE t2 AS SELECT a, b + c AS d FROM t1` 之后，怎样知道 t2.d 这一列的数据是从哪里来的？

## A
`ACCESS_HISTORY` 对写操作（CTAS、INSERT … SELECT、MERGE 等）还会记录 `OBJECTS_MODIFIED`，其中包含列级血缘（column lineage）：目标列 t2.d 的 `directSources` 和 `baseSources` 指向源列 t1.b 和 t1.c。把这些记录串起来就能从任意一列向上游追溯来源、向下游找出受影响的列，用于影响分析（改源表会波及谁）和敏感数据流向追踪。
