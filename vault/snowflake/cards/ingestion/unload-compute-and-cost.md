---
id: unload-compute-and-cost
node: ingestion.unload-export
type: qa
tags: [grown]
---
## Q
`COPY INTO <location>` 消耗什么资源？导出到另一个云区域的 S3 桶，除了计算费还可能产生什么费用？

## A
卸载本质上是执行一条查询并写出文件，使用当前会话的虚拟仓库（virtual warehouse），按仓库运行时间消耗信用点（credit）；查询越复杂、数据量越大，所需时间越长。若目标云存储与 Snowflake 账户位于不同区域或不同云平台，数据跨区域或跨云流出还会产生数据传输（egress）费用，因此大批量导出应尽量写到同区域的存储。
