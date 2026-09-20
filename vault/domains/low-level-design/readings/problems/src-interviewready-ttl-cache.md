---
nodes: [problems.components.ttl-cache]
url: https://github.com/InterviewReady/Low-Level-Design/tree/main/distributed-cache
tags: [no-archive]
---
# InterviewReady/Low-Level-Design — distributed-cache

值得读：Java，把缓存放进分布式语境（一致性哈希、数据源接入、超时与重试）来设计。
它对"缓存背后接一个数据源"的抽象比本题解完整——`DataSource` 是一等公民，
读穿透、写回、超时都在接口上写明，可以拿来想清楚本题的 `get_or_load` 再往前一步长什么样。
分歧在重心：它讲网络与拓扑，不讲"进程内一个类怎么管住自己的内存"，
因此没有到期索引、没有墓碑压实，也没有单飞（single-flight）这条防缓存踩踏的闸；
类层次也是 Java 味的多层接口，Python 里只有一个实现的接口是负担而不是扩展点。
仓库无 LICENSE 文件，故只链接不摘录。
