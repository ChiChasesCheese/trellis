---
id: hi-pt-distributed-file-system-9-small-files
node: qb.sd.distributed-file-system.points
type: qa
step: 9
---
## Q
**分布式文件系统 · 小文件**｜追问 · 出自：分布式文件系统 › 深入 5

分布式文件系统平均文件只有 1 MB 时，元数据达到 40 TB。怎么缓解？有什么代价？

## A
**做法。** 把小文件打包进大的容器块，目录项指向 (containerId, offset, length)；文件不可变，打包很简单。

**代价。** 删除要靠容器整理（compaction）才能回收空间。
