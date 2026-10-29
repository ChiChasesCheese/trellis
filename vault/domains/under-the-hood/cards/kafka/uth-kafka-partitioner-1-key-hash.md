---
id: uth-kafka-partitioner-1-key-hash
node: kafka.partitioner
type: qa
step: 1
---
## Q
**带 key 的消息怎么选分区**｜Kafka · 4.0

生产者给带 key 的消息选分区，用的是什么哈希？为什么同一个 key 总是落到同一个分区？

## A
**结构。** `toPositive(murmur2(keyBytes)) % numPartitions`。`toPositive` 就是 `& 0x7fffffff`，清掉符号位。

**细节。**

- `murmur2` 是 32 位的非加密哈希，种子固定，同一个 key 的结果可重复。
- 不用 `Math.abs`：`Math.abs(Integer.MIN_VALUE)` 按规范仍返回负数，而 `& 0x7fffffff` 恒为非负。
- `partitioner.ignore.keys=true` 可以让 key 不参与选分区。

**为什么。** 无状态：不用查表，任何生产者都能独立算出同一个分区，同 key 的消息因此有序。

**对应 LeetCode：** LC 705 设计哈希集合 · LC 706 设计哈希映射
