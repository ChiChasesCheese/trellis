---
id: kafka-consumer-eager-vs-cooperative-rebalance
node: consumer.groups-rebalance
type: qa
step: 4
source: kafka-2e
---
## Q
「主动再均衡」（eager rebalance）和「协作再均衡」（cooperative/incremental rebalance）在处理分区重新分配时有什么根本区别？为什么协作再均衡对大型消费者群组更友好？

## A
主动再均衡要求所有消费者先放弃自己拥有的全部分区、重新加入群组，再统一获得新分配，整个群组在此期间完全停止消费（「停止世界」式停顿）。协作再均衡只把需要转移的那部分分区从原消费者手里收回、分配给别的消费者，其余消费者对未被重新分配的分区可以继续正常读取，不受影响。群组规模越大，一次完整的再均衡通常耗时越长，协作再均衡通过避免全员停顿，把再均衡对大型群组吞吐量的冲击降到最低。
