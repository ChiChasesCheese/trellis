---
id: datastream-inherits-governance
node: ingestion.datastream-kafka-compatible
type: qa
tags: [grown]
---
## Q
与数据先停留在外部 Kafka 集群里相比，经由 Datastream 写入的数据在治理上有什么不同？

## A
数据直接写成 Snowflake 表，因此自动继承平台已有的能力：用基于角色的访问控制（RBAC）统一授权、记录血缘（lineage），并可用时间旅行（Time Travel）查询或恢复历史数据。在外部 Kafka 中，主题的访问控制、审计和保留策略需要在另一套系统里单独维护，治理是割裂的。
