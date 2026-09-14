---
id: multi-cluster-shared-independent-compute-one-store
node: architecture.multi-cluster-shared-data
type: qa
source: snowflake-docs
---
## Q
多集群共享数据模型（multi-cluster, shared data）中"多集群"具体指什么？它和只有一个计算集群访问共享存储有何不同？

## A
"多集群"指的是可以同时存在多个相互独立的虚拟仓库（compute cluster），每一个都拥有自己专属的计算资源，互不共享；"共享数据"指的是这些独立的计算集群都挂载在同一份持久化的数据存储之上。也就是说，计算侧允许水平并列出任意多套独立算力，而不是只能有一套计算集群串行地访问这份共享数据。
