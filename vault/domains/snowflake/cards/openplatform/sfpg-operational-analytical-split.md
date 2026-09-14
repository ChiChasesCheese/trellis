---
id: sfpg-operational-analytical-split
node: openplatform.snowflake-postgres
type: qa
tags: [grown]
---
## Q
把在线交易放在 Snowflake Postgres 里，为什么仍然不应该直接在这个 Postgres 实例上跑大范围分析查询？

## A
Postgres 是面向事务的行存引擎，全表扫描和大聚合会占满实例的 CPU、内存和 I/O，与在线事务争抢同一台主节点的资源，导致交易延迟抖动。分析型扫描应该在列式存储和可弹性伸缩的虚拟仓库上执行：把 Postgres 中的数据同步到 Snowflake 表（或开放格式表）后再分析，让交易负载与分析负载在资源上隔离。
