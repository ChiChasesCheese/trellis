---
id: mp-metadata-collected-at-load
node: storage.micro-partition-metadata
type: qa
source: snowflake-docs
---
## Q
Snowflake 的微分区（micro-partition）元数据是什么时候产生的？为什么这个时机很关键？

## A
在数据插入/加载到表中的过程中，每创建一个微分区，Snowflake 就同时收集并记录它的元数据（包括聚簇相关信息）。因为元数据在写入时就已就绪，查询时无需再做任何统计扫描，便可直接依据它跳过无关的微分区，这是剪枝能“免费”发生的前提。
