---
id: multi-cluster-shared-vs-shared-disk-bottleneck
node: architecture.multi-cluster-shared-data
type: qa
source: snowflake-docs
---
## Q
纯粹的共享磁盘（shared-disk）架构容易在什么地方出现瓶颈？Snowflake 的做法与之相比多了哪一步？

## A
共享磁盘架构里所有计算节点直接对同一块磁盘发起 I/O，磁盘的带宽和 I/O 能力会成为所有节点共同竞争的瓶颈。Snowflake 虽然也用一份集中的共享存储作为持久化数据源，但采用大规模并行处理（MPP）执行查询时，参与计算的每个节点会先把自己需要处理的那部分数据缓存到本地，之后的计算主要针对本地缓存进行，从而避免所有节点同时对中心存储反复发起 I/O 竞争。
