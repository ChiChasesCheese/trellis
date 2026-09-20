---
id: kafka-consumer-heartbeat-session-timeout-death-detection
node: consumer.groups-rebalance
type: qa
step: 3
source: kafka-2e
---
## Q
消费者群组协调器（group coordinator，负责管理某个消费者群组成员关系的 broker）是靠什么机制判断一个消费者是否还「活着」，进而决定要不要触发再均衡？

## A
消费者会通过一个后台线程持续向群组协调器发送心跳（heartbeat），只要按时发送心跳就被认为存活。如果消费者在足够长的时间内没有发心跳（比如进程崩溃、无法继续处理），它的会话就会超时，协调器判定它「死亡」并触发一次再均衡，把它原本负责的分区转移给群组里其他消费者；而如果消费者是被正常关闭的，它会主动通知协调器离开群组，协调器会立即触发再均衡，不用等到会话超时才发现。
