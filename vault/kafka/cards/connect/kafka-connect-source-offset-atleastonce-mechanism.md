---
id: kafka-connect-source-offset-atleastonce-mechanism
node: connect.connect-basics
type: qa
source: kafka-2e
---
## Q
数据源连接器（source connector）任务在向 worker 汇报「已处理到哪里」时，用的是 Kafka 自己的分区和偏移量吗？worker 是在什么时机才把这个进度持久化下来，这个时机为什么和「至少一次传递」的保证有关？

## A
不是。数据源连接器返回给 worker 的每条记录都带着一个**逻辑分区和逻辑偏移量**，这是「源系统」自己的概念，与 Kafka 的分区/偏移量无关——比如文件数据源里，分区可以是某个文件，偏移量是文件里的行号或字符位置；JDBC 数据源里，分区可以是一张数据库表，偏移量是某条记录的 ID 或时间戳。worker 只有在把这些记录成功写入 Kafka、并收到 Kafka 的确认之后，才会把对应的逻辑偏移量保存下来（通常存进一个由 `offset.storage.topic` 指定的内部主题）。这个「先确认写入 Kafka 成功、再保存偏移量」的顺序保证了连接器崩溃重启后，最多只会从上一个已确认的偏移量重新读取一部分数据重复处理，而不会漏掉任何还没成功写入 Kafka 的数据——这正是「至少一次传递」语义的来源。
