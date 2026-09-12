---
id: kafka-reliability-auto-offset-reset-tradeoff
node: reliability.consumer-reliable
type: qa
source: kafka-2e
---
## Q
一个消费者第一次启动，或者它请求的偏移量在 broker 上已经不存在了（比如超过保留期被删除）。`auto.offset.reset` 参数的 `earliest` 和 `latest` 两个取值，分别会让消费者怎么读，各自的代价是什么？

## A
设为 `earliest` 时，消费者会从分区**最开始**的位置读取，好处是尽量不漏掉任何数据，代价是可能会重复处理大量早已存在的历史消息。设为 `latest` 时，消费者从分区**末尾**（也就是当前最新位置）开始读，好处是不会处理旧的重复数据，代价是很可能**错过**在它开始读之前就已经写入、还没被消费过的消息。也就是「宁可重复也不丢」和「宁可漏掉也不重复」之间的取舍。
