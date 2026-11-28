---
id: hi-pt-distributed-file-system-3-namespace-sharding
node: qb.sd.distributed-file-system.points
type: qa
step: 3
---
## Q
**分布式文件系统 · 命名空间分片**｜必会 · 出自：分布式文件系统 › 深入 1

分布式文件系统的目录树放在分片键值库里。分片键该选路径哈希，还是别的？怎样让列目录和创建文件都高效？

## A
**选择。** 键为 (tenantId, dirId, name)，做范围分区，每片三副本、用 Raft 复制。

**好处。** 同一目录的目录项相邻，列目录是一次范围扫描；putFile 和 createDirectory 是单片事务；大目录按大小自动分裂。

**不用路径哈希。** 列目录要散射到所有分片，改目录名要改整棵子树的键。
