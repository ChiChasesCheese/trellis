---
id: hybrid-row-store-async-copy
node: openplatform.hybrid-tables-oltp
type: qa
source: snowflake-docs
---
## Q
向 Snowflake 混合表（hybrid table，面向低延迟随机读写的行存表类型）写入一行后，数据存在哪里？大范围分析扫描为什么不会拖慢在线事务？

## A
写入直接落入行存储（row store），行存是混合表的主存储，负责基于索引的低延迟点读写。数据随后被异步复制到对象存储中，部分数据还可能以列式格式缓存在仓库上；大扫描可以读这些副本，与正在进行的操作型负载隔离。用户只对逻辑上的一张表写 SQL，由查询优化器决定从行存还是列式副本读取。
