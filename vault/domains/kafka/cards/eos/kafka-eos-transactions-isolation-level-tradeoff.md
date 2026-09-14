---
id: kafka-eos-transactions-isolation-level-tradeoff
node: eos.transactions
type: qa
source: kafka-2e
---
## Q
消费者的 `isolation.level` 参数在 `read_committed` 和默认的 `read_uncommitted` 之间怎么选？选 `read_committed` 会带来什么代价？

## A
`read_uncommitted`（默认）会把所有消息都返回给消费者，包括还在执行中、甚至最终会被中止的事务里的消息；`read_committed` 只返回已经成功提交的事务里的消息，以及所有非事务方式写入的消息，不会返回执行中或已中止事务的消息。要获得精确一次性保证，消费者必须配置成 `read_committed`。代价是：为了保证消息按顺序、干净地呈现，`read_committed` 不会把「最后稳定偏移量（LSO，last stable offset，即某个还没结束的事务开始之后写入的位置）」之后的消息交给消费者，这些消息要等到对应事务被提交、中止，或超过 `transaction.timeout.ms`（默认 15 分钟）被 broker 强制终止之后才会放出来——事务开得越久，消费者能看到的最新数据就滞后越多，端到端延迟也随之升高。
