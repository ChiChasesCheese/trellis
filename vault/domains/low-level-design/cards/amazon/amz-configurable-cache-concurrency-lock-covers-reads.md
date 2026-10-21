---
id: amz-configurable-cache-concurrency-lock-covers-reads
node: amazon.amz-configurable-cache
type: qa
step: 8
tags: [grown]
---
## Q
在可配置缓存里，为什么连 `get` 也要加锁？只靠 GIL（全局解释器锁）够不够？

## A
不够。`get` 会改策略（LRU 挪到队尾、LFU 升一个桶），是写操作。`put` 的「检查还有没有空位 -> 淘汰 -> 登记」是多步复合操作，GIL 只保证单个字节码原子：容量 1 时两个线程同时看到「有空位」，缓存就有 2 条，超出容量。做法：一把锁包住每个公开操作，文件 IO 也在锁内（吞吐换正确性）；要提高吞吐再按 key 分片，每片一套策略和后端。
