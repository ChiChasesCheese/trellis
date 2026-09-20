---
id: kafka-mirroring-alt-mrc-observer-auto-promote
node: mirroring.alternatives
type: qa
step: 6
source: kafka-2e
---
## Q
多区域集群（MRC，multi-region cluster，Confluent Server 提供的一种延展集群变体）里的「观察者（observer）」副本是什么？为什么正常情况下它不会拖慢生产者，却又能在某个区域故障时自动帮上忙？

## A
观察者是一种**不属于 ISR（in-sync replicas，同步副本集合）的异步副本**：它持续从首领异步复制数据，但即使生产者配置了 `acks=all`，broker 也不会等观察者确认，所以观察者的存在不会给生产者的写入延迟增加负担；同时它又能正常把消息发送给消费者，起到分担读流量、跨区域容灾的作用。当某个区域故障导致 ISR 里的同步副本数量跌破配置的 `min.insync.replicas`（最少同步副本数）时，一个原本处于「同步」状态的观察者会被自动提升，正式加入 ISR，把同步副本数补回配置要求的数量，从而让集群在不丢数据的前提下继续接受写入；等故障区域恢复后，这个被提升的观察者又会自动降级回普通观察者角色，集群性能恢复正常——整个过程不需要人工干预就能实现快速、不丢数据的故障转移。
