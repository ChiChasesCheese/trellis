---
id: dag-no-buffer-pool-no-txn-during-exec
node: query.dag-execution-model
type: qa
tags: [grown]
---
## Q
传统数据库执行查询时要经过 buffer pool（缓冲池）并处理事务并发控制，为什么 Snowflake 的执行引擎可以省掉这两项开销？

## A
查询执行时读取的是编译期确定的一组不可变微分区（micro-partition）文件，这组文件在执行过程中不会被其他事务修改，因此执行期间无需加锁或做事务管理。Snowflake 也不维护传统意义上的 buffer pool：内存直接分配给算子（如哈希表、排序）使用，内存不够时让算子溢出到磁盘，而读过的文件缓存在工作节点的本地磁盘上。
