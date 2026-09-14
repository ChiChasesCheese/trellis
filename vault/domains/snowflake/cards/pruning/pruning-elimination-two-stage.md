---
id: pruning-elimination-two-stage
node: pruning.partition-elimination
type: qa
source: snowflake-docs
---
## Q
Snowflake 执行一条带过滤条件的查询时，剪枝分几个阶段完成，每个阶段作用在什么粒度上？

## A
分两个阶段：第一阶段是分区消除（partition elimination），在编译期把需要扫描的对象从“全表所有微分区”缩小到“存活的微分区集合”；第二阶段是在这些存活的微分区内部，按列（column）继续剪枝——因为每个微分区内部数据按列独立存储，所以只需要扫描查询实际引用到的那些列，未被引用的列即使在存活分区里也不会被读取。
