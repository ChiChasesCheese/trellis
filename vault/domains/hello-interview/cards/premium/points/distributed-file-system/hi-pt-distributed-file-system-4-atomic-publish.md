---
id: hi-pt-distributed-file-system-4-atomic-publish
node: qb.sd.distributed-file-system.points
type: qa
step: 4
---
## Q
**分布式文件系统 · 原子发布**｜必会 · 出自：分布式文件系统 › 深入 1

分布式文件系统的 putFile 要写多个数据块、块列表和目录项。写入顺序是什么？崩溃在中途会怎样？

## A
**顺序。** 先写不可变的东西，最后翻一个指针：块（三副本落盘）→ 块列表（键为 fileId）→ 在父目录所在分片的事务里写目录项，仅当名字不存在。

**提交点。** 目录项是唯一提交点；之前任何一步失败，文件对外不可见，已写的块成为孤儿，之后被回收。
