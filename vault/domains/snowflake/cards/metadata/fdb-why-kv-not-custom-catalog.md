---
id: fdb-why-kv-not-custom-catalog
node: metadata.foundationdb-role
type: qa
tags: [grown]
---
## Q
Snowflake 为什么把目录与事务元数据放进 FoundationDB（一个强一致的分布式事务型键值存储），而不是自研一个专用的目录服务（catalog service）？

## A
元数据需要的是跨多个键的 ACID 事务（例如提交时同时更新表的分区列表和事务状态）、水平扩展、跨可用区复制和故障自动恢复。自研目录服务就得自己实现分布式共识、复制和事务，这些正是最难做对的部分；FoundationDB 已经提供了严格可串行化（serializable）的多键事务和容错复制，Snowflake 只需在其上建模目录对象。这样云服务层的各个服务可以保持无状态，所有状态都落在同一个事务性存储中。
