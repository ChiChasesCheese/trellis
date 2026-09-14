---
id: kafka-internals-follower-read-highwatermark
node: internals.replication-protocol
type: qa
source: kafka-2e
---
## Q
Kafka 支持消费者直接从跟随者副本（follower replica）而不是首领副本（leader replica）读取消息（KIP-392），目的是就近读取以降低网络成本。但为什么这种读法仍然只能读到「已提交」的消息，且往往比从首领读要慢一点？

## A
首领在把消息发给跟随者做复制的同时，会把自己当前的**高水位标记（high watermark，即最近一次被判定为「已提交」的消息偏移量）**一并带过去，跟随者据此知道自己保存的消息里哪些已经被正式提交、可以对外提供。这保证了不论从首领还是跟随者读，读到的都只是已提交消息，可靠性一致。但高水位标记本身需要经过一次网络传输才能到达跟随者，这段传播延迟意味着跟随者「知道」某条消息已提交的时间，天然会比首领本身晚一点，所以如果最看重低延迟，应该直接从首领读。
