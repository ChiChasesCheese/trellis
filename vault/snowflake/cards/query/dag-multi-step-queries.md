---
id: dag-multi-step-queries
node: query.dag-execution-model
type: qa
tags: [grown]
---
## Q
为什么有些 Snowflake 查询在查询画像（Query Profile）中被分成多个“步骤（step）”，而大多数 SELECT 只有一个执行图？举例说明。

## A
有些语句需要按先后顺序执行几个独立的处理阶段，每个阶段各自形成一个算子图，画像里就按步骤展示，可逐步切换查看，每步的最昂贵节点也按该步骤的执行时间计算。例如 `CREATE TABLE ... AS SELECT` 由建表的 DDL 部分和执行 SELECT 写入数据的部分组成，可以是多步画像；普通 SELECT 通常在单个执行图中完成，只有一个步骤。
