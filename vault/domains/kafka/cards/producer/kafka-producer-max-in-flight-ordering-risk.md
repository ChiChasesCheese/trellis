---
id: kafka-producer-max-in-flight-ordering-risk
node: producer.timeouts-retries
type: qa
step: 5
source: kafka-2e
---
## Q
如果 `retries` 设置为非零、`max.in.flight.requests.per.connection`（生产者在收到响应前可以连续发送的消息批次数）大于1，为什么消息顺序可能被打乱？

## A
因为多个批次可以同时在途（in flight，已发送但还没收到 broker 响应），如果第一个批次写入失败而排在它后面的第二个批次先写入成功，broker 随后重试写入第一个批次并成功后，这两个批次在分区里的实际落地顺序就和发送顺序颠倒了。也就是说，只要允许多个未确认请求同时在途并且开启了重试，顺序就有被打乱的风险，在意消息顺序的场景需要额外权衡这个参数的取值。
