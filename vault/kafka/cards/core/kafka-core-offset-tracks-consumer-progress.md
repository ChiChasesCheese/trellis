---
id: kafka-core-offset-tracks-consumer-progress
node: core.offsets
type: qa
source: kafka-2e
---
## Q
一个消费者进程被重启后，为什么通常能从上次读到的地方继续处理，而不是重新从头读整个分区？

## A
消费者会针对它读取的每个分区保存一个「下一个要读取的偏移量」，这份进度信息通常保存在 Kafka 自身当中。消费者关闭或重启并不会丢失这份记录，恢复后可以直接从保存的偏移量继续读取，从而实现断点续读，而不必每次都从分区最开始重新消费一遍。
