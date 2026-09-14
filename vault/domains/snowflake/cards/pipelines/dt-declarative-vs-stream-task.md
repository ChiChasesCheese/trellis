---
id: dt-declarative-vs-stream-task
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
过去要让一张汇总表保持新鲜，需要手写流（Stream）+ 任务（Task）+ MERGE。动态表（dynamic table）用什么方式替代这些？

## A
动态表是声明式的：只需给出一条 SELECT 查询（表里应该有什么）和一个 `TARGET_LAG`（数据最多允许落后多久）。Snowflake 解析查询、识别它读取的基表、登记刷新，并持续监控基表变化、自动调度刷新，使结果保持在目标延迟之内；不需要编写编排代码、管理流的偏移量或任务调度。只要逻辑能表达成一条 SELECT，就可以考虑用动态表。
