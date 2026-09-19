---
id: kafka-internals-isr-out-condition
node: internals.replication-protocol
type: qa
step: 2
source: kafka-2e
---
## Q
一个跟随者副本（follower replica）在什么条件下会被首领判定为「不同步」，从而被移出 ISR（in-sync replicas，同步副本集合）？这个判定标准由哪个参数控制？

## A
首领会看两件事：一是这个跟随者有没有在最近 `replica.lag.time.max.ms`（默认场景下的滞后时间阈值）配置的时间窗口内发来过 `Fetch` 请求；二是即使发来了请求，它请求的偏移量与首领最新消息的偏移量之间的差距，是否已经超过了这个时间窗口所允许的追赶时间。只要满足其一，这个副本就被认为跟不上首领了，会被移出 ISR，直到重新追上。之所以用「时间」而不是「消息条数」作为阈值，是因为消息条数的滞后在流量高峰和低谷下含义差别很大，而不活跃/追赶所需的时间更能反映副本是否真的健康。
