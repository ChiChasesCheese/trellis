---
id: hi-c-sd-kafka-n10-fault-tolerance
node: sd.deep-dives.kafka.notes
type: qa
step: 9
---
## Q
**Kafka · 容错与持久性：副本、确认、消费者故障**｜摘要 · 必会

Kafka 怎样保证不丢消息？消费者挂了会怎样？应怎样回答"Kafka 挂了怎么办"？

## A
- **复制：** 每个分区复制到多个 broker，一个 leader 加若干 follower；写入先到 leader 再复制。复制因子（replication factor）3 很常见：1 个 leader 加 2 个 follower，坏一个 broker 数据仍在，可以提升 follower。
- **`acks`：** 设为 `all` 时，消息要等所有同步副本（ISR）都收到才确认，是最强的持久性保证。
- **"Kafka 挂了怎么办"：** 常说"Kafka 总是可用，有时一致"；这取决于配置，`acks=all` 加 `min.insync.replicas` 时它宁可拒绝写入也不丢数据。这个问题不太现实，可以礼貌地反驳。更现实的是消费者挂了。
- **偏移量管理：** 消费者处理完消息后提交偏移量。重启时读取最后提交的偏移量继续，不会漏消息，但若在提交前崩溃，部分消息会被重复处理（至少一次）。
- **再均衡（rebalancing）：** 组内一个消费者挂了，Kafka 把它的分区重新分给剩下的消费者，保证所有分区仍有人处理。
- **何时提交偏移量是取舍：** 网络爬虫要在确认原始 HTML 已存进对象存储后再提交。消费者的工作越多，崩溃后要重做的就越多，所以让消费者的工作尽量小——爬虫就拆成两段：下载 HTML、解析 HTML。
