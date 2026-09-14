---
id: multi-cluster-shared-consistent-view
node: architecture.multi-cluster-shared-data
type: qa
source: snowflake-docs
---
## Q
当两个不同的虚拟仓库（例如一个跑 ETL、一个跑 BI 查询）同时读取同一张表时，它们各自要维护一份数据副本吗？

## A
不需要。因为持久化数据只在共享存储层保存一份，两个虚拟仓库只是各自独立地从这同一份数据上读取所需内容；它们不需要、也不会在本地维护完整的数据副本，读到的都是同一份底层存储的内容。
