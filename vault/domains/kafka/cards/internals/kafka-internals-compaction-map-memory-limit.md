---
id: kafka-internals-compaction-map-memory-limit
node: internals.compaction
type: qa
step: 4
source: kafka-2e
---
## Q
Kafka 管理员给压实线程分配的 map 内存，如果连一个日志片段（log segment）浑浊部分的全部键都放不下，会发生什么？管理员有哪两种解决办法？

## A
Kafka 并不要求这张去重用的 map 能装下整个分区浑浊部分的所有键，但至少要能装下**一个片段**的浑浊部分，否则会报错，压实无法正常进行。管理员的解决办法有两种：一是调大分配给压实线程的 map 内存总量（这个内存是所有压实线程共享分配的，比如 1 GB 内存配 5 个线程，每个线程平均可用 200 MB）；二是减少压实线程的数量，让每个线程能分到更多内存。如果内存放得下多个片段的键，Kafka 会优先压实最旧的片段，其余片段留到下一轮。
