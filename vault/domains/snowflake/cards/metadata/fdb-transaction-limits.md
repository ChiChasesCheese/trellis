---
id: fdb-transaction-limits
node: metadata.foundationdb-role
type: qa
tags: [grown]
---
## Q
FoundationDB 本身对单个事务和单个值有哪些硬性限制？这对在它之上构建 Snowflake 元数据层意味着什么？

## A
FoundationDB 的事务最长约 5 秒、写入总量上限约 10 MB，单个值上限约 100 KB（键约 10 KB）。因此元数据层不能把一个大对象（例如拥有海量微分区的表的完整文件列表）塞进一个值，也不能用一个长时间运行的事务包住整个 SQL 语句：需要把大对象拆成许多小的键值，并把一次提交分解为短小的元数据事务，SQL 层面的长事务语义由 Snowflake 在其上自行实现。
