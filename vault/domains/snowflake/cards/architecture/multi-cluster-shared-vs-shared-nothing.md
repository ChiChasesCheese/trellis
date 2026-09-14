---
id: multi-cluster-shared-vs-shared-nothing
node: architecture.multi-cluster-shared-data
type: qa
source: snowflake-docs
---
## Q
在纯粹的无共享（shared-nothing）架构里，加一个新的计算节点为什么往往要重新分片（reshard）数据？Snowflake 的多集群共享数据模型如何避开这个问题？

## A
无共享架构中每个节点各自拥有并只能访问自己那一份数据，扩容意味着把数据重新切分、迁移到新节点上，才能让新节点有活干。Snowflake 把持久化数据集中存放在一份共享的存储仓库里，任何虚拟仓库（compute cluster）都可以直接挂载访问同一份数据，因此新增或调整计算集群时不需要搬动或重新分片任何数据。
