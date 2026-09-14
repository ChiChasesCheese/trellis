---
id: isolation-what-is-not-isolated
node: warehouse.isolation-workload-separation
type: qa
tags: [grown]
---
## Q
ETL 和 BI 已经跑在不同的虚拟仓库（virtual warehouse）上，为什么 ETL 的 MERGE 仍可能让另一个仓库上对同一张表的 UPDATE 卡住？仓库隔离到底没隔离什么？

## A
仓库隔离的是计算资源，不隔离数据层面的并发控制。对同一张表的 UPDATE、DELETE、MERGE 需要基于表的最新版本串行提交，无论语句来自哪个仓库，都要等待对方的锁释放。只读查询则读取已提交的快照，不会被写入阻塞。此外，所有仓库共用同一个云服务（Cloud Services）与元数据层。所以要避免跨仓库的写冲突，得在作业调度上错开对同一张表的写入，而不是再加仓库。
