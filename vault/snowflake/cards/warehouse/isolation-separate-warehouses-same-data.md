---
id: isolation-separate-warehouses-same-data
node: warehouse.isolation-workload-separation
type: qa
tags: [grown]
---
## Q
夜间 ETL 作业常把 BI 看板拖慢。在 Snowflake 中把 ETL 和 BI 分到两个虚拟仓库（virtual warehouse）为什么能解决，而且不需要复制数据？

## A
每个虚拟仓库是独立的计算集群，不与其他仓库共享 CPU、内存或本地缓存，所以 ETL 仓库再忙也抢不到 BI 仓库的资源。两者读写的是同一份存放在共享存储中的表数据，BI 查询通过元数据读取 ETL 最新提交的版本，因此隔离的只是计算，数据仍只有一份，不需要像传统方案那样为报表另建一套数据副本。
