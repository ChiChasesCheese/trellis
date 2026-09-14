---
id: fdb-enables-stateless-services
node: metadata.foundationdb-role
type: qa
tags: [grown]
---
## Q
为什么说把所有元数据放进 FoundationDB（共享的事务型 KV 存储）是 Snowflake 云服务（Cloud Services）实例可以随意增减、替换的前提？

## A
云服务实例本身不在本地保存权威状态，目录、表版本、事务和权限都读写自同一个 FoundationDB 集群。于是任何一个实例都能处理任何账户的请求；实例崩溃时不会丢失已提交的元数据，新实例启动后直接从存储读取状态即可接手；扩容时增加实例也无需迁移数据。代价是元数据存储处在每次登录、编译和提交的关键路径上，它的可用性和延迟直接决定整个服务的可用性和延迟。
