---
id: three-layer-hybrid-architecture
node: architecture.three-layer-model
type: qa
source: snowflake-docs
---
## Q
为什么说 Snowflake 的架构是共享磁盘（shared-disk）与无共享（shared-nothing）架构的混合体？

## A
像共享磁盘架构一样，Snowflake 用一个中心化的数据仓库存放持久化数据，所有计算节点都能访问；但像无共享架构一样，Snowflake 用大规模并行处理（MPP）的计算集群执行查询，集群中每个节点在执行期间把一部分数据缓存到本地磁盘。这样既获得了共享磁盘架构管理简单（数据只有一份、不用手工分片）的好处，又获得了无共享架构在扩展性和性能上的优势。
