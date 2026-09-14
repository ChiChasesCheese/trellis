---
id: hybrid-same-engine-atomic-txn
node: openplatform.hybrid-tables-oltp
type: qa
source: snowflake-docs
---
## Q
把 OLTP 数据放在混合表（hybrid table）里、分析数据放在标准表里，相比“外部 OLTP 数据库 + Snowflake 数仓”的架构，在跨表查询和事务上有什么好处？

## A
混合表运行在同一个 Snowflake 服务中：查询同样在云服务层编译优化，在同一引擎和虚拟仓库上执行。因此混合表可以与标准表直接 JOIN，无需联邦查询（federation）；可以在混合表与其他 Snowflake 表之间执行一个原子事务，无需自己编排两阶段提交（2PC）；数据治理等平台功能开箱即用。
