---
id: uth-kafka-partitioner-2-add-partitions
node: kafka.partitioner
type: qa
step: 2
---
## Q
**加分区会打乱 key**｜Kafka · 4.0

一个主题从 6 个分区扩到 7 个，已有的 key 会怎样？

## A
**结构。** 映射是 `hash % N`，N 一变，几乎每个 key 的结果都变。

**细节。**

- 例：`hash % 6` 与 `hash % 7` 只在 `hash` 对 42 取余落在 0–5 时相等，即约 1/7 的 key 不动，约 6/7 换了分区。
- 公式在 `BuiltInPartitioner.partitionForKey`，只看 key 字节和当前分区数，不记任何历史。

**坑。** 同一个 key 的新旧消息进了不同分区，按 key 有序的保证就断了；压实主题里同一个 key 还会在两个分区各留一份。

**为什么。** 取模零状态，代价是扩容几乎全部重分布；一致性哈希只需搬走约 1/N 的 key。

**对应 LeetCode：** LC 706 设计哈希映射
