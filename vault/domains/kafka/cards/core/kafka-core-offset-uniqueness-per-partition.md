---
id: kafka-core-offset-uniqueness-per-partition
node: core.offsets
type: qa
step: 3
source: kafka-2e
---
## Q
偏移量的「唯一性」是在什么范围内成立的？两个不同分区里能不能出现相同的偏移量数值？

## A
偏移量只在同一个分区内保证唯一：给定分区里每条消息的偏移量都不同，且越往后的消息偏移量越大。但偏移量不是全局唯一的，不同分区各自独立计数，所以分区 A 的偏移量 100 和分区 B 的偏移量 100 是完全独立的两条消息，彼此没有关系。
