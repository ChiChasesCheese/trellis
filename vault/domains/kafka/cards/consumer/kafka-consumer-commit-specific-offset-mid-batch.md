---
id: kafka-consumer-commit-specific-offset-mid-batch
node: consumer.offset-commit
type: qa
source: kafka-2e
---
## Q
`poll()` 一次可能返回一大批消息，如果只在处理完整批消息后才调用 `commitSync()`/`commitAsync()`（它们只会提交这批消息里的最后一个偏移量），万一处理到一半发生再均衡，重复处理的消息范围会有多大？有什么办法缩小这个范围？

## A
如果只在处理完整批之后才提交，一旦处理到中途发生再均衡，新的所有者会从上一批提交的偏移量开始读，导致这一整批已经处理过一部分的消息全部要重新处理一遍，重复范围等于整批数据。为了缩小这个范围，可以在批次处理过程中，针对某个具体分区调用带参数的 `commitSync(offsets)` / `commitAsync(offsets)`，显式提交「该分区目前已处理到的偏移量+1」，比如每处理1000条就提交一次，这样即使中途发生再均衡，重复处理的窗口也只有最近这一小段，而不是整批数据。
