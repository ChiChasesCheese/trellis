---
id: kafka-consumer-auto-offset-reset-choices
node: consumer.poll-config
type: qa
step: 4
source: kafka-2e
---
## Q
消费者要读取一个没有已提交偏移量、或者偏移量已经因为长时间离线而失效的分区时，`auto.offset.reset` 的三个可选值 latest、earliest、none 分别会发生什么？

## A
`latest`（默认值）让消费者从这个分区里最新写入的位置开始读，也就是只处理消费者启动之后新产生的消息；`earliest` 让消费者从分区最开始的位置读起，会读到所有仍保留在分区里的历史消息；`none` 则完全不做自动处理，遇到无效偏移量直接抛出异常，把决定权交给应用程序自己处理。
