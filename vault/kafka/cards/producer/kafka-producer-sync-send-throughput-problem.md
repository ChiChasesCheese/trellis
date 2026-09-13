---
id: kafka-producer-sync-send-throughput-problem
node: producer.client-basics
type: qa
source: kafka-2e
---
## Q
为什么说同步发送方式「通常不会被用在生产环境中」？

## A
因为同步发送要求发送线程在每次调用 send().get() 后一直阻塞，直到 broker 返回响应为止；根据集群繁忙程度，一次响应可能要等 2 毫秒甚至更久。在这段等待时间里，线程什么也做不了，甚至不能去发送下一条消息，这会严重拖累整体发送吞吐量，所以同步发送常见于示例代码，而不是生产环境。
