---
id: sos-search-access-path
node: pruning.search-optimization-service
type: qa
source: snowflake-docs
---
## Q
搜索优化服务（Search Optimization Service, SOS）用来加速点查（point lookup）的核心数据结构叫什么？它记录了什么信息，又是怎样利用这些信息让查询变快的？

## A
这个数据结构叫搜索访问路径（search access path），是一个持续维护的持久化结构，它记录了表的某些列的取值可能出现在哪些微分区（micro-partition）里。查询执行时，引擎查一下这个访问路径，就能把大量不可能包含目标值的微分区直接跳过，从而在只返回一两行结果的高选择性点查上大幅减少需要扫描的分区数量。
