---
id: sfpg-compute-model-contrast
node: openplatform.snowflake-postgres
type: qa
tags: [grown]
---
## Q
Snowflake Postgres 实例的计算模型与 Snowflake 虚拟仓库（virtual warehouse）有什么根本不同？这带来什么取舍？

## A
虚拟仓库是存算分离的无状态计算：数据在对象存储里，仓库可随时挂起、秒级扩缩、多集群横向扩展，适合突发的分析负载。Postgres 实例是有状态的数据库服务器：单个主节点负责写入并持有本地存储与缓冲，需要持续运行来服务在线请求，扩容主要靠换更大规格（纵向扩展）和只读副本分担读请求。取舍是：Postgres 提供完整的事务语义和稳定低延迟，但不具备仓库那种按需挂起与弹性。
