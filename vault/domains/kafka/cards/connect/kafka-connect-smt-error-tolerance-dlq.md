---
id: kafka-connect-smt-error-tolerance-dlq
node: connect.smt
type: qa
step: 4
source: kafka-2e
---
## Q
一个数据池连接器（sink connector）在处理来自 Kafka 的记录时，遇到了一条格式损坏、无法正常处理的消息。配置参数 `error.tolerance` 能提供哪两种应对方式，分别适合什么场景？

## A
`error.tolerance` 可以让连接器在遇到处理失败的消息时选择：一种是**静默丢弃**这条损坏的消息，直接继续处理后面的记录，适合那种「个别脏数据丢了也无所谓、更看重管道不中断」的场景；另一种是把这条消息路由到一个专门的「死信队列（dead letter queue）」主题里，管道继续正常运行，同时保留下这些处理失败的消息供后续排查或人工修复，适合「不能悄悄丢数据、但也不想让一条坏消息卡住整个管道」的场景。这个配置不是某个特定连接器专属的，而是可以用在任意数据池连接器上的通用能力。
