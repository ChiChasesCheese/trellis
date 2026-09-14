---
id: kafka-consumer-fetch-min-bytes-tradeoff
node: consumer.poll-config
type: qa
source: kafka-2e
---
## Q
`fetch.min.bytes`（默认1字节）指定 broker 要凑够多少数据才把响应返回给消费者的拉取请求。把它调大对吞吐量和延迟分别有什么影响？

## A
把 `fetch.min.bytes` 调大，会让 broker 在主题流量不大时等到攒够足够多的数据才响应，减少了消费者和 broker 之间来回传输的次数，从而降低双方的 CPU 和网络负载，适合流量高峰期或消费者数量很多、想给 broker 减负的场景。代价是在低吞吐量时段，消费者要多等一会儿才能拿到数据，读取延迟会增加。
