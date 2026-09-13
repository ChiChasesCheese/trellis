---
id: kafka-consumer-static-membership-avoids-rebalance
node: consumer.groups-rebalance
type: qa
source: kafka-2e
---
## Q
给消费者配置一个唯一的 `group.instance.id`，让它成为群组的「固定成员」（static membership），这样做能避免什么开销？什么场景下特别有用？

## A
默认情况下消费者的群组成员身份是临时的，一旦离开群组（比如重启）就会失去原来的分区、重新加入时要走一次完整的再均衡流程重新分配分区。而固定成员被关闭后不会立即离开群组，只要在 `session.timeout.ms` 规定的时间内重新加入，就能拿回之前持有的原班分区，完全不触发再均衡。这对那些为分区维护了本地状态或缓存（比如聚合计算的中间结果）的应用特别有用，因为可以避免每次重启消费者都要重建这些昂贵的本地状态。
