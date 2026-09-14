---
id: hybrid-vs-standard-table-choice
node: openplatform.hybrid-tables-oltp
type: qa
source: snowflake-docs
---
## Q
什么样的查询该放在混合表（hybrid table），什么样的查询该放在标准表？二者在锁粒度上的差异如何影响选择？

## A
混合表适合：按 ID 基于索引读取少量记录的随机点读，以及高并发的随机写（INSERT、UPDATE、MERGE），例如数千个并行 worker 更新同一张工作流状态表、通过 API 低延迟提供预计算聚合。它使用行级锁，并发写不互相阻塞。标准表是列式微分区、分区或表级锁，擅长批量加载、大扫描和聚合。常见做法是在同一数据库里混用两种表，各存适合的数据。
