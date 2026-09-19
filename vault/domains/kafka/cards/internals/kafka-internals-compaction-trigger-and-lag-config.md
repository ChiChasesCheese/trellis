---
id: kafka-internals-compaction-trigger-and-lag-config
node: internals.compaction
type: qa
step: 2
source: kafka-2e
---
## Q
Kafka 默认不是消息一写入就立刻压实，而是攒到「浑浊率」（浑浊消息占分区总消息的比例）达到一定程度才触发一轮压实。这个默认阈值是多少，为什么不设得更低或更高？另外，`min.compaction.lag.ms` 和 `max.compaction.lag.ms` 各自约束什么？

## A
默认阈值是 50%：阈值太低会让压实过于频繁，压实本身要占用 CPU/IO 并影响主题的读写性能；阈值太高则会让浑浊（未去重）的数据长期占用磁盘空间。50% 是一个折中值，管理员也可以调整。两个滞后参数控制的是时间边界而非比例：`min.compaction.lag.ms` 保证一条消息写入后至少要经过这么久才**可以**被压实（避免刚写入就被处理掉）；`max.compaction.lag.ms` 保证一条消息从写入起最多经过这么久就**必须**被压实掉，用于满足「必须在多少天内完成清理」这类硬性业务要求（例如 GDPR 要求收到删除请求后 30 天内完成）。
