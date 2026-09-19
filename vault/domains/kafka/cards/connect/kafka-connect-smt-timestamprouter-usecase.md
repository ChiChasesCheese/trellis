---
id: kafka-connect-smt-timestamprouter-usecase
node: connect.smt
type: qa
step: 6
source: kafka-2e
---
## Q
`TimestampRouter` 这个 SMT 是根据消息的什么信息来改变目标主题的？在什么场景下这种「按时间戳路由」的能力特别有用？

## A
`TimestampRouter` 会根据消息自带的时间戳来决定这条消息最终应该被路由到哪个主题。这在数据池连接器（sink connector）把数据写入下游存储时特别有用：如果下游系统按时间对数据做了分区（比如按天/按月建不同的数据集或分区表），就可以用消息的时间戳自动算出它该落到哪个目标主题（进而对应下游哪个数据集），不需要在管道之外单独维护一套「消息时间 → 目标位置」的路由逻辑。
