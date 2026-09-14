---
id: kafka-internals-follower-fetch-protocol
node: internals.replication-protocol
type: qa
source: kafka-2e
---
## Q
在 Kafka 里，跟随者副本（follower replica，不直接处理客户端请求的副本）是通过什么方式跟首领副本（leader replica）保持数据同步的？首领又是怎么据此判断某个跟随者「落后」了多少？

## A
跟随者会像消费者一样，主动向首领发送 `Fetch` 请求，请求里带着自己想要拉取的下一条消息的偏移量（offset）；这些偏移量是严格递增有序的。首领通过记录每个跟随者最近一次请求的偏移量，就能推算出该副本已经获取到哪里、与最新消息相差多少，从而判断它的复制进度和滞后程度。也就是说，同步进度完全靠跟随者「主动来拉」并汇报自己要的偏移量来体现，而不是首领主动推送后再确认。
