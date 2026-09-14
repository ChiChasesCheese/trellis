---
id: object-storage-central-repo-plus-local-cache
node: storage.object-storage-backend
type: qa
source: snowflake-docs
---
## Q
Snowflake 把持久化数据放在所有计算节点都能访问的中央云存储上，而不是每个节点的本地磁盘上。这带来什么收益？它又用什么手段弥补远程读取的性能损失？

## A
收益来自共享磁盘（shared-disk）式的中央数据仓库：数据只有一份，任何计算节点都能读取，不需要手工分片，也不必在节点之间搬运或复制数据。弥补手段借鉴无共享（shared-nothing）架构：查询由 MPP（大规模并行处理）计算集群执行，集群中每个节点在本地保存一部分数据，从而减少对中央存储的反复远程读取。
