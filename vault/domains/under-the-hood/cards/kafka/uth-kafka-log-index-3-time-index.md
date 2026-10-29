---
id: uth-kafka-log-index-3-time-index
node: kafka.log-index
type: qa
step: 3
---
## Q
**时间索引与预分配的索引文件**｜Kafka · 4.0

按时间戳查消息（`offsetsForTimes`）怎样串起两个索引？为什么活动段的 `.index` 文件大小永远是 10485760 字节？

## A
**结构。** `.timeindex` 是第二张稀疏索引，每项 12 字节（8 字节时间戳 + 4 字节相对偏移），和 `.index` 同时追加。

**细节。**

- 先在 `.timeindex` 二分出不晚于目标时间的偏移量，再用 `.index` 换成文件位置，最后顺序扫 `.log`。
- 索引文件新建时就按 `segment.index.bytes`（10 MiB）预分配，向下取整到项大小的整数倍：`.index` 是 10485760，`.timeindex` 是 10485756；段滚动时才截成实际大小。

**为什么。** 预分配的 mmap 追加写不用扩文件；代价是 `ls` 看到的大小不是真实用量。

**对应 LeetCode：** LC 981 基于时间的键值存储 · LC 1146 快照数组
