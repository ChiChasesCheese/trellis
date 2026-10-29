---
id: uth-kafka-log-index-1-sparse-index
node: kafka.log-index
type: qa
step: 1
---
## Q
**按偏移量找消息：稀疏索引**｜Kafka · 4.0

一个分区的日志切成很多 1 GiB 的段（segment）。消费者要从偏移量 `N` 开始读，Kafka 怎么快速定位？索引是每条消息一项吗？

## A
**结构。** 每段有 `.log` 和 `.index`，文件名是该段首条消息偏移量的 20 位零填充数字。所有段放在跳表（`ConcurrentSkipListMap`）里，`floorEntry(N)` 找到所属段。

**细节。**

- 每追加超过 `index.interval.bytes`（默认 4096）字节，才记一条：4 字节相对偏移 + 4 字节文件位置。
- 查找 = 在索引里二分出不大于 `N` 的最后一项，再从它的文件位置顺序扫 `.log`。

**为什么。** 1 GiB 的段只要 262144 条、2 MiB 索引，能整个 mmap 进内存；逐条消息建索引（按 100 字节一条约 82 MiB）省下的只是不到 4 KB 的顺序扫描。

**对应 LeetCode：** LC 704 二分查找 · LC 981 基于时间的键值存储
