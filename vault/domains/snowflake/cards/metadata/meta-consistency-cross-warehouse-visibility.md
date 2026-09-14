---
id: meta-consistency-cross-warehouse-visibility
node: metadata.metadata-scaling-consistency
type: qa
tags: [grown]
---
## Q
ETL 仓库刚提交了一批 INSERT，紧接着 BI 仓库上发起的查询能看到这批数据吗？为什么两个独立的虚拟仓库（virtual warehouse）之间不需要同步缓存？

## A
能看到。表由哪些微分区（micro-partition）组成、当前是哪个版本，都记录在一个账户内所有仓库共用的强一致元数据存储中；提交成功就意味着新版本已写入这份元数据。任何仓库上随后开始的查询在编译时都从同一处读取最新已提交版本，因此不存在“某个集群还拿着旧目录”的问题，也不需要在仓库之间做缓存失效或数据同步。
