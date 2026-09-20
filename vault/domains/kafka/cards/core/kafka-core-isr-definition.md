---
id: kafka-core-isr-definition
node: core.replication-isr
type: qa
step: 2
source: kafka-2e
---
## Q
跟随者副本要满足什么条件才会被算作「同步副本」，从而留在 ISR（in-sync replicas，同步副本集合）里？

## A
跟随者副本会像消费者一样不断向首领发送 Fetch 请求来拉取消息，首领据此判断每个跟随者已经复制到了哪个偏移量、落后了多少。如果一个跟随者持续按时发来请求，且与最新消息的差距没有超过 replica.lag.time.max.ms 参数设定的时间阈值（例如 30 秒），它就被视为同步副本，留在 ISR 中；否则会被标记为不同步，暂时移出 ISR。
