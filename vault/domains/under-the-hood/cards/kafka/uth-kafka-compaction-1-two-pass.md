---
id: uth-kafka-compaction-1-two-pass
node: kafka.compaction
type: qa
step: 1
---
## Q
**压实：先建哈希表，再重写段**｜Kafka · 4.0

`cleanup.policy=compact` 的主题怎样做到“每个 key 只留最新值”？清理线程要多少内存？

## A
**结构。** 清理线程先扫“脏”段（上次清理后追加的，不含活动段），把每个 key 的最新偏移量记进哈希表 `SkimpyOffsetMap`；第二趟重写段文件，只保留偏移量不小于表中记录的消息。

**细节。**

- 表项只存 key 的 MD5（16 字节）加 8 字节偏移量，共 24 字节，与 key 多长无关。
- 缓冲区默认 128 MiB（`log.cleaner.dedupe.buffer.size`），装填率上限 0.9，约装 503 万个 key；脏段 key 更多时，这一轮只清一部分。

**为什么。** 用定长哈希代替 key，换来固定的内存上限。

**对应 LeetCode：** LC 706 设计哈希映射 · LC 387 字符串中的第一个唯一字符
