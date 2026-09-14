---
id: kafka-producer-acks-0-fire-and-forget-risk
node: producer.acks-durability
type: qa
source: kafka-2e
---
## Q
生产者把 `acks` 设置为 0 会带来什么效果？为什么这个设置吞吐量最高，但风险也最大？

## A
`acks=0` 表示生产者发送消息后完全不等待 broker（Kafka 服务器节点）的任何响应就认为发送完成。因为不需要等待网络往返，生产者可以以网络能支持的最快速度连续发送消息，吞吐量最高；但代价是如果 broker 没收到消息（比如网络问题、broker 故障），生产者完全不会知道，消息就这样悄悄丢失了，没有任何报错。
