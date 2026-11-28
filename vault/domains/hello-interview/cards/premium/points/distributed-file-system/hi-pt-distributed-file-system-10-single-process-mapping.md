---
id: hi-pt-distributed-file-system-10-single-process-mapping
node: qb.sd.distributed-file-system.points
type: qa
step: 10
---
## Q
**分布式文件系统 · 内存文件系统的对应**｜追问 · 出自：分布式文件系统 › 取舍与追问

单进程的内存文件系统（目录节点里放名字到子节点的字典）搬到分布式后，目录树、空间分配、崩溃安全写各自变成什么？

## A
**目录树。** 变成有序键值库里 (dirId, name) 的键；目录项的互斥从一把锁变成分片内的事务。

**空间分配。** 空闲链表变成放置服务。

**崩溃安全写。** 本地"先写临时文件再改名"，变成先写块和块列表、最后原子提交目录项。
