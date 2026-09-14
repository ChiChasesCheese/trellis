---
id: metadata-cache-pruning-before-scan
node: cache.metadata-cache-pruning-stats
type: qa
tags: [grown]
---
## Q
为什么 Snowflake 把微分区统计信息放在云服务层的元数据存储里，而不是只写在各个数据文件的头部让仓库自己去读？

## A
剪枝（pruning，跳过不可能包含匹配行的分区）发生在查询编译阶段、仓库开始读文件之前。如果统计信息只存在数据文件里，判断一个分区能否跳过就得先从对象存储把它的头部读出来，一张有上百万个分区的表光这一步就要大量远程 I/O。把统计集中缓存在元数据层，编译器可以直接在内存级的元数据上完成剪枝，仓库只拿到需要真正扫描的分区清单。
