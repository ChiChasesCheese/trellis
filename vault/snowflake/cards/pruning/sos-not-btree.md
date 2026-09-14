---
id: sos-not-btree
node: pruning.search-optimization-service
type: qa
source: snowflake-docs
---
## Q
搜索访问路径（search access path）和传统关系型数据库里的 B 树二级索引相比，本质上是同一类结构吗？它加速的是哪一层面的操作？

## A
不是。B 树索引直接定位到具体的行位置，供运行时做行级查找和回表；而搜索访问路径记录的是“哪些值可能出现在哪些微分区里”，它加速的是微分区这一层面的剪枝判断——帮助引擎跳过不相关的微分区，而不是替代微分区内部的扫描或直接定位到某一行。
