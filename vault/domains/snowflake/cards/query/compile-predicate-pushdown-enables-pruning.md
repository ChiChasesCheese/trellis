---
id: compile-predicate-pushdown-enables-pruning
node: query.compilation-pipeline
type: qa
tags: [grown]
---
## Q
为什么 `WHERE d >= '2026-01-01'` 能在 Snowflake 编译期剪掉大量微分区（micro-partition），而 `WHERE d >= (SELECT MAX(d) FROM cfg)` 即使子查询结果是常量也不能用于剪枝？

## A
优化阶段会把过滤谓词下推到表扫描，并在编译期拿字面常量与每个微分区元数据中的列取值范围比较，直接排除不可能匹配的分区，生成要扫描的文件列表。子查询的值要到执行时才算出来，编译期无法用它与分区元数据比较，所以 Snowflake 不会基于含子查询的谓词剪枝。若过滤值可以提前确定，先单独查出来再把常量写进查询，才能享受剪枝。
