---
id: pruning-zonemap-vs-btree-index
node: pruning.min-max-zone-maps
type: qa
source: snowflake-docs
---
## Q
min/max zone map 剪枝和传统数据库里显式创建、显式维护的 B 树二级索引相比，运维方式上的根本区别是什么？

## A
B 树索引需要用户显式创建、占用额外存储、并在每次 DML 后同步维护，维护成本会随写入量线性增长。而 zone map 的 min/max 元数据是数据加载/插入时自动为每个微分区收集的，不需要用户定义、也不需要单独的索引结构去维护——它是数据本身自带的统计信息，天然覆盖每一张表的每一列。
