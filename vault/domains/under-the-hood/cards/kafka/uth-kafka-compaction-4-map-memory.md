---
id: uth-kafka-compaction-4-map-memory
node: kafka.compaction
type: qa
step: 2
---
## Q
**哈希表要多大：每个 key 只占 24 字节**｜Kafka · 4.0

压实时，清理线程用一张哈希表（`SkimpyOffsetMap`）记每个 key 的最新偏移量。key 很长怎么办？这张表最多装多少个 key？

## A
**结构。** 表项不存 key 本身，只存 key 的 MD5（把任意长度的内容算成固定 16 字节“指纹”的哈希函数）加 8 字节偏移量，共 24 字节，和 key 多长无关。

**细节。**

- 缓冲区默认 128 MiB（`log.cleaner.dedupe.buffer.size`），表最多填到九成满（装填率上限 0.9），约装 503 万个 key。
- 脏段里的 key 比这更多时，这一轮只清一部分，下一轮接着清。

**为什么。** 用定长指纹代替 key，内存上限固定，不会被超长的 key 撑爆。

**对应 LeetCode：** 无直接对应的题
