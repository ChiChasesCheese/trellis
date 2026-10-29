---
id: uth-kafka-zero-copy-1-page-cache
node: kafka.zero-copy
type: qa
step: 1
---
## Q
**不自建缓存：页缓存**｜Kafka · 4.0

Kafka broker 为什么不在 JVM 堆里缓存消息，而是把读写都交给操作系统的页缓存（page cache）？

## A
**结构。** 写消息只是追加到文件，数据先留在内核页缓存，由操作系统异步刷盘。`log.flush.interval.messages` 默认是 `Long.MAX_VALUE`：Kafka 自己不主动 `fsync`，持久性靠多副本。

**细节。**

- 设计文档估算：32 GB 的机器页缓存最多 28–30 GB，没有 GC 开销。
- 堆内再缓存一份等于存两遍，Java 对象的内存开销还常翻倍。
- broker 重启后页缓存仍是热的，进程内缓存要重建。

**为什么。** 日志顺序追加、顺序读，内核的预读和回写本就擅长；缓存淘汰（LRU 一类）也一并交给内核。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 460 LFU 缓存
