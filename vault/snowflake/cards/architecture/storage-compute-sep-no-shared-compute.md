---
id: storage-compute-sep-no-shared-compute
node: architecture.storage-compute-separation
type: qa
source: snowflake-docs
---
## Q
多个虚拟仓库（virtual warehouse）同时运行时，它们的计算资源是如何隔离的？这对故障影响范围意味着什么？

## A
每个虚拟仓库都是一个独立的计算集群，不与其他虚拟仓库共享任何计算资源。因此某个虚拟仓库上的负载峰值、性能问题甚至崩溃，都不会波及其他虚拟仓库的查询性能；而且因为持久化数据本身存放在与计算完全分离的存储层，即便某个虚拟仓库出问题，数据也不会受影响，可以直接换一个新的仓库继续访问同一份数据。
